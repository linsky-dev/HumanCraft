#!/usr/bin/env python3
"""Build deterministic source, standard skill, and WorkBuddy skill archives."""

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/humancraft"
WORKBUDDY_METADATA = ROOT / "scripts/workbuddy-extension.json"
ROOTS = (
    ".github",
    "assets",
    "bench",
    "benchmark",
    "docs",
    "evals",
    "scripts",
    "skills",
    "tests",
    ".gitattributes",
    ".gitignore",
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
)
ALLOWED = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".log",
    ".md",
    ".png",
    ".py",
    ".sha256",
    ".svg",
    ".txt",
    ".yaml",
    ".yml",
    ".zip",
}
EXCLUDED = {".git", "__pycache__", ".venv", "dist", "local-eval-results", "execution-logs", "packets"}
WORKBUDDY_FIELDS = (
    "display_name",
    "display_name_en",
    "description_zh",
    "description_en",
)


def files(base, roots, optional=()):
    """Yield reviewed files and fail on unrecognized file types or symlinks."""
    optional_roots = set(optional)
    for name in roots:
        path = base / name
        if not path.exists():
            if name in optional_roots:
                continue
            raise ValueError(f"missing release path: {path}")

        # 按 ZIP 路径文本排序，避免 WindowsPath 的大小写折叠改变顺序。
        candidates = sorted(path.rglob("*"), key=lambda child: child.relative_to(base).as_posix()) if path.is_dir() else [path]
        for file_path in candidates:
            relative_path = file_path.relative_to(base)
            if any(part in EXCLUDED or part.startswith(".env") for part in relative_path.parts):
                continue
            if file_path.is_symlink():
                raise ValueError(f"symlink forbidden: {relative_path}")
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in ALLOWED and file_path.name not in {
                "LICENSE",
                ".gitignore",
                ".gitattributes",
            }:
                raise ValueError(f"unreviewed release type: {relative_path}")
            yield file_path, relative_path


def archive(destination, entries, prefix, overrides=None):
    """Write a reproducible ZIP and verify its integrity and skill entry point."""
    content_overrides = overrides or {}
    with zipfile.ZipFile(
        destination,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as output:
        for source_path, relative_path in entries:
            archive_path = f"{prefix}/{relative_path.as_posix()}"
            info = zipfile.ZipInfo(archive_path, date_time=(2026, 11, 24, 0, 0, 0))
            # 固定 ZIP 创建平台标志，否则 Windows 与 Linux 的归档字节不同。
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            content = content_overrides[relative_path] if relative_path in content_overrides else source_path.read_bytes()
            output.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    with zipfile.ZipFile(destination) as packaged:
        if packaged.testzip() is not None:
            raise ValueError(f"corrupt archive: {destination}")
        paths = packaged.namelist()
        if len(paths) != len(set(paths)):
            raise ValueError(f"duplicate paths: {destination}")
        skill_entry = f"{prefix}/SKILL.md" if prefix == "humancraft" else f"{prefix}/skills/humancraft/SKILL.md"
        if skill_entry not in paths:
            raise ValueError(f"missing skill entry: {skill_entry}")
    return len(paths)


def release_version():
    """Read the version maintained in the standard skill frontmatter."""
    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$', skill_text, re.MULTILINE)
    if match is None:
        raise ValueError("standard skill must define metadata.version")
    return match.group(1)


def load_workbuddy_metadata():
    """Load the four localized listing fields copied from the verified handoff."""
    metadata = json.loads(WORKBUDDY_METADATA.read_text(encoding="utf-8"))
    missing = [field for field in WORKBUDDY_FIELDS if not isinstance(metadata.get(field), str) or not metadata[field].strip()]
    if missing:
        raise ValueError(f"WorkBuddy metadata fields are missing or empty: {', '.join(missing)}")
    return metadata


def workbuddy_skill(skill_bytes, metadata, version, author=None):
    """Add WorkBuddy listing metadata while preserving the Markdown body bytes."""
    frontmatter = re.match(
        rb"\A---(?P<newline>\r?\n)(?P<fields>.*?)(?P<closing>\r?\n---\r?\n)",
        skill_bytes,
        re.DOTALL,
    )
    if frontmatter is None:
        raise ValueError("standard skill has invalid YAML frontmatter boundaries")

    existing_keys = set(
        re.findall(rb"(?m)^([A-Za-z0-9_-]+):", frontmatter.group("fields"))
    )
    generated_keys = [*WORKBUDDY_FIELDS, "version"]
    if author is not None:
        generated_keys.append("author")
    duplicate_keys = [field for field in generated_keys if field.encode("ascii") in existing_keys]
    if duplicate_keys:
        raise ValueError(f"WorkBuddy fields already exist in standard skill: {', '.join(duplicate_keys)}")

    newline = frontmatter.group("newline")
    fields = dict(metadata, version=version)
    generated_fields = [*WORKBUDDY_FIELDS, "version"]
    if author is not None:
        if not author.strip():
            raise ValueError("WorkBuddy author must not be empty")
        fields["author"] = author
        generated_fields.append("author")
    added_fields = b"".join(
        field.encode("ascii")
        + b": "
        + json.dumps(fields[field], ensure_ascii=False).encode("utf-8")
        + newline
        for field in generated_fields
    )
    frontmatter_end = frontmatter.start("closing")
    return skill_bytes[:frontmatter_end] + newline + added_fields + skill_bytes[frontmatter_end:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--workbuddy-author",
        help="Optional author value for WorkBuddy metadata when supplied by the maintainer.",
    )
    args = parser.parse_args()

    version = release_version()
    workbuddy_metadata = load_workbuddy_metadata()
    output_directory = args.output.resolve()
    output_directory.mkdir(parents=True, exist_ok=True)

    skill_entries = list(files(SKILL, ("SKILL.md", "LICENSE", "references", "assets", "scripts")))
    source_skill = (SKILL / "SKILL.md").read_bytes()
    workbuddy_entries = list(files(SKILL, ("SKILL.md", "LICENSE", "references", "assets", "scripts")))
    full_entries = list(files(ROOT, ROOTS, optional=(".gitattributes", "assets")))
    packages = (
        (
            "skill",
            skill_entries,
            "humancraft",
            None,
        ),
        (
            "WorkBuddy",
            workbuddy_entries,
            "humancraft",
            {
                Path("SKILL.md"): workbuddy_skill(
                    source_skill,
                    workbuddy_metadata,
                    version,
                    args.workbuddy_author,
                )
            },
        ),
        (
            "full",
            full_entries,
            f"HumanCraft-v{version}",
            None,
        ),
    )

    outputs = []
    for suffix, entries, prefix, overrides in packages:
        destination = output_directory / f"HumanCraft-v{version}-{suffix}.zip"
        count = archive(destination, entries, prefix, overrides)
        print(f"{destination.name}: {count} files")
        outputs.append(destination)

    checksums = "".join(
        f"{hashlib.sha256(package.read_bytes()).hexdigest()}  {package.name}\n"
        for package in outputs
    )
    (output_directory / "SHA256SUMS.txt").write_text(checksums, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

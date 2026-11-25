import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_SPEC = importlib.util.spec_from_file_location("humancraft_package", ROOT / "scripts/package.py")
package = importlib.util.module_from_spec(PACKAGE_SPEC)
PACKAGE_SPEC.loader.exec_module(package)


def read_frontmatter(markdown):
    """Return parsed YAML fields and the unchanged body bytes."""
    content = markdown.encode("utf-8") if isinstance(markdown, str) else markdown
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].strip() != b"---":
        raise AssertionError("missing YAML frontmatter opening delimiter")
    closing_line = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == b"---"),
        None,
    )
    if closing_line is None:
        raise AssertionError("missing YAML frontmatter closing delimiter")
    frontmatter = b"".join(lines[1:closing_line]).decode("utf-8")
    body = b"".join(lines[closing_line + 1 :])
    return yaml.safe_load(frontmatter), body


class PackagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary_directory = tempfile.TemporaryDirectory(prefix="humancraft-package-")
        cls.output = Path(cls.temporary_directory.name) / "first"
        cls.full_source_snapshot = {
            f"HumanCraft-v{package.release_version()}/{relative.as_posix()}": file_path.read_bytes()
            for file_path, relative in package.files(
                ROOT,
                package.ROOTS,
                optional=(".gitattributes", "assets"),
            )
        }
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/package.py"),
                "--output",
                str(cls.output),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        cls.with_author_output = Path(cls.temporary_directory.name) / "with-author"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/package.py"),
                "--output",
                str(cls.with_author_output),
                "--workbuddy-author",
                "Verified Maintainer",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.temporary_directory.cleanup()

    def archive_path(self, suffix):
        version = package.release_version()
        release_suffix = "WorkBuddy" if suffix == "workbuddy" else suffix
        return self.output / f"HumanCraft-v{version}-{release_suffix}.zip"

    def test_standard_skill_archive_is_exact_source_tree(self):
        expected = {
            f"humancraft/{relative.as_posix()}": file_path.read_bytes()
            for file_path, relative in package.files(
                package.SKILL,
                ("SKILL.md", "LICENSE", "references", "assets", "scripts"),
            )
        }
        with zipfile.ZipFile(self.archive_path("skill")) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(set(archive.namelist()), set(expected))
            for name, content in expected.items():
                self.assertEqual(archive.read(name), content, name)

    def test_workbuddy_archive_changes_only_metadata_and_preserves_body(self):
        expected_source = {
            f"humancraft/{relative.as_posix()}": file_path.read_bytes()
            for file_path, relative in package.files(
                package.SKILL,
                ("SKILL.md", "LICENSE", "references", "assets", "scripts"),
            )
        }
        with (
            zipfile.ZipFile(self.archive_path("skill")) as standard,
            zipfile.ZipFile(self.archive_path("workbuddy")) as workbuddy,
        ):
            self.assertIsNone(workbuddy.testzip())
            self.assertEqual(set(standard.namelist()), set(workbuddy.namelist()))
            skill_path = "humancraft/SKILL.md"
            for name, source_content in expected_source.items():
                if name == skill_path:
                    continue
                self.assertEqual(workbuddy.read(name), source_content, name)

            standard_fields, standard_body = read_frontmatter(standard.read(skill_path))
            workbuddy_fields, workbuddy_body = read_frontmatter(workbuddy.read(skill_path))
            self.assertEqual(workbuddy_body, standard_body)
            self.assertNotEqual(workbuddy.read(skill_path), standard.read(skill_path))

        metadata = json.loads(package.WORKBUDDY_METADATA.read_text(encoding="utf-8"))
        for field in package.WORKBUDDY_FIELDS:
            self.assertEqual(workbuddy_fields[field], metadata[field])
        self.assertEqual(workbuddy_fields["name"], "humancraft")
        self.assertEqual(workbuddy_fields["description"], standard_fields["description"])
        self.assertEqual(workbuddy_fields["version"], package.release_version())
        self.assertEqual(workbuddy_fields["metadata"]["version"], package.release_version())
        self.assertNotIn("author", workbuddy_fields)

    def test_full_archive_includes_available_root_assets(self):
        expected_assets = {
            f"HumanCraft-v{package.release_version()}/{relative.as_posix()}": file_path.read_bytes()
            for file_path, relative in package.files(ROOT, ("assets",), optional=("assets",))
        }
        with zipfile.ZipFile(self.archive_path("full")) as archive:
            self.assertIsNone(archive.testzip())
            contents = set(archive.namelist())
            asset_prefix = f"HumanCraft-v{package.release_version()}/assets/"
            packaged_assets = {name for name in contents if name.startswith(asset_prefix)}
            self.assertEqual(packaged_assets, set(expected_assets))
            for name, content in expected_assets.items():
                self.assertIn(name, contents)
                self.assertEqual(archive.read(name), content)

    def test_full_archive_matches_packaging_input_snapshot_bytes(self):
        with zipfile.ZipFile(self.archive_path("full")) as archive:
            self.assertEqual(set(archive.namelist()), set(self.full_source_snapshot))
            for name, content in self.full_source_snapshot.items():
                self.assertEqual(archive.read(name), content, name)

    def test_optional_root_assets_can_be_absent(self):
        with tempfile.TemporaryDirectory(prefix="humancraft-no-assets-") as directory:
            temporary_root = Path(directory)
            (temporary_root / "scripts").mkdir()
            result = list(package.files(temporary_root, ("assets", "scripts"), optional=("assets",)))
        self.assertEqual(result, [])

    def test_checksum_manifest_covers_three_packages(self):
        manifest = self.output / "SHA256SUMS.txt"
        rows = [line.split("  ", 1) for line in manifest.read_text(encoding="utf-8").splitlines()]
        packages = [self.archive_path(suffix) for suffix in ("skill", "workbuddy", "full")]
        self.assertEqual([name for _, name in rows], [path.name for path in packages])
        for (expected_hash, filename), archive_path in zip(rows, packages):
            self.assertEqual(filename, archive_path.name)
            self.assertEqual(expected_hash, hashlib.sha256(archive_path.read_bytes()).hexdigest())

    def test_archives_are_reproducible(self):
        second_output = Path(self.temporary_directory.name) / "second"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/package.py"),
                "--output",
                str(second_output),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        for suffix in ("skill", "workbuddy", "full"):
            first = self.archive_path(suffix)
            second = second_output / first.name
            self.assertEqual(first.read_bytes(), second.read_bytes(), first.name)
        self.assertEqual(
            (self.output / "SHA256SUMS.txt").read_bytes(),
            (second_output / "SHA256SUMS.txt").read_bytes(),
        )

    def test_optional_author_changes_only_workbuddy_metadata(self):
        for suffix in ("skill", "full"):
            self.assertEqual(
                self.archive_path(suffix).read_bytes(),
                (self.with_author_output / self.archive_path(suffix).name).read_bytes(),
            )

        default_workbuddy_path = self.archive_path("workbuddy")
        authored_workbuddy_path = self.with_author_output / default_workbuddy_path.name
        with (
            zipfile.ZipFile(default_workbuddy_path) as default_archive,
            zipfile.ZipFile(authored_workbuddy_path) as authored_archive,
        ):
            self.assertEqual(set(default_archive.namelist()), set(authored_archive.namelist()))
            for name in default_archive.namelist():
                if name != "humancraft/SKILL.md":
                    self.assertEqual(default_archive.read(name), authored_archive.read(name), name)
            default_fields, default_body = read_frontmatter(default_archive.read("humancraft/SKILL.md"))
            authored_fields, authored_body = read_frontmatter(authored_archive.read("humancraft/SKILL.md"))

        self.assertNotIn("author", default_fields)
        self.assertEqual(authored_fields["author"], "Verified Maintainer")
        self.assertEqual(default_body, authored_body)

        checksum_rows = [
            line.split("  ", 1)
            for line in (self.with_author_output / "SHA256SUMS.txt")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        for digest, filename in checksum_rows:
            archive_path = self.with_author_output / filename
            self.assertEqual(digest, hashlib.sha256(archive_path.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
# Assertions are the validation mechanism; fail closed in optimized mode.
if not __debug__: raise SystemExit("Validation requires Python without -O")
import json,re,yaml
root=Path(__file__).resolve().parents[1]; skill=root/'skills/humancraft'
files=list(root.rglob('*.md'))
for p in files:
    t=p.read_text(encoding='utf-8'); assert t.startswith('---\n'),p
    _,front,body=t.split('---',2); m=yaml.safe_load(front); assert isinstance(m,dict),p
    assert isinstance(m.get('name'),str) and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',m['name']) and len(m['name'])<=64,p
    assert isinstance(m.get('description'),str) and 0<len(m['description'])<=1024,p
    if p.name=='SKILL.md':
        assert m['name']==p.parent.name and len(t.splitlines())<=500,p
        assert all(isinstance(k,str) and isinstance(v,str) for k,v in m.get('metadata',{}).items()),p
        for link in re.findall(r'\]\(([^)]+)\)',body):
            if not link.startswith(('http://','https://','#')): assert (p.parent/link).is_file(),link
for f in root.rglob('*'):
    if f.is_file(): assert f.suffix.lower() not in ('.pdf','.epub','.docx'),f
cases=json.loads((root/'evals/cases.json').read_text(encoding='utf-8')); assert len({c['id'] for c in cases})==len(cases) and all(c['prompt'] and c['assertions'] and type(c['should_trigger']) is bool for c in cases)
a=json.loads((root/'evals/activation.json').read_text(encoding='utf-8'));assert len({x['id'] for x in a})==len(a) and all(x['query'] and type(x['should_trigger']) is bool for x in a)
print(f'PASS: {len(files)} Markdown YAML headers; skill directory/name, description, entry links, {len(cases)} behavior cases, {len(a)} activation cases. Local specification checks; not official client import.')

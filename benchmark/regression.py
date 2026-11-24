#!/usr/bin/env python3
"""Same current agent authored repairs; frozen v0.3 fixture versus v0.4, DOM memory only."""
import argparse,json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parent

def render(page,html):
    page.evaluate('''()=>{if(!window.__hcStorage){const m=new Map();window.__hcStorage={getItem:k=>m.get(k)??null,setItem:(k,v)=>m.set(k,v)}}}''')
    page.set_content(html.replace('<script>','<script>{',1).replace('</script>','}</script>',1))

def repeat_import(p,html):
    p.get_by_role('button',name='Import 3 records').click()
    p.get_by_role('button',name='Retry failed record').click()
    expect(p.get_by_text('3 stored; 0 failed')).to_be_visible(timeout=700)
    p.get_by_role('button',name='Import 3 records').click()
    assert p.evaluate("JSON.parse(window.__hcRead('records'))")==['A','B','C'],'repeat import lost previously stored C'
    expect(p.get_by_text('3 stored; 0 failed')).to_be_visible(timeout=700)

def repeat_archive(p,html):
    p.get_by_role('button',name='Approve and start').click()
    expect(p.get_by_text('Record A-17 archived')).to_be_visible(timeout=1500)
    assert p.evaluate("JSON.parse(window.__hcRead('archived'))") is True
    expect(p.get_by_role('button',name='Approve and start')).to_be_disabled(timeout=500)

def reload_archive(p,html):
    p.get_by_role('button',name='Approve and start').click()
    expect(p.get_by_text('Record A-17 archived')).to_be_visible(timeout=1500)
    render(p,html)
    expect(p.get_by_text('Record A-17 archived')).to_be_visible(timeout=500)
    expect(p.get_by_role('button',name='Approve and start')).to_be_disabled(timeout=500)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--executable');ap.add_argument('--output',default=str(ROOT/'evidence-v04'));a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True);rows=[]
    with sync_playwright() as pw:
        b=pw.chromium.launch(headless=True,**({'executable_path':a.executable} if a.executable else {}))
        for width,height in [(1280,900),(390,844)]:
            for variant,filename in [('v03','baseline-v03.html'),('v04','index.html')]:
                html=(ROOT/'fixture'/filename).read_text()
                for test in [repeat_import,repeat_archive,reload_archive]:
                    ctx=b.new_context(viewport={'width':width,'height':height});p=ctx.new_page();ctx.tracing.start(screenshots=True,snapshots=True,sources=True);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));status='ERROR';reason=''
                    try:
                        render(p,html);expect(p.get_by_role('heading',name='Workflow lab')).to_be_visible(timeout=700);test(p,html);status='PASS'
                    except AssertionError as e:status='FAIL';reason=str(e)[:1000]
                    except Exception as e:reason=str(e)[:1000]
                    if errors:status='ERROR';reason=str(errors)
                    name=f'{width}-{variant}-{test.__name__}';p.screenshot(path=out/(name+'.png'),full_page=True);ctx.tracing.stop(path=out/(name+'.zip'));ctx.close();rows.append(dict(variant=variant,case=test.__name__,width=width,result=status,reason=reason,expected='FAIL' if variant=='v03' else 'PASS',trace=name+'.zip'))
        report=dict(scope='self-application, synthetic DOM component; memory storage; no independent agent comparison or production persistence',browser=b.version,results=rows);b.close()
    (out/'regression.json').write_text(json.dumps(report,indent=2));print(sum(x['result']==x['expected'] for x in rows),'/',len(rows),'expected regression outcomes');sys.exit(int(any(x['result']!=x['expected'] for x in rows)))

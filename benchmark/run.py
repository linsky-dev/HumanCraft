#!/usr/bin/env python3
import argparse,json,platform,sys,time,threading,functools
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parent

def mode(p):
 p.get_by_label('Target workspace').select_option('Team');p.get_by_role('button',name='Apply setting').click();assert p.evaluate("JSON.parse(window.__hcRead('settings'))")=={'Team':True},'wrong target write';expect(p.get_by_text('Active target: Team')).to_be_visible(timeout=500)
def draft(p):
 p.get_by_label('Document note').fill('Retain me');
 if p.url=='about:blank': render_component(p, p.evaluate('window.__hcFault'))
 else: p.reload()
 expect(p.get_by_label('Document note')).to_have_value('Retain me',timeout=500)
def batch(p):
 p.get_by_role('button',name='Import 3 records').click();expect(p.get_by_text('2 stored; 1 failed: C')).to_be_visible(timeout=500);p.get_by_role('button',name='Retry failed record').click();assert p.evaluate("JSON.parse(window.__hcRead('records'))")==['A','B','C'],'duplicate writes';expect(p.get_by_text('3 stored; 0 failed')).to_be_visible(timeout=500)
def cancel(p):
 p.get_by_role('button',name='Approve and start').click();p.get_by_role('button',name='Cancel pending action').click();expect(p.get_by_text('Cancelled before commit')).to_be_visible(timeout=500);p.wait_for_timeout(850) # observe beyond scheduled commit
 assert not p.evaluate("JSON.parse(window.__hcRead('archived')||'false')"),'cancelled action committed';expect(p.get_by_text('Record A-17 active')).to_be_visible(timeout=500)
def wait(p):
 p.get_by_role('button',name='Start check').click();expect(p.get_by_text('Checking records; duration unknown')).to_be_visible(timeout=500);p.get_by_role('button',name='Simulate dependency failure').click();expect(p.get_by_text('Check failed:',exact=False)).to_be_visible(timeout=500)
def handoff(p):
 p.get_by_role('button',name='Submit for review').click();expect(p.get_by_text('Choose a reviewer before submitting')).to_be_visible(timeout=500);p.get_by_label('Assigned reviewer').select_option('Reviewer B');p.get_by_role('button',name='Submit for review').click();expect(p.get_by_text('Awaiting Reviewer B')).to_be_visible(timeout=500)
def a11y(p):
 field=p.get_by_role('textbox',name='Document note');expect(field).to_be_visible(timeout=500);p.keyboard.press('Tab');p.keyboard.press('Tab');p.keyboard.press('Tab');expect(field).to_be_focused(timeout=500)
CASES=[('mode','HC-B02',mode),('draft','HC-B03',draft),('batch','HC-B06',batch),('cancel','HC-B07',cancel),('wait','HC-B04',wait),('handoff','HC-B05/09',handoff),('a11y','accessible-name-keyboard',a11y)]
def render_component(p,variant):
 # Offline DOM component harness: memory adapter, not browser persistence.
 p.evaluate("""fault=>{window.__hcFault=fault; if(!window.__hcStorage){const store=new Map();window.__hcStorage={getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,v)}}}""",variant)
 html=(ROOT/'fixture/index.html').read_text().replace('<script>','<script>{',1).replace('</script>','}</script>',1)
 p.set_content(html)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--engine',choices=['chromium','firefox','webkit'],default='chromium');ap.add_argument('--executable');ap.add_argument('--component',action='store_true');ap.add_argument('--output',default=str(ROOT/'evidence'));a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True);results=[]
 server=None
 if not a.component:
  server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(SimpleHTTPRequestHandler,directory=str(ROOT/'fixture')))
  threading.Thread(target=server.serve_forever,daemon=True).start()
  base=f'http://127.0.0.1:{server.server_port}/index.html'
 with sync_playwright() as pw:
  browser=getattr(pw,a.engine).launch(headless=True,**({'executable_path':a.executable} if a.executable else {}));version=browser.version
  for width,height in [(1280,900),(390,844)]:
   for fault,rule,test in CASES:
    for variant in ['reference',fault]:
     ctx=browser.new_context(viewport={'width':width,'height':height});p=ctx.new_page();start=time.monotonic();ctx.tracing.start(screenshots=True,snapshots=True,sources=True);state='ERROR';reason='';page_errors=[];p.on('pageerror',lambda error:page_errors.append(str(error)))
     try:
      if a.component: render_component(p,variant)
      else: p.goto(base+'?fault='+variant)
      expect(p.get_by_role('heading',name='Workflow lab')).to_be_visible();
      if page_errors: raise RuntimeError(str(page_errors))
      try: test(p);state='PASS'
      except AssertionError as e: state='FAIL';reason=str(e)[:700]
      if page_errors:state='ERROR';reason=str(page_errors)
     except Exception as e:reason=str(e)[:700];state='ERROR'
     finally:
      name=f'{width}-{fault}-{variant}';p.screenshot(path=out/(name+'.png'),full_page=True);ctx.tracing.stop(path=out/(name+'.zip'));ctx.close()
     results.append(dict(case=fault,rule=rule,variant=variant,width=width,result=state,reason=reason,expected='PASS' if variant=='reference' else 'FAIL',seconds=round(time.monotonic()-start,3),screenshot=name+'.png',trace=name+'.zip'))
  browser.close()
 if server: server.shutdown();server.server_close()
 report={'engine':a.engine,'browser_version':version,'python':platform.python_version(),'scope':('offline DOM component fixture; memory adapter and rerender, not persistence/E2E' if a.component else 'local HTTP synthetic E2E fixture; not model A/B or production test'),'results':results};(out/'results.json').write_text(json.dumps(report,indent=2));good=sum(x['result']==x['expected'] for x in results);print(f'{good}/{len(results)} expected outcomes; reference pass={sum(x["variant"]=="reference" and x["result"]=="PASS" for x in results)}; mutants detected={sum(x["variant"]!="reference" and x["result"]=="FAIL" for x in results)}');return int(good!=len(results))
if __name__=='__main__':sys.exit(main())

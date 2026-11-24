#!/usr/bin/env python3
"""Public development verifier. Browser DOM test, not human research or a production backend."""
import argparse, hashlib, json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright, expect, TimeoutError as PlaywrightTimeout
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(condition,message):
    if not condition:raise AssertionError(message)
def state(p):return p.evaluate("window.readState()")
def button(p,s):return p.get_by_role('button',name=s,exact=True)
def status(p,s):expect(p.get_by_role('status')).to_contain_text(s,timeout=800)
def search(p,q):
    p.get_by_label('Search records').fill(q);button(p,'Search').click()
def scenario(p,task,kind):
    adverse=kind=='adverse'
    if task=='stale-search':
        search(p,'alpha')
        if adverse:search(p,'beta')
        q='beta' if adverse else 'alpha'
        status(p,'Results for '+q);p.wait_for_timeout(240)
        check(state(p)=={'query':q,'result':q},'stale result overwrote latest search')
        status(p,'Results for '+q)
    elif task=='revoked-access':
        button(p,'Preview').click()
        if adverse:button(p,'Revoke access').click()
        # A disabled action is acceptable if refusal is clear.
        if button(p,'Publish').is_enabled():button(p,'Publish').click()
        check(state(p)['published'] is (not adverse),'publication did not respect current authorization')
        status(p,'revoked' if adverse else 'Published')
    elif task=='draft-switch':
        p.get_by_label('Note').fill('Alpha note')
        if adverse:
            p.get_by_label('Record').select_option('B')
            expect(p.get_by_label('Note')).to_have_value('')
            p.get_by_label('Note').fill('Beta note')
            p.get_by_label('Record').select_option('A')
            expect(p.get_by_label('Note')).to_have_value('Alpha note',timeout=800)
            check(state(p)['notes']=={'A':'Alpha note','B':'Beta note'},'draft isolation or retention failed')
        else:check(state(p)['notes']['A']=='Alpha note','draft not retained')
    elif task=='preview-drift':
        button(p,'Review').click()
        if adverse:
            p.get_by_label('Target').select_option('B')
            if button(p,'Execute').is_enabled():button(p,'Execute').click()
            check(state(p)['applied']==[],'stale approval executed wrong target')
            button(p,'Review').click()
        button(p,'Execute').click()
        check(state(p)['applied']==['B' if adverse else 'A'],'fresh approval did not execute exactly once')
        status(p,'Executed '+('B' if adverse else 'A'))
    elif task=='undo-trash':
        button(p,'Remove A').click()
        check(state(p)['items']==['B'],'remove did not change actual data')
        status(p,'A removed')
        if adverse:
            button(p,'Undo removal').click()
            check(sorted(state(p)['items'])==['A','B'],'undo did not restore record')
            expect(p.get_by_text('A, B',exact=True)).to_be_visible(timeout=800)
    elif task=='empty-filter':
        p.get_by_label('Filter records').fill('missing' if adverse else 'Alpha')
        check(state(p)['items']==([] if adverse else ['Alpha']),'filter failed')
        if adverse:
            status(p,'No results');button(p,'Clear filter').click()
            check(state(p)['items']==['Alpha','Beta'] and state(p)['filter']=='','filter recovery failed')
            expect(p.get_by_label('Filter records')).to_have_value('')
            expect(p.get_by_role('listitem')).to_have_count(2)
    elif task=='duplicate-send':
        if adverse:
            button(p,'Send request').evaluate('(b)=>{b.click();b.click()}')
        else:button(p,'Send request').click()
        status(p,'Sending');status(p,'Request sent');p.wait_for_timeout(140)
        check(state(p)=={'sent':1,'pending':False},'duplicate or lost request')
    elif task=='dialog-focus':
        button(p,'Open details').click()
        expect(p.get_by_role('dialog',name='Record details')).to_be_visible(timeout=800)
        if adverse:
            expect(button(p,'Close details')).to_be_focused(timeout=800)
            p.keyboard.press('Escape')
            expect(p.get_by_role('dialog',name='Record details')).not_to_be_visible(timeout=800)
            expect(button(p,'Open details')).to_be_focused(timeout=800)
        else:button(p,'Close details').click()
        check(state(p)['open'] is False,'dialog remained open')
        expect(p.get_by_role('dialog',name='Record details')).not_to_be_visible(timeout=800)
    else:raise ValueError(task)
def main():
    a=argparse.ArgumentParser();a.add_argument('--task');a.add_argument('--app');a.add_argument('--calibrate',action='store_true');a.add_argument('--output',required=True);a.add_argument('--executable');a.add_argument('--engine',default='chromium',choices=['chromium','firefox','webkit']);args=a.parse_args()
    if args.calibrate==bool(args.task or args.app) or (not args.calibrate and not(args.task and args.app)):a.error('use --calibrate OR --task and --app')
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    rows=[]
    task_dirs=sorted((ROOT/'tasks').iterdir()) if args.calibrate else [ROOT/'tasks'/args.task]
    with sync_playwright() as pw:
        browser=getattr(pw,args.engine).launch(headless=True,**({'executable_path':args.executable} if args.executable else {}))
        for d in task_dirs:
            spec=json.loads((d/'task.json').read_text())
            variants=[('starter',d/'starter.html'),('reference',d/'reference.html')] if args.calibrate else [('submission',Path(args.app))]
            for variant,app in variants:
                html=app.read_text(encoding="utf-8")
                for viewport in [(1280,900),(390,844)]:
                    for kind in ('normal','adverse'):
                        context=browser.new_context(viewport={'width':viewport[0],'height':viewport[1]})
                        # External traffic is forbidden; no network APIs, real backend or persistent browser storage.
                        context.route('**/*',lambda route:route.abort())
                        p=context.new_page();p.set_default_timeout(1200);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
                        start=time.monotonic();result='ERROR';reason=''
                        name=f'{spec["id"]}-{variant}-{viewport[0]}-{kind}'
                        try:
                            p.set_content(html,wait_until='domcontentloaded',timeout=2500)
                            check(callable_state(p),'missing state interface')
                            scenario(p,spec['id'],kind)
                            result='PASS'
                        except (AssertionError, PlaywrightTimeout) as e:result='FAIL';reason=str(e)[:900]
                        except Exception as e:result='ERROR';reason=str(e)[:900]
                        if errors:result='FAIL';reason='application JavaScript error: '+ '; '.join(errors)[:850]
                        elapsed=round(time.monotonic()-start,3)
                        try:p.screenshot(path=out/(name+'.png'),timeout=1500)
                        except Exception:pass
                        context.close()
                        expected=('FAIL' if variant=='starter' and kind=='adverse' else 'PASS') if args.calibrate else None
                        rows.append(dict(task=spec['id'],variant=variant,viewport=viewport[0],scenario=kind,result=result,expected=expected,critical=spec['critical'] and kind=='adverse',reason=reason,seconds=elapsed,app_sha256=sha(app),screenshot=name+'.png' if (out/(name+'.png')).exists() else None))
        report=dict(scope='public development synthetic DOM workflow; in-memory state, no live backend, no independent agent or human inference',engine=args.engine,browser=browser.version,verifier_sha256=sha(Path(__file__)),results=rows)
        browser.close()
    (out/'results.json').write_text(json.dumps(report,indent=2))
    ok=all(x['result']==(x['expected'] if args.calibrate else 'PASS') for x in rows)
    print(f"{sum(x['result']==(x['expected'] if args.calibrate else 'PASS') for x in rows)}/{len(rows)} expected outcomes")
    return 0 if ok else 1
def callable_state(p):return p.evaluate("typeof window.readState==='function'")
if __name__=='__main__':sys.exit(main())

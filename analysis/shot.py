"""Screenshot the page at desktop (light, dark) and phone widths. Usage: python3 shot.py ["js to run before the shot" ...]"""
import asyncio, sys, subprocess, time, os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
PAGE=os.path.join(HERE,'..','page')
LOCAL_TOPOJSON=os.path.join(HERE,'npmtmp','package','dist','topojson.min.js')  # optional offline copy: npm pack topojson@3.0.2
async def main():
    srv=subprocess.Popen([sys.executable,'-m','http.server','8765','--directory',PAGE],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b=await p.chromium.launch()
            for name,w,h,scheme in [('desk-light',1280,900,'light'),('desk-dark',1280,900,'dark'),('phone-light',400,860,'light')]:
                ctx=await b.new_context(viewport={'width':w,'height':h},color_scheme=scheme,device_scale_factor=1)
                pg=await ctx.new_page(); errs=[]
                pg.on('console',lambda m: errs.append(m.text) if m.type in('error','warning') else None); pg.on('pageerror',lambda e: errs.append('PAGEERROR '+str(e)))
                # wrap like the publish skeleton
                html=open(PAGE+'/index.html').read()
                open(PAGE+'/_t.html','w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>'+html+'</body></html>')
                if os.path.exists(LOCAL_TOPOJSON):   # sandbox without CDN access: serve the library locally and skip web fonts
                    await pg.route('**/topojson.min.js',lambda r: r.fulfill(path=LOCAL_TOPOJSON,content_type='application/javascript'))
                    await pg.route('**/fonts.googleapis.com/**',lambda r: r.abort())
                await pg.goto('http://localhost:8765/_t.html'); await pg.wait_for_timeout(2500)
                for a in sys.argv[1:]:
                    await pg.evaluate(a); await pg.wait_for_timeout(400)
                sw=await pg.evaluate('document.documentElement.scrollWidth'); 
                await pg.screenshot(path=f'shot-{name}.png',full_page=True)
                print(name,'scrollWidth',sw,'errors',errs[:6])
                await ctx.close()
            await b.close()
    finally:
        srv.terminate(); os.remove(PAGE+'/_t.html')
asyncio.run(main())

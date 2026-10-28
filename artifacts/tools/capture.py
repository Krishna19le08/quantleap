"""Reusable capture tool. Usage: python artifacts/tools/capture.py <round_label> [--port 8765]
Starts python http.server itself, captures full-page (517,820,1440,390) and per-section
(517,1440) screenshots into artifacts/screenshots/<label>/, prints section top/height,
page height, overflow, console errors, failed requests, broken images. Writes <label>/metrics.json."""
import sys, os, json, subprocess, time, urllib.request
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SECTIONS = [  # inventory id -> selector
    ("header", "header.site-header"), ("hero", "main > section.hero"),
    ("focus", "#focus"), ("ventures", "#ventures"), ("nation", "#nation"),
    ("model", "#model"), ("impact", "#impact"), ("insights", "#insights"),
    ("presence", "#presence"), ("cta-1", "section#contact"),
    ("cta-2", "main > section.cta:not(#contact)"), ("footer", "footer.site-footer")]
FULL = [(517, 1600), (820, 1100), (1440, 900), (390, 844)]
SECT = [517, 1440]
INV = {s["id"]: s["height"] for s in json.load(open(os.path.join(ROOT, "artifacts", "section-inventory.json")))["sections"]}

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    label = args[0] if args else "round0"
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8765
    out = os.path.join(ROOT, "artifacts", "screenshots", label)
    os.makedirs(out, exist_ok=True)
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    url = f"http://127.0.0.1:{port}/index.html"
    try:
        for _ in range(50):
            try: urllib.request.urlopen(url, timeout=1); break
            except Exception: time.sleep(0.1)
        result = {}
        with sync_playwright() as p:
            b = p.chromium.launch()
            for w, h in FULL:
                ctx = b.new_context(viewport={"width": w, "height": h})
                pg = ctx.new_page()
                errs, fails, bad = [], [], []
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
                pg.on("requestfailed", lambda r: fails.append(r.url))
                pg.on("response", lambda r: bad.append(f"{r.status} {r.url}") if r.status >= 400 else None)
                pg.goto(url, wait_until="networkidle")
                pg.wait_for_timeout(800)
                # scroll through to trigger lazy/reveal, then return to top
                H = pg.evaluate("document.documentElement.scrollHeight")
                for y in range(0, H, 400):
                    pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(60)
                pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(400)
                m = pg.evaluate("""(sels)=>{
                  const r={};
                  r.pageHeight=document.documentElement.scrollHeight;
                  r.scrollWidth=document.documentElement.scrollWidth;
                  r.innerWidth=innerWidth;
                  r.hOverflow=r.scrollWidth>r.innerWidth;
                  r.brokenImages=[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.getAttribute('src'));
                  r.sections={};
                  for(const [id,s] of sels){const e=document.querySelector(s);
                    if(!e){r.sections[id]=null;continue}
                    const b=e.getBoundingClientRect();
                    r.sections[id]={top:Math.round(b.top+scrollY),height:Math.round(b.height)};}
                  return r;}""", SECTIONS)
                m.update(consoleErrors=errs, failedRequests=fails, httpErrors=bad)
                pg.screenshot(path=os.path.join(out, f"{label}_full_{w}.png"), full_page=True)
                if w in SECT:
                    for sid, sel in SECTIONS:
                        loc = pg.locator(sel).first
                        if loc.count() and m["sections"][sid]:
                            loc.screenshot(path=os.path.join(out, f"{label}_{w}_{sid}.png"))
                result[w] = m
                ctx.close()
            b.close()
        json.dump(result, open(os.path.join(out, "metrics.json"), "w"), indent=1)
        for w, m in result.items():
            print(f"\n=== {w}px  pageHeight={m['pageHeight']} scrollWidth={m['scrollWidth']} hOverflow={m['hOverflow']}")
            print(f"  brokenImages={m['brokenImages']} consoleErrors={m['consoleErrors']} failedReq={m['failedRequests']} http>=400={m['httpErrors']}")
            if w in SECT:
                scale = w / 517
                print(f"  {'section':10} {'top':>6} {'height':>6}  ref_h*scale")
                for sid, _ in SECTIONS:
                    s = m["sections"][sid]
                    print(f"  {sid:10} " + (f"{s['top']:>6} {s['height']:>6}  {INV[sid]*scale:.0f}" if s else "MISSING"))
        print(f"\nscreenshots: {out}")
    finally:
        srv.terminate()

if __name__ == "__main__":
    main()

"""Functional checks with Python Playwright. Serves site on port 8791 (not 8765)."""
import sys, http.server, socketserver, threading, os, json, functools
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"D:\projects\quantleap"
PORT = 8791
RESULTS = []


def rec(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + (" :: " + str(detail) if detail else ""))


class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


H = functools.partial(Q, directory=ROOT)
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.ThreadingTCPServer(("127.0.0.1", PORT), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{PORT}/index.html"


def load(browser, w, h=900, errs=None, fails=None):
    ctx = browser.new_context(viewport={"width": w, "height": h})
    p = ctx.new_page()
    if errs is not None:
        p.on("console", lambda m: errs.append(f"{m.type}: {m.text}") if m.type in ("error", "warning") else None)
        p.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
    if fails is not None:
        p.on("requestfailed", lambda r: fails.append(f"{r.url} {r.failure}"))
        p.on("response", lambda r: fails.append(f"{r.status} {r.url}") if r.status >= 400 else None)
    p.goto(URL, wait_until="networkidle")
    p.wait_for_selector("#nav", state="attached")
    p.wait_for_timeout(400)
    return ctx, p


JS_HASID = "id=>!!document.getElementById(id)"

with sync_playwright() as pw:
    b = pw.chromium.launch()

    # 1. nav links (desktop)
    ctx, p = load(b, 1440)
    hrefs = p.eval_on_selector_all("#nav a", "els=>els.map(a=>[a.textContent.trim(),a.getAttribute('href')])")
    for txt, h in hrefs:
        ok = h.startswith("#") and len(h) > 1 and p.evaluate(JS_HASID, h[1:])
        rec(f"nav link '{txt}' -> {h} resolves to element id", ok)
    for txt, h in dict.fromkeys((t, h) for t, h in hrefs):
        if h == "#top":
            continue
        p.evaluate("window.scrollTo(0,0)")
        p.wait_for_timeout(150)
        p.click(f'#nav a[href="{h}"] >> nth=0', force=True)
        p.wait_for_timeout(1300)
        top = p.evaluate("id=>document.getElementById(id).getBoundingClientRect().top", h[1:])
        atmax = p.evaluate("Math.abs(scrollY+innerHeight-document.documentElement.scrollHeight)<2")
        rec(f"click nav '{txt}' scrolls target near viewport top (or page bottom reached)", -50 <= top <= 200 or (atmax and 0 <= top < 900),
            f"top={top:.0f}px scrollY={p.evaluate('scrollY')} atPageBottom={atmax}")
    allA = p.eval_on_selector_all(
        "a", "els=>els.map(a=>({t:(a.textContent||a.getAttribute('aria-label')||'').trim().slice(0,30),h:a.getAttribute('href')}))")
    dead = [a for a in allA if a["h"] in ("#", "", None)]
    rec("no dead '#'/empty href anywhere in page (incl. footer/social/legal)", not dead, json.dumps(dead))
    broken = [a for a in allA if a["h"] and a["h"].startswith("#") and len(a["h"]) > 1
              and not p.evaluate(JS_HASID, a["h"][1:])]
    rec("all #anchor hrefs resolve to ids", not broken, json.dumps(broken))
    selfref = []
    for sel in [".hero a.btn", ".link-gold", ".link-dark", ".vbody a", ".ibody a", ".cta a", ".nation a.btn", ".presence a.btn"]:
        for el in p.query_selector_all(sel):
            h = el.get_attribute("href")
            sec = el.evaluate("e=>e.closest('section')&&e.closest('section').id")
            if h == "#" + (sec or "_"):
                selfref.append(f"{sel} '{el.inner_text().strip()[:25]}' -> {h}")
    rec("CTAs/links don't merely point at their own containing section", not selfref, "; ".join(selfref))
    hero = p.eval_on_selector_all(".hero a, .hero button",
                                  "els=>els.map(a=>[a.textContent.trim(),a.getAttribute('href'),a.dataset.modal||''])")
    rec("hero CTAs have href/action", all(h[1] and h[1] != "#" for h in hero), json.dumps(hero))
    ctx.close()

    # 2. mobile menu 390
    ctx, p = load(b, 390, 844)

    def vis():
        return p.evaluate("""(()=>{const n=document.getElementById('nav');const r=n.getBoundingClientRect();
          const s=getComputedStyle(n);return n.classList.contains('open')&&s.visibility!=='hidden'&&s.display!=='none'&&r.height>0})()""")

    def exp():
        return p.get_attribute("#burger", "aria-expanded")

    rec("menu initially closed, aria-expanded=false", exp() == "false" and not vis(), exp())
    p.click("#burger"); p.wait_for_timeout(400)
    rec("burger click opens menu, aria-expanded=true", vis() and exp() == "true", exp())
    p.click("#burger"); p.wait_for_timeout(400)
    rec("burger click closes menu, aria-expanded=false", not vis() and exp() == "false", exp())
    p.click("#burger"); p.wait_for_timeout(300)
    p.keyboard.press("Escape"); p.wait_for_timeout(300)
    rec("Escape closes open mobile menu", not vis() and exp() == "false", f"open={vis()} expanded={exp()}")
    if vis():
        p.click("#burger"); p.wait_for_timeout(300)
    p.click("#burger"); p.wait_for_timeout(400)
    p.click('#nav a[href="#ventures"]'); p.wait_for_timeout(1300)
    rec("nav link click closes menu + aria-expanded=false", not vis() and exp() == "false", f"expanded={exp()}")
    top = p.evaluate("document.getElementById('ventures').getBoundingClientRect().top")
    rec("mobile nav link scrolls to target", -50 <= top <= 200, f"top={top:.0f}")
    ctx.close()

    # 3. modal
    ctx, p = load(b, 1440)

    def mopen():
        return p.evaluate("!document.getElementById('story').hidden")

    def open_m():
        p.click(".watch"); p.wait_for_timeout(250)

    rec("modal initially hidden", not mopen())
    open_m()
    rec("'Watch Our Story' opens modal", mopen())
    rec("focus moves into modal on open (close button)",
        p.evaluate("document.activeElement.classList.contains('modal-close')"), p.evaluate("document.activeElement.className"))
    rec("opening modal doesn't change URL hash (preventDefault)", "#story" not in p.url, p.url)
    p.keyboard.press("Tab"); p.keyboard.press("Tab")
    rec("focus trapped inside modal after Tab x2",
        p.evaluate("document.getElementById('story').contains(document.activeElement)"),
        p.evaluate("document.activeElement.tagName+'.'+document.activeElement.className"))
    p.click(".modal-close"); p.wait_for_timeout(200)
    rec("close button closes modal", not mopen())
    rec("focus returns to trigger after close",
        p.evaluate("document.activeElement.classList.contains('watch')"),
        p.evaluate("document.activeElement.tagName+'.'+document.activeElement.className"))
    open_m(); p.keyboard.press("Escape"); p.wait_for_timeout(200)
    rec("Escape closes modal", not mopen())
    open_m(); p.mouse.click(5, 5); p.wait_for_timeout(200)
    rec("backdrop click closes modal", not mopen())
    open_m()
    box = p.eval_on_selector(".modal-box", "e=>{const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}")
    p.mouse.click(*box); p.wait_for_timeout(200)
    rec("click inside modal box does NOT close modal", mopen())
    p.keyboard.press("Escape")
    ctx.close()

    # 4. carousel
    for w in (1440, 390):
        ctx, p = load(b, w, 900)
        p.evaluate("document.getElementById('carousel').scrollIntoView({block:'center'})"); p.wait_for_timeout(600)
        m = p.evaluate("(()=>{const c=document.getElementById('carousel');return [c.scrollWidth,c.clientWidth]})()")
        sl = lambda: p.evaluate("document.getElementById('carousel').scrollLeft")
        vb = p.is_visible(".car-btn.next")
        fits = m[0] <= m[1] + 1
        if fits:
            # nothing to scroll: both arrows are shown (desktop) but disabled; they must not be clickable
            both_off = p.evaluate("[...document.querySelectorAll('.car-btn')].every(b=>b.disabled)")
            rec(f"carousel arrows disabled when all cards fit @ {w}", both_off, f"scrollWidth/clientWidth={m}")
            if w >= 1400:
                rec(f"carousel arrows visible (disabled state) @ {w}", vb, "next button visible")
            ctx.close(); continue
        if not vb:
            rec(f"carousel arrow buttons visible @ {w}", False, "next/prev buttons not visible; track scrollWidth/clientWidth=%s" % m)
            ctx.close(); continue
        prev_off = p.evaluate("document.querySelector('.car-btn.prev').disabled")
        rec(f"carousel prev disabled at start @ {w}", prev_off, "")
        s0 = sl(); p.click(".car-btn.next"); p.wait_for_timeout(1000); s1 = sl()
        rec(f"carousel next button scrolls track @ {w}", s1 > s0, f"scrollLeft {s0}->{s1}; scrollWidth/clientWidth={m}")
        p.click(".car-btn.prev"); p.wait_for_timeout(1000); s2 = sl()
        rec(f"carousel prev button scrolls track back @ {w}", s2 < s1, f"scrollLeft {s1}->{s2}")
        ctx.close(); continue
        s0 = sl(); p.click(".car-btn.next"); p.wait_for_timeout(1000); s1 = sl()
        rec(f"carousel next button scrolls track @ {w}", s1 > s0, f"scrollLeft {s0}->{s1}; scrollWidth/clientWidth={m}")
        p.click(".car-btn.prev"); p.wait_for_timeout(1000); s2 = sl()
        rec(f"carousel prev button scrolls track back @ {w}", s2 < s1, f"scrollLeft {s1}->{s2}")
        ctx.close()

    # 5. keyboard focus-visible
    ctx, p = load(b, 1440)
    p.mouse.click(1, 1)
    seen, bad = [], []
    for i in range(45):
        p.keyboard.press("Tab")
        info = p.evaluate("""(()=>{const e=document.activeElement;if(!e||e===document.body)return null;const s=getComputedStyle(e);
          const r=e.getBoundingClientRect();
          return {t:e.tagName+'.'+(typeof e.className==='string'?e.className:'')+' '+(e.textContent||e.getAttribute('aria-label')||'').trim().slice(0,22),
          ow:s.outlineWidth,os:s.outlineStyle,bs:s.boxShadow,vis:r.width>0&&r.height>0&&s.visibility!=='hidden',fv:e.matches(':focus-visible')}})()""")
        if not info:
            continue
        seen.append(info)
        has = (info["os"] not in ("none", "hidden") and info["ow"] != "0px") or info["bs"] != "none"
        if info["vis"] and not has:
            bad.append(info["t"] + f" outline={info['os']} {info['ow']} shadow={info['bs']}")
    rec("Tab focus-visible indicator on every focused visible link/button", not bad and len(seen) > 5,
        f"tabbed {len(seen)} elems; missing: {bad}")
    ctx.close()

    # 6. overflow
    for w in (320, 390, 517, 820, 1024, 1440):
        ctx, p = load(b, w, 900)
        p.wait_for_timeout(300)
        o = p.evaluate("""(()=>{const d=document.documentElement;const vw=d.clientWidth;
          const offenders=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>vw+1&&!e.closest('.carousel')&&!e.closest('#nav')&&getComputedStyle(e).position!=='fixed'}).slice(0,5).map(e=>e.tagName+'.'+e.className+' right='+Math.round(e.getBoundingClientRect().right));
          return {sw:d.scrollWidth,vw,bsw:document.body.scrollWidth,offenders}})()""")
        rec(f"no horizontal overflow @ {w}px", o["sw"] <= o["vw"] and o["bsw"] <= o["vw"], json.dumps(o))
        ctx.close()

    # 7. console / network / images
    for w in (390, 517, 1440):
        errs, fails = [], []
        ctx, p = load(b, w, 900, errs, fails)
        h = p.evaluate("document.documentElement.scrollHeight")
        for y in range(0, h, 500):
            p.evaluate(f"window.scrollTo(0,{y})"); p.wait_for_timeout(120)
        p.wait_for_timeout(600)
        rec(f"console errors/warnings @ {w}", not errs, errs)
        rec(f"failed requests / HTTP>=400 @ {w}", not fails, fails)
        imgs = p.evaluate("[...document.images].map(i=>({s:i.getAttribute('src'),ok:i.complete&&i.naturalWidth>0}))")
        badi = [i["s"] for i in imgs if not i["ok"]]
        rec(f"all {len(imgs)} <img> loaded @ {w} (after scroll)", not badi, badi)
        ctx.close()
    b.close()

srv.shutdown()
n = sum(1 for r in RESULTS if not r[1])
print(f"\nTOTAL {len(RESULTS)} checks, {n} FAILED")
json.dump(RESULTS, open(os.path.join(ROOT, "artifacts", "tools", "functional-results.json"), "w"), indent=1)

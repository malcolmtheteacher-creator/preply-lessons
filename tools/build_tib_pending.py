#!/usr/bin/env python3
"""Build the PENDING 'Think Inside the Box' lessons (tools nodes on the mind map that have no lesson yet).

  tools/tib_content_pending/NN_<slug>.json  ->  tib_<slug>_b2.html   (one lesson each)

Uses build_tib.py's own template, CSS, JS, page parts and checks, so the pages are identical in
style to the existing lessons.  It ONLY writes the new lesson files: it does not touch the
dashboard, toolbox, chooser, the mind-map hotspots or any existing lesson.  Extra diagram types
needed by the new tools (venn, hype, mindmap, forces, widepyramid) are registered here, so
build_tib.py itself is unchanged.
Usage: python3 tools/build_tib_pending.py
"""
import glob, json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_tib as B  # noqa: E402

PENDING = os.path.join(B.HERE, "tib_content_pending")
INK, TEAL, LIGHT, TONES, svg_text = B.INK, B.TEAL, B.LIGHT, B.TONES, B.svg_text
ARROW = (f'<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">'
         f'<path d="M0,0 L8,4 L0,8 z" fill="{TEAL}"/></marker></defs>')


def d_widepyramid(d):
    levels = d["levels"]  # top first
    n, W, T, LH = len(levels), 560, 10, 56
    H = LH * n + 30
    step = (W - 60) / n
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" xmlns="http://www.w3.org/2000/svg" role="img">']
    tones = d.get("tones", ["b", "t", "g", "y", "r", "n"])
    for i, lab in enumerate(levels):
        y0, y1 = T + i * LH, T + (i + 1) * LH
        w0, w1 = i * step, (i + 1) * step
        if i == 0:
            pts = f"{W/2},{y0} {W/2 + w1/2:.1f},{y1} {W/2 - w1/2:.1f},{y1}"
        else:
            pts = f"{W/2 - w0/2:.1f},{y0} {W/2 + w0/2:.1f},{y0} {W/2 + w1/2:.1f},{y1} {W/2 - w1/2:.1f},{y1}"
        out.append(f'<polygon points="{pts}" fill="{TONES[tones[i % len(tones)]]}" stroke="white" stroke-width="3"/>')
        top_off = (12 if "|" not in lab else 8) if i == 0 else 0
        out.append(svg_text(W / 2, (y0 + y1) / 2 + top_off, lab, 12 if i == 0 else 13, "600"))
    if d.get("side"):
        out.append(f'<line x1="14" y1="{T + LH * n}" x2="14" y2="{T + 4}" stroke="{TEAL}" stroke-width="2" marker-end="url(#ar)"/>')
        out.insert(1, ARROW)
        out.append(svg_text(30, T + LH * n / 2, d["side"], 12, "700", TEAL, rotate=-90))
    out.append("</svg>")
    return "".join(out)


def d_venn(d):
    a, b = d["sets"]
    W, H, cy, r = 600, 330, 160, 125
    xa, xb = 225, 375
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" xmlns="http://www.w3.org/2000/svg" role="img">',
           f'<rect x="8" y="8" width="{W - 16}" height="{H - 16}" rx="12" fill="{TONES["n"]}" stroke="#c5e6e1"/>',
           f'<circle cx="{xa}" cy="{cy}" r="{r}" fill="{TONES["t"]}" fill-opacity="0.75" stroke="{TEAL}" stroke-width="2"/>',
           f'<circle cx="{xb}" cy="{cy}" r="{r}" fill="{TONES["b"]}" fill-opacity="0.6" stroke="{TEAL}" stroke-width="2"/>']
    out.append(svg_text(xa - 40, 54, a, 15, "700", TEAL))
    out.append(svg_text(xb + 40, 54, b, 15, "700", TEAL))
    out.append(svg_text(xa - 50, cy, d["left"], 13, "600"))
    out.append(svg_text(xb + 50, cy, d["right"], 13, "600"))
    out.append(svg_text(W / 2, cy, d["both"], 13, "700"))
    if d.get("outside"):
        out.append(svg_text(W - 24, H - 24, d["outside"], 11, "600", "#556", "end"))
    out.append("</svg>")
    return "".join(out)


def d_hype(d):
    W, H, L, B_ = 640, 340, 60, 270
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" xmlns="http://www.w3.org/2000/svg" role="img">', ARROW]
    def f(x):
        t = (x - L) / (W - L - 30)
        peak = 190 * math.exp(-((t - 0.22) / 0.085) ** 2)
        slope = 105 / (1 + math.exp(-(t - 0.66) / 0.07))
        return B_ - 8 - peak - slope * (1 if t > 0.3 else (t / 0.3) ** 3)
    pts = " ".join(f"{x},{f(x):.1f}" for x in range(L, W - 29, 4))
    out.append(f'<polyline points="{pts}" fill="none" stroke="{TEAL}" stroke-width="3.5"/>')
    out.append(f'<line x1="{L}" y1="{B_}" x2="{W - 20}" y2="{B_}" stroke="{TEAL}" stroke-width="2" marker-end="url(#ar)"/>')
    out.append(f'<line x1="{L}" y1="{B_}" x2="{L}" y2="18" stroke="{TEAL}" stroke-width="2" marker-end="url(#ar)"/>')
    out.append(svg_text((W + L) / 2, B_ + 50, d.get("x", "Time"), 14, "700", TEAL))
    out.append(svg_text(26, B_ / 2 + 10, d.get("y", "Expectations"), 14, "700", TEAL, rotate=-90))
    xs = [0.07, 0.22, 0.42, 0.64, 0.9]
    for i, (lab, t) in enumerate(zip(d["phases"], xs)):
        x = L + t * (W - L - 30)
        y = f(x)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{INK}"/>')
        out.append(f'<line x1="{x:.1f}" y1="{y + 6:.1f}" x2="{x:.1f}" y2="{B_}" stroke="#9fb" stroke-dasharray="3 4"/>')
        ly = B_ + 22 if i % 2 == 0 else B_ + 22
        out.append(svg_text(x, ly, lab, 11, "600", INK))
    out.append("</svg>")
    return "".join(out)


def d_mindmap(d):
    br = d["branches"]  # [[label, [sub, sub]], ...]
    W, H, cx, cy = 640, 400, 320, 200
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" xmlns="http://www.w3.org/2000/svg" role="img">']
    tones = ["t", "y", "b", "g", "r", "n"]
    n = len(br)
    for i, (lab, subs) in enumerate(br):
        a = -math.pi / 2 + (i + 0.5) * 2 * math.pi / n
        x, y = cx + 165 * math.cos(a), cy + 120 * math.sin(a)
        out.append(f'<path d="M{cx},{cy} Q{cx + 90*math.cos(a - 0.35):.1f},{cy + 70*math.sin(a - 0.35):.1f} {x:.1f},{y:.1f}" fill="none" stroke="{TEAL}" stroke-width="5" stroke-linecap="round"/>')
        for j, s in enumerate(subs):
            aa = a + (j - (len(subs) - 1) / 2) * 0.42
            sx, sy = x + 70 * math.cos(aa), y + 48 * math.sin(aa)
            out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{sx:.1f}" y2="{sy:.1f}" stroke="{TEAL}" stroke-width="2"/>')
            c = math.cos(aa)
            anchor = "start" if c > 0.3 else ("end" if c < -0.3 else "middle")
            tx = sx + (4 if anchor == "start" else -4 if anchor == "end" else 0)
            ty = sy + (12 * math.sin(aa) if anchor == "middle" else 0)
            out.append(svg_text(tx, ty, s, 11, "400", INK, anchor))
        out.append(f'<rect x="{x - 52:.1f}" y="{y - 15:.1f}" width="104" height="30" rx="14" fill="{TONES[tones[i % 6]]}" stroke="{TEAL}"/>')
        out.append(svg_text(x, y, lab, 13, "700"))
    out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="70" ry="36" fill="{LIGHT}" stroke="{TEAL}" stroke-width="3"/>')
    out.append(svg_text(cx, cy, d["centre"], 14, "700", TEAL))
    out.append("</svg>")
    return "".join(out)


def d_forces(d):
    W, H, cx, cy = 600, 380, 300, 190
    out = [f'<svg viewBox="0 0 {W} {H}" width="{W}" xmlns="http://www.w3.org/2000/svg" role="img">', ARROW]
    boxes = [(cx, 42, d["top"]), (cx + 205, cy, d["right"]), (cx, H - 42, d["bottom"]), (cx - 205, cy, d["left"])]
    ends = [(cx, cy - 52), (cx + 92, cy), (cx, cy + 52), (cx - 92, cy)]
    starts = [(cx, 70), (cx + 205 - 82, cy), (cx, H - 70), (cx - 205 + 82, cy)]
    for (bx, by, lab), (sx, sy), (ex, ey) in zip(boxes, starts, ends):
        out.append(f'<line x1="{sx}" y1="{sy}" x2="{ex}" y2="{ey}" stroke="{TEAL}" stroke-width="3" marker-end="url(#ar)"/>')
        out.append(f'<rect x="{bx - 80}" y="{by - 27}" width="160" height="54" rx="10" fill="{LIGHT}" stroke="{TEAL}" stroke-width="2"/>')
        out.append(svg_text(bx, by, lab, 13, "700"))
    out.append(f'<rect x="{cx - 90}" y="{cy - 50}" width="180" height="100" rx="12" fill="{TONES["y"]}" stroke="{INK}" stroke-width="2"/>')
    out.append(svg_text(cx, cy, d["centre"], 14, "700"))
    out.append("</svg>")
    return "".join(out)


B.DIAGRAMS.update({"widepyramid": d_widepyramid, "venn": d_venn, "hype": d_hype,
                   "mindmap": d_mindmap, "forces": d_forces})


def main():
    existing = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(B.CONTENT, "*.json")))]
    pending = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(PENDING, "*.json")))]
    tb = json.load(open(os.path.join(B.HERE, "tib_toolbox.json")))
    B.CHECK_NAMES = {t["name"] for f in tb["families"] for t in f["tools"]}
    order = existing + pending  # so the prev/next strip continues the series
    for d in pending:
        B.check(d, "B2")
        out = os.path.join(B.ROOT, f'tib_{d["slug"]}_b2.html')
        open(out, "w").write(B.lesson(d, order, "B2", ()))
        print(f"  wrote {os.path.basename(out)}  ({os.path.getsize(out)//1024}KB)")


if __name__ == "__main__":
    main()

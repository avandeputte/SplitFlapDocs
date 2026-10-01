#!/usr/bin/env python3
"""Import the GitHub wiki into docs/ and build the nav from the wiki's sidebar.

    python3 tools/import_wiki.py /path/to/SplitFlapGateway.wiki

Pages keep their wiki names, so every URL on the site mirrors the wiki's. Wiki links
([Text](Page-Name) and [Text](Page-Name#anchor)) become Markdown links to the page files;
Home becomes index.md; images are copied alongside. The nav in mkdocs.yml is regenerated
from _Sidebar.md between the two marker lines.
"""
import pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CFG  = ROOT / "mkdocs.yml"

def main(wiki):
    wiki = pathlib.Path(wiki)
    pages = {p.stem for p in wiki.glob("*.md") if not p.name.startswith("_")}
    def target(name):
        return "index.md" if name == "Home" else f"{name}.md"
    link = re.compile(r'\]\(([A-Za-z0-9][A-Za-z0-9_.\-]*)(#[^)\s]*)?\)')
    def fix(m):
        name, anchor = m.group(1), m.group(2) or ""
        if name in pages:
            return f"]({target(name)}{slug(anchor)})"
        return m.group(0)
    # GitHub keeps a double hyphen where an em dash sat in a heading ("Option A -- Nudge"
    # becomes #option-a--nudge); Python-Markdown collapses the run. Normalise the anchors.
    def slug(anchor):
        return re.sub(r'-{2,}', '-', anchor)
    same = re.compile(r'\]\((#[^)\s]+)\)')
    n = 0
    for p in wiki.glob("*.md"):
        if p.name.startswith("_"):
            continue
        text = link.sub(fix, p.read_text(encoding="utf-8"))
        text = same.sub(lambda m: f"]({slug(m.group(1))})", text)
        (DOCS / target(p.stem)).write_text(text, encoding="utf-8")
        n += 1
    for img in list(wiki.glob("*.png")) + list(wiki.glob("*.jpg")) + list(wiki.glob("*.jpeg")) + list(wiki.glob("*.svg")):
        shutil.copy2(img, DOCS / img.name)
    # nav from the sidebar
    nav = ["nav:", "  - Home: index.md"]
    section = None
    for line in (wiki / "_Sidebar.md").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        sm = re.match(r'^\*\*(.+?)\*\*$', line)
        im = re.match(r'^- \[(.+?)\]\(([^)#]+)\)$', line)
        if sm and sm.group(1) != "[SplitFlap wiki](Home)":
            section = sm.group(1); nav.append(f"  - {section}:")
        elif im and section and im.group(2) in pages:
            nav.append(f"      - {im.group(1)}: {target(im.group(2))}")
    cfg = CFG.read_text(encoding="utf-8")
    a, b = "# --- nav: generated from the wiki sidebar by tools/import_wiki.py ---", "# --- end nav ---"
    assert a in cfg and b in cfg, "nav markers missing from mkdocs.yml"
    cfg = cfg[:cfg.index(a)] + a + "\n" + "\n".join(nav) + "\n" + cfg[cfg.index(b):]
    CFG.write_text(cfg, encoding="utf-8")
    print(f"imported {n} pages, nav rebuilt")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../SplitFlapGateway.wiki")

#!/usr/bin/env python3
"""Render docs/notebooks/*.ipynb to HTML pages that match the QMLearn site chrome."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

import mistune
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer, get_lexer_by_name

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "docs" / "notebooks"

PAGES = [
    {
        "stem": "create_training",
        "title": "Creating a training data set",
        "blurb": "Sample geometries, run PySCF, and write an HDF5 training database.",
    },
    {
        "stem": "rdm_training",
        "title": "1-RDM and 2-RDM learning / training",
        "blurb": "Unified fitting of γ, δγ, Γ, Γ<sup>c</sup>, and Δ, with hyperparameter search and PEC plots.",
    },
    {
        "stem": "aimd_1rdm",
        "title": "1-RDM AIMD",
        "blurb": "NVE dynamics for water using a machine-learned 1-RDM (method='gamma').",
    },
    {
        "stem": "aimd_2rdm_gamma2c",
        "title": "2-RDM AIMD (Γ<sup>c</sup>)",
        "blurb": "NVE dynamics from the correlated 2-RDM Γ<sup>c</sup> (method='gamma2').",
    },
    {
        "stem": "aimd_2rdm_cumulant",
        "title": "2-RDM AIMD (cumulant Δ)",
        "blurb": "NVE dynamics from δγ plus the cumulant Δ (method='gamma2cum').",
    },
]

markdown = mistune.create_markdown(
    escape=False,
    plugins=["strikethrough", "table", "url"],
)

try:
    LEXER = get_lexer_by_name("ipython3")
except Exception:
    LEXER = Python3Lexer()

FORMATTER = HtmlFormatter(nowrap=True)


def join_source(source) -> str:
    if isinstance(source, list):
        return "".join(source)
    return source or ""


def highlight_python(code: str) -> str:
    return highlight(code, LEXER, FORMATTER)


def render_markdown(source: str) -> str:
    return f'<div class="nb-markdown">{markdown(source)}</div>'


def render_code(cell: dict) -> str:
    source = join_source(cell.get("source"))
    count = cell.get("execution_count")
    prompt = f"In&nbsp;[{count}]:" if count else "In&nbsp;[&nbsp;]:"
    highlighted = highlight_python(source.rstrip("\n"))
    parts = [
        '<div class="nb-cell nb-code">',
        f'<div class="nb-prompt" aria-hidden="true">{prompt}</div>',
        '<div class="nb-source">',
        f'<pre><code class="nb-highlight">{highlighted}</code></pre>',
        "</div>",
        "</div>",
    ]
    outputs = render_outputs(cell.get("outputs") or [], cell.get("execution_count"))
    if outputs:
        parts.append(outputs)
    return "\n".join(parts)


def render_outputs(outputs: list, execution_count) -> str:
    chunks = []
    for output in outputs:
        kind = output.get("output_type")
        if kind == "stream":
            text = html.escape(join_source(output.get("text")))
            name = output.get("name") or "stdout"
            chunks.append(
                f'<pre class="nb-stream nb-stream-{html.escape(name)}">{text}</pre>'
            )
        elif kind in ("display_data", "execute_result"):
            chunks.append(render_data(output.get("data") or {}, execution_count if kind == "execute_result" else None))
        elif kind == "error":
            tb = html.escape("\n".join(output.get("traceback") or []))
            chunks.append(f'<pre class="nb-error">{tb}</pre>')
    chunks = [c for c in chunks if c]
    if not chunks:
        return ""
    prompt = ""
    if execution_count and any(o.get("output_type") == "execute_result" for o in outputs):
        prompt = f'<div class="nb-prompt" aria-hidden="true">Out[{execution_count}]:</div>'
    return (
        '<div class="nb-output">'
        + prompt
        + '<div class="nb-output-body">'
        + "\n".join(chunks)
        + "</div></div>"
    )


def render_data(data: dict, execution_count) -> str:
    if "image/png" in data:
        b64 = join_source(data["image/png"]).replace("\n", "")
        return f'<img class="nb-figure" alt="Notebook figure" src="data:image/png;base64,{b64}">'
    if "image/jpeg" in data:
        b64 = join_source(data["image/jpeg"]).replace("\n", "")
        return f'<img class="nb-figure" alt="Notebook figure" src="data:image/jpeg;base64,{b64}">'
    if "text/html" in data:
        return f'<div class="nb-html">{join_source(data["text/html"])}</div>'
    if "text/plain" in data:
        text = html.escape(join_source(data["text/plain"]))
        return f'<pre class="nb-plain">{text}</pre>'
    return ""


def render_cells(nb: dict) -> str:
    blocks = []
    for cell in nb.get("cells") or []:
        ctype = cell.get("cell_type")
        if ctype == "markdown":
            blocks.append(render_markdown(join_source(cell.get("source"))))
        elif ctype == "code":
            blocks.append(render_code(cell))
        elif ctype == "raw":
            blocks.append(f'<pre class="nb-plain">{html.escape(join_source(cell.get("source")))}</pre>')
    return "\n".join(blocks)


def strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def page_html(meta: dict, body: str) -> str:
    stem = meta["stem"]
    title = meta["title"]
    blurb = meta["blurb"]
    plain_title = strip_tags(title)
    plain_blurb = strip_tags(blurb)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(plain_title)}: QMLearn</title>
  <meta name="description" content="{html.escape(plain_blurb)}">
  <link rel="icon" href="../_static/qmlearn.ico" sizes="any">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body data-page="tutorials" data-root="../">

  <section class="page-hero">
    <div class="container">
      <div class="page-hero-inner">
        <div class="crumbs"><a href="../index.html">Home</a> <span>/</span> <a href="../tutorials.html">Tutorials</a> <span>/</span> {html.escape(stem)}</div>
        <h1>{title}</h1>
        <p>{blurb} Open this page as a rendered notebook, or <a href="{html.escape(stem)}.ipynb" download>download {html.escape(stem)}.ipynb</a> and run it locally after you <a href="../install.html">install QMLearn</a>.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container notebook">
{body}
    </div>
  </section>

  <script src="../assets/js/main.js" defer></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}], ignoredTags: ['script','noscript','style','textarea','pre','code']}});"></script>
</body>
</html>
"""


def main() -> None:
    for meta in PAGES:
        ipynb = NB_DIR / f"{meta['stem']}.ipynb"
        nb = json.loads(ipynb.read_text(encoding="utf-8"))
        html_path = NB_DIR / f"{meta['stem']}.html"
        html_path.write_text(page_html(meta, render_cells(nb)), encoding="utf-8")
        print(f"wrote {html_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

"""
para_utils.py — Safe paragraph-level manipulation for DOCX document.xml files.

The core problem this solves:
    Splitting document.xml by `<w:p>` includes the `<w:sectPr>` and closing
    `</w:body></w:document>` tags inside the LAST paragraph chunk. If you then
    remove or insert after that chunk, you either lose the closing structure
    (causing "Premature end of data") or append content after </w:document>
    (causing "Extra content at end of document").

Safe pattern:
    1. split_doc()  — separates body paragraphs from the sectPr tail
    2. operate on paras list freely (insert, remove, modify)
    3. join_doc()   — always re-appends the tail correctly

Usage (in an edit script):
    import sys
    sys.path.insert(0, 'scripts')
    from para_utils import split_doc, join_doc, text_of, xe, arial_run, arial_run_simple, rebuild_para

    with open('unpacked/word/document.xml', 'r', encoding='utf-8') as f:
        content = f.read()

    paras, tail = split_doc(content)

    # Step 1: inspect to find the right indices (or run CLI: see below)
    for i, p in enumerate(paras):
        t = text_of(p)
        if t.strip():
            print(f'[{i}] {t[:80]}')

    # Step 2: modify by index — no fragile text-fragment search needed
    paras[4]  = rebuild_para(paras[4],  arial_run_simple('New branding statement...'))
    paras[10] = rebuild_para(paras[10], arial_bold('Category: ') + arial_run('body text...'))
    paras[17] = rebuild_para(paras[17], arial_run('New bullet text.'))

    # remove a paragraph
    paras.pop(33)

    # insert a page break before paragraph N
    paras.insert(20, page_break_para())

    new_content = join_doc(paras, tail)
    with open('unpacked/word/document.xml', 'w', encoding='utf-8') as f:
        f.write(new_content)

CLI usage:
    # List all paragraphs with index, style, char count, and text preview:
    python scripts/para_utils.py list unpacked/word/document.xml

    # Show full XML of a specific paragraph:
    python scripts/para_utils.py get unpacked/word/document.xml 17

    # Show total character count (useful for page-length budgeting):
    python scripts/para_utils.py chars unpacked/word/document.xml

IMPORTANT — paras[0] is the XML header (<w:document><w:body>), not a paragraph.
The first real paragraph is paras[1]. The list command marks the header as [0]*.
"""

import re


# ---------------------------------------------------------------------------
# Core split / join
# ---------------------------------------------------------------------------

def split_doc(content: str) -> tuple[list[str], str]:
    """
    Split document.xml into (paras, tail).

    paras — list of strings, each starting with <w:p (or the pre-paragraph
            header for index 0, which contains the XML declaration and <w:body>)
    tail  — everything from <w:sectPr> to end of file, i.e.
            "<w:sectPr ...>...</w:sectPr></w:body></w:document>"

    The sectPr is REMOVED from the paragraph list so paragraph operations
    (insert / remove) never corrupt the closing document structure.
    """
    sectpr_idx = content.find('<w:sectPr')
    if sectpr_idx == -1:
        raise ValueError(
            "No <w:sectPr> found in document.xml. "
            "File may be corrupt or not a standard OOXML document."
        )
    body = content[:sectpr_idx]
    tail = content[sectpr_idx:]

    # Verify tail ends properly
    if not tail.rstrip().endswith('</w:document>'):
        raise ValueError(
            "Document does not end with </w:document>. "
            "File may already be corrupt — inspect manually."
        )

    paras = re.split(r'(?=<w:p[ >])', body)
    return paras, tail


def join_doc(paras: list[str], tail: str) -> str:
    """Rejoin paragraphs and re-append the sectPr tail."""
    return ''.join(paras) + tail


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

def text_of(para: str) -> str:
    """Return all plain text content from a paragraph's <w:t> elements."""
    return ''.join(re.findall(r'<w:t[^>]*>([^<]+)</w:t>', para))


# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------

def xe(s: str) -> str:
    """XML-escape a string for use inside a <w:t> element."""
    return (s
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def arial_run(text: str, bold: bool = False) -> str:
    """
    Build a single Arial run (with eastAsiaTheme, as used in body bullets).
    Set bold=True for bold runs (e.g. KA titles, skill category labels).
    """
    b = '<w:b/><w:bCs/>' if bold else ''
    return (
        f'<w:r>'
        f'<w:rPr>'
        f'<w:rFonts w:ascii="Arial" w:eastAsiaTheme="minorEastAsia" w:hAnsi="Arial" w:cs="Arial"/>'
        f'{b}'
        f'<w:sz w:val="20"/><w:szCs w:val="20"/>'
        f'</w:rPr>'
        f'<w:t xml:space="preserve">{xe(text)}</w:t>'
        f'</w:r>'
    )


def arial_run_simple(text: str) -> str:
    """
    Build a single Arial run WITHOUT eastAsiaTheme.
    Used for the Summary/branding paragraph which uses the simpler rPr variant.
    """
    return (
        f'<w:r>'
        f'<w:rPr>'
        f'<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>'
        f'<w:sz w:val="20"/><w:szCs w:val="20"/>'
        f'</w:rPr>'
        f'<w:t xml:space="preserve">{xe(text)}</w:t>'
        f'</w:r>'
    )


def get_ppr(para: str) -> str:
    """Extract the <w:pPr>...</w:pPr> block from a paragraph, or '' if absent."""
    m = re.search(r'(<w:pPr>.*?</w:pPr>)', para, re.DOTALL)
    return m.group(1) if m else ''


def rebuild_para(para: str, new_runs_xml: str) -> str:
    """
    Replace all run content in a paragraph with new_runs_xml, preserving
    the opening tag and <w:pPr> exactly.

    Args:
        para:         The original paragraph XML string.
        new_runs_xml: One or more <w:r>...</w:r> elements as a string.

    Returns:
        A new <w:p>...</w:p> string with the original pPr and new runs.
    """
    ppr = get_ppr(para)
    open_tag_m = re.match(r'(<w:p[^>]*>)', para)
    open_tag = open_tag_m.group(1) if open_tag_m else '<w:p>'
    return f'{open_tag}{ppr}{new_runs_xml}</w:p>'


def arial_bold(text: str) -> str:
    """
    Convenience alias: bold Arial run. Same as arial_run(text, bold=True).
    Use for skill category labels, KA titles, etc.
    """
    return arial_run(text, bold=True)


def page_break_para() -> str:
    """Return a minimal paragraph containing only a page break."""
    return (
        '<w:p>'
        '<w:pPr><w:spacing w:line="240" w:lineRule="auto"/></w:pPr>'
        '<w:r><w:br w:type="page"/></w:r>'
        '</w:p>'
    )


def clean_para(para: str) -> str:
    """
    Strip any trailing <w:sectPr> and document-closing tags from a paragraph.
    Useful when copying paragraphs verbatim from a baseline document where the
    last paragraph may contain the sectPr.
    """
    sectpr_pos = para.find('<w:sectPr')
    if sectpr_pos != -1:
        # Ensure we close the <w:p> tag properly
        if not para[:sectpr_pos].rstrip().endswith('</w:p>'):
            para = para[:sectpr_pos] + '</w:p>'
        else:
            para = para[:sectpr_pos]
    return para


# ---------------------------------------------------------------------------
# Inspection helpers
# ---------------------------------------------------------------------------

def list_paras(content: str) -> list[dict]:
    """
    Return a list of dicts describing each entry in split_doc(content).

    Keys per entry:
        idx     — index in the paras list (use this in paras[idx])
        style   — paragraph style (e.g. 'normal', 'Title', 'ListBullet') or '' for header
        chars   — character count of visible text
        bold    — True if paragraph contains any bold runs
        text    — full visible text (for preview / searching)
        is_header — True for paras[0] (the XML preamble, not a real paragraph)
    """
    paras, _ = split_doc(content)
    result = []
    for i, p in enumerate(paras):
        if i == 0:
            result.append(dict(idx=0, style='', chars=0, bold=False, text='', is_header=True))
            continue
        style_m = re.search(r'<w:pStyle w:val="([^"]+)"', p)
        style = style_m.group(1) if style_m else 'normal'
        t = text_of(p)
        bold = bool(re.search(r'<w:b[ /]', p))
        result.append(dict(idx=i, style=style, chars=len(t), bold=bold, text=t, is_header=False))
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _out(msg: str) -> None:
    import sys
    sys.stdout.buffer.write((msg + '\n').encode('utf-8', errors='replace'))


def main():
    import sys

    def usage():
        _out("Usage:")
        _out("  python scripts/para_utils.py list  <xml_path>          # list all paragraphs")
        _out("  python scripts/para_utils.py get   <xml_path> <idx>    # print XML of paragraph N")
        _out("  python scripts/para_utils.py chars <xml_path>          # total char count")
        sys.exit(1)

    if len(sys.argv) < 3:
        usage()

    cmd, xml_path = sys.argv[1], sys.argv[2]

    with open(xml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if cmd == 'list':
        entries = list_paras(content)
        for e in entries:
            if e['is_header']:
                _out(f"[{e['idx']:3d}]* (XML header)")
                continue
            style = e['style'][:10].ljust(10)
            b = 'B' if e['bold'] else ' '
            preview = e['text'][:80].replace('\n', ' ')
            _out(f"[{e['idx']:3d}] [{style}] {b} ({e['chars']:4d}): {preview}")

    elif cmd == 'get':
        if len(sys.argv) < 4:
            usage()
        idx = int(sys.argv[3])
        paras, _ = split_doc(content)
        if idx < 0 or idx >= len(paras):
            _out(f"Index {idx} out of range (0..{len(paras)-1})")
            sys.exit(1)
        _out(paras[idx])

    elif cmd == 'chars':
        entries = list_paras(content)
        total = sum(e['chars'] for e in entries)
        para_count = sum(1 for e in entries if not e['is_header'] and e['chars'] > 0)
        _out(f"Total chars : {total}")
        _out(f"Non-empty paragraphs: {para_count}")

    else:
        usage()


if __name__ == '__main__':
    main()

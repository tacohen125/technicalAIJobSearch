# XML Editing Guide

## Table of Contents
- [Formatting Rules](#formatting-rules)
- [Baseline Patterns](#baseline-patterns)
- [Baseline Structure](#baseline-structure)
- [Section-Specific Formatting](#section-specific-formatting)
- [Content Reduction Strategy](#content-reduction-strategy)
- [XML Editing Examples](#xml-editing-examples)
- [Common Pitfalls](#common-pitfalls)
- [Troubleshooting](#troubleshooting)

## Formatting Rules

**NEVER change these elements from the baseline:**

### Spacing
- Line spacing: `<w:spacing w:line="..." w:lineRule="..."/>` — preserve exact values
- Paragraph spacing before/after: `w:before`, `w:after` — preserve or omit as baseline does
- Line rule: `w:lineRule` (typically `"auto"`) — never change

### Indentation
- `<w:ind w:left="..." w:right="..." w:hanging="..." w:firstLine="..."/>` — preserve all values exactly
- Negative indentation values (e.g., `left="-360"`) are intentional — do not "fix" them

### Paragraph Properties (`<w:pPr>`)
- `<w:widowControl/>` — preserve as-is
- `<w:jc w:val="..."/>` — justification/alignment, never change
- `<w:pStyle w:val="..."/>` — paragraph style references, never change
- `<w:keepNext/>` and `<w:keepLines/>` — page break control, preserve if present

### Run Properties (`<w:rPr>`)
- `<w:rFonts .../>` — font family specifications, never change
- `<w:sz w:val="..."/>` and `<w:szCs w:val="..."/>` — font size, never change
- `<w:b w:val="..."/>` — bold, only modify when content strategy requires it
- `<w:i w:val="..."/>` — italic, preserve unless content strategy requires change
- `<w:u w:val="..."/>` — underline, preserve unless content strategy requires change
- `<w:color w:val="..."/>` — text color, never change

### Numbering and Bullets
- `<w:numPr>` containing `<w:ilvl>` and `<w:numId>` — preserve exact IDs and levels
- When adding new bulleted items, copy `<w:numPr>` from an adjacent bullet of the same type

### Tabs
- `<w:tab/>` elements within runs — preserve for right-alignment in company/title lines
- `<w:tabs>` definitions in paragraph properties — never change

### Page Layout
- `<w:pgSz>` — page size, never change
- `<w:pgMar>` — page margins, never change
- `<w:sectPr>` — section properties, never change

### General Rule
Only modify text content within `<w:t>` tags. When `<w:t xml:space="preserve">` is used, maintain the `xml:space` attribute. If splitting or merging runs, preserve the `<w:rPr>` from the original run(s).

## Baseline Patterns

- Headers like "Areas of Expertise", "Technical Skills", "Key Accomplishments", "Experience", "Education": NOT all caps
- Line spacing: typically 228-240 for body, 276 for headers
- Indents: -360 left/right for non-bullets, 0 left with 360 hanging for bullets
- Tabs: `<w:tab/>` used for right-alignment in company/title lines
- Bold: Only on branding headline and first few impactful words of each Key Accomplishments bullet
- Areas of Expertise and Technical Skills: Plain text with pipe separators, NOT bulleted

## Baseline Structure

**Resume sections in order:**
1. Header (Name, contact info, LinkedIn)
2. Branding Title (bold, no header, 1-2 lines)
3. Branding Statement (no header, 3-4 sentences, regular text)
4. Areas of Expertise (header + up to 4 lines of pipe-separated expertise areas)
5. Technical Skills (header + up to 2 lines of pipe-separated skills, NOT bulleted)
6. Key Accomplishments (header + 3 bulleted items, first words bold)
7. Experience (header + positions with company/title/bullets)
8. Education (header + institution line [bold name, regular location] + degree line [underlined])

**Key spacing values:**
- Headers: `line="276"`
- Body paragraphs: `line="228"` or `line="229"`
- Contact info: `line="240"`
- Most paragraphs: NO `before` or `after` spacing (relies on line spacing)

**Key indentation patterns:**
- Non-bullets: `left="-360" right="-360" firstLine="0"`
- Bullets: `left="0" right="-360" hanging="360"`

## Section-Specific Formatting

### Branding Title
- Located immediately after LinkedIn URL
- Bold formatting: `<w:b w:val="1"/>` and `<w:bCs w:val="1"/>`
- Typically 1-2 lines describing target role/title
- No section header

### Branding Statement
- Located immediately after Branding Title
- Regular text (not bold)
- 3-4 sentences maximum
- No section header

### Key Accomplishments
- Section header: "Key Accomplishments" (NOT all caps)
- Each accomplishment: first few words bold (`<w:b w:val="1"/>`), rest regular
- Use bullet formatting (`<w:numPr>` with appropriate `<w:numId>`)

### Areas of Expertise
- Section header: "Areas of Expertise" (NOT all caps)
- Format: Up to 4 lines of pipe-separated expertise areas
- Example: `Strategic Planning & Execution | Cross-functional Collaboration | Technical Program Management`
- NOT bulleted (plain paragraphs with standard `w:ind` attributes)
- Regular text formatting (no bold)

### Technical Skills
- Section header: "Technical Skills" (NOT all caps)
- Format: Up to 2 lines of pipe-separated tools and technical skills (NOT bulleted)
- Example: `Google Workspace | Microsoft Office Suite | Asana | Airtable | Jira | Python | SQL | HTML/CSS`
- Contains mixed content: enterprise tools, project management platforms, programming languages
- NOT bulleted (plain paragraphs with standard `w:ind` attributes)
- Regular text formatting (no bold)
- Tailor by reordering items and adding/removing based on job requirements

### Experience
- Section header: "Experience" (NOT all caps)
- Company line: **Company Name**[TAB]Location (company name bold, location regular)
- Title line: Job Title[TAB]Dates (both regular text, title may be underlined)
- Bullets use numbering (`<w:numPr>`)

### Education
- Section header: "Education" (NOT all caps)
- Bold, 13pt, centered alignment
- Institution line: **Institution Name** (bold), Location (regular text)
  - Both parts in same paragraph but different runs
  - Format: `<w:b w:val="1"/>` for institution name only
  - Tab stop at position 9720 for potential right-aligned content
  - Line spacing: 240
- Degree line: Degree title (underlined)
  - Single underline: `<w:u w:val="single"/>`
  - Tab stop at position 9720
  - Line spacing: 240
- No graduation date in baseline

## Page Count — Critical Notes

**The baseline resume renders as 3 pages in LibreOffice AND in Word.** `verify_page_count.sh` works correctly — always run it after packing. The 2-page target must be achieved by cutting content from the baseline.

**Verified 2-page char range: 6970–7430 chars.** Char count is a rough guide only — line wrapping matters as much as total chars. Use char count as a pre-check, but always run verify_page_count.sh as the final gate:

**Single-line bullet rule**: Experience bullets (non-list paragraphs) must stay under ~110 chars to render as 1 line. Bullets in the 113–158 char range wrap to 2 lines, adding significant vertical space. Each extra wrap costs one line (~14pt). Four extra wraps = ~56pt ≈ pushed-to-3-page territory even when total char count looks safe. Always check the lengths of paras 19, 20, 24, 25, 26 — these are the most common overflow points.

```bash
python scripts/para_utils.py chars unpacked/word/document.xml
# Baseline = 7679 chars (3 pages). Target: ≤7400 chars for 2 pages.
# Do NOT use "within ±200 of baseline" — baseline is 3 pages, not 2.
```

**Publications must be cut proactively, not as a last resort.** The baseline is already a 3-page document. Tailored resumes must cut enough content to reach 2 pages (target ≤7400 chars). Cut publications first, then bullets from older/less-relevant roles. Do this before writing experience bullets:

1. Remove non-first-author publications unrelated to the target role (e.g., batteries paper for optics role)
2. Always keep: patent application, all first-author publications
3. Can remove: second/third-author publications where the topic is clearly off-domain

Typical cut: 1-2 publications frees ~4-6 lines, creating the headroom needed for tailored experience bullets.

## Content Reduction Strategy

When resume still exceeds budget after proactive publication cuts, follow this priority order:

**Priority 1: Remove entire bullets from older/less-relevant positions**
- Each bullet is typically 150-250 characters
- Removing 2-3 bullets usually brings content back within budget
- Start with positions older than 5 years or less relevant to target role

**Priority 2: Remove additional less-relevant Select Publications and Patents**
- Always keep the patent application.
- Keep all publications where I am the first named author.

**Priority 2: Shorten verbose bullets**
- Target: 150-200 characters per bullet maximum
- Remove redundant phrases like "thereby", "in order to"
- Combine related points into single bullets when possible

**Priority 3: Trim Technical Skills**
- Remove skills only peripherally related to role
- Consolidate similar skills (e.g., "Jira, Asana, Airtable" → "Jira, Asana")

**Priority 4: Reduce Key Accomplishments detail**
- Keep bold headers unchanged (for keyword scanning)
- Trim supporting detail after the bold text
- Target: 200-250 characters total per accomplishment

**Last Resort: Remove one Key Accomplishment**
- Keep the 2 most directly relevant to the job posting

**NEVER:**
- Remove the Summary section, section headers, or branding headline
- Reduce font size or margins (breaks formatting consistency)
- Remove an entire experience

## Page Breaks

To insert a page break before a job header, insert a new `<w:p>` immediately before the header paragraph containing a page break run:

```xml
<w:p>
  <w:pPr>
    <w:spacing w:line="240" w:lineRule="auto"/>
  </w:pPr>
  <w:r>
    <w:br w:type="page"/>
  </w:r>
</w:p>
```

In Python (lxml), insert it like this before the target paragraph:

```python
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
def wt(tag): return '{' + W + '}' + tag

pb_para = etree.Element(wt('p'))
ppr = etree.SubElement(pb_para, wt('pPr'))
sp = etree.SubElement(ppr, wt('spacing'))
sp.set(wt('line'), '240')
sp.set(wt('lineRule'), 'auto')
run = etree.SubElement(pb_para, wt('r'))
br = etree.SubElement(run, wt('br'))
br.set(wt('type'), 'page')

# Insert before the target paragraph
idx = list(body).index(target_paragraph)
body.insert(idx, pb_para)
```

**When to add**: After completing all edits, estimate the layout. If a job title header falls at the bottom of a page separated from its first bullet, insert this paragraph immediately before the company line for that job.

**When NOT to add**: Do not add page breaks preemptively. Only insert where a header would otherwise be orphaned.

## Working on an Existing Output File

**NEVER run `prepare_resume.sh` or `create_tailored_resume.sh` on a file that already exists in `assets/outputs/`.** Both scripts unconditionally overwrite the target file with the baseline before unpacking, destroying any prior edits.

When the user asks you to modify, update, or add to an existing tailored resume, unpack it directly:

```bash
python scripts/unpack.py assets/outputs/[FOLDER]/[FILENAME].docx unpacked/
```

Then edit `unpacked/word/document.xml` and pack back normally. Never use the prepare/create scripts on existing output files.

## Preferred Editing Approach: para_utils.py

**Always use `scripts/para_utils.py` for editing.** It is reliable, index-based, and avoids the run-fragmentation problem (where Word splits one word like "Owned" into `<w:t>Own</w:t>` + `<w:t>ed</w:t>` across separate runs, breaking fragment-search approaches).

### Step 1 — Inspect paragraph indices

```bash
python scripts/para_utils.py list unpacked/word/document.xml
```

Output:
```
[  0]* (XML header)
[  1] [Header    ] B (  20): Theodore (Ted) Cohen
[  5] [normal    ]   ( 420): PhD‑trained researcher with deep experience...
[ 11] [normal    ] B ( 207): Nanofabrication & Process Integration: ...
[ 18] [normal    ]   ( 181): Owned operations for 11 custom and commercial...
```

The index in `[  N]` is the exact value to use in `paras[N]`.

To see the full XML of a specific paragraph (e.g., to copy its pPr):
```bash
python scripts/para_utils.py get unpacked/word/document.xml 18
```

To check total character count for page-length budgeting:
```bash
python scripts/para_utils.py chars unpacked/word/document.xml
# Total chars: 7679  (baseline)
# Keep modified version within ~200 chars of baseline to stay at 2 pages
```

### Step 2 — Write the edit script

```python
import sys
sys.path.insert(0, 'scripts')
from para_utils import split_doc, join_doc, rebuild_para, arial_run, arial_bold, arial_run_simple

with open('unpacked/word/document.xml', 'r', encoding='utf-8') as f:
    content = f.read()

paras, tail = split_doc(content)

# Modify by index — no fragile text-fragment search needed
paras[5]  = rebuild_para(paras[5],  arial_run_simple('New branding statement text here.'))
paras[11] = rebuild_para(paras[11], arial_bold('New Category: ') + arial_run('skill1, skill2, skill3.'))
paras[18] = rebuild_para(paras[18], arial_run('New bullet text for first RS experience bullet.'))

# Remove a paragraph (e.g. less-relevant UW bullet at index 34)
paras.pop(34)

# Insert a page break before paragraph N (only when a job header would be orphaned)
# paras.insert(31, page_break_para())

with open('unpacked/word/document.xml', 'w', encoding='utf-8') as f:
    f.write(join_doc(paras, tail))
```

**Key helpers from para_utils:**
| Function | Use for |
|---|---|
| `arial_run(text)` | Body text in experience bullets, skill body text |
| `arial_bold(text)` | Bold run: skill category labels, KA title prefixes |
| `arial_run_simple(text)` | Branding statement (uses simpler rPr without eastAsiaTheme) |
| `rebuild_para(para, runs_xml)` | Replace all runs in a paragraph, preserve pPr exactly |
| `split_doc(content)` | Split XML into editable paragraph list + sectPr tail |
| `join_doc(paras, tail)` | Reassemble after edits |
| `page_break_para()` | Insert a forced page break paragraph |
| `xe(text)` | XML-escape text (auto-applied inside `arial_run` / `arial_bold`) |

**Note:** `xe()` is called automatically inside `arial_run` and `arial_bold`, so you write `arial_bold("Optics & Holography: ")` — the `&` is auto-escaped to `&amp;` in the XML. Do NOT pre-escape text you pass to these functions.

### Step 3 — Pack and verify

```bash
python scripts/pack.py unpacked/ output.docx --original assets/Ted_Cohen-RESUME.docx
python scripts/para_utils.py chars unpacked/word/document.xml   # compare to baseline ~7679
```

Note: `verify_page_count.sh` uses LibreOffice which renders the baseline as 3 pages.
Use char count comparison instead: keep modified total within ±200 chars of baseline to stay at 2 pages in Word.

## XML Editing Examples (legacy — prefer para_utils approach above)

**Reordering paragraphs:**
Use `split_doc` / `join_doc` from `para_utils.py` and reorder the `paras` list directly.

**Adding new skill categories:**
Copy an existing skill paragraph's pPr using `get` command, then use `rebuild_para` with new run content.

## Common Pitfalls

1. **Using Python stdlib `xml.etree.ElementTree` to write XML**: `ET.write()` strips namespace declarations and can produce wrong encoding (e.g., `cp1252` instead of `UTF-8`), causing Word to refuse to open the file. **Always use `lxml`** for any programmatic XML editing: `from lxml import etree` → `etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)`. Install with `pip install lxml` if needed.

2. **Recreating resume from scratch**: Always edit the baseline XML directly
2. **Changing spacing/indentation**: Preserve all `<w:spacing>` and `<w:ind>` attributes
3. **All-caps section headers**: Use baseline casing exactly (e.g., "Experience" not "EXPERIENCE")
4. **Keyword stuffing**: Keywords must flow naturally in context
5. **Format deviation**: Any deviation from baseline formatting breaks professional appearance
6. **Exceeding 2-page limit**: Always verify page count via PDF conversion before delivery. Remove less-relevant bullets rather than reducing font size or margins.

## Troubleshooting

**If resume formatting looks wrong:**
1. Did you edit the baseline XML directly? (Correct approach)
2. Or did you recreate from scratch with docx-js? (Wrong approach - start over)
3. Check that all spacing and indentation values match baseline
4. Verify section headers match baseline casing exactly
5. Confirm paragraph properties are preserved

For LPS/keyword scoring issues, see `references/qa_and_delivery.md` > Verification Checklist.

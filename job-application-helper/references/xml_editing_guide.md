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

## Content Reduction Strategy

When resume exceeds 2 pages, follow this priority order:

**Priority 1: Remove entire bullets from older/less-relevant positions**
- Each bullet is typically 150-250 characters
- Removing 2-3 bullets usually brings a 3-page resume back to 2 pages
- Start with positions older than 5 years or less relevant to target role

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

## XML Editing Examples

**Updating text content:**
```bash
str_replace \
  --description "Updating branding headline" \
  --old_str '<w:t xml:space="preserve">Old headline text</w:t>' \
  --new_str '<w:t xml:space="preserve">New headline text with keywords</w:t>' \
  --path unpacked/word/document.xml
```

**Reordering paragraphs:**
Use Python script to extract paragraph blocks between `<w:p>` and `</w:p>` tags, reorder them, and write back to document.xml.

**Adding new skill categories:**
Copy an existing skill paragraph block (with all `<w:pPr>`, `<w:numPr>`, spacing, etc.), modify only the `<w:t>` content, and insert at appropriate location.

## Common Pitfalls

1. **Recreating resume from scratch**: Always edit the baseline XML directly
2. **Changing spacing/indentation**: Preserve all `<w:spacing>` and `<w:ind>` attributes
3. **All-caps section headers**: Use baseline casing exactly (e.g., "Experience" not "EXPERIENCE")
4. **Keyword stuffing**: Keywords must flow naturally in context
5. **Format deviation**: Any deviation from baseline formatting breaks professional appearance
6. **Exceeding 2-page limit**: Always verify page count via PDF conversion before delivery. Remove less-relevant bullets rather than reducing font size or margins.
7. **Using stdlib `xml.etree.ElementTree` to write XML**: Python's built-in `ET.write()` changes the encoding declaration and strips namespace prefixes (e.g., `w:`, `r:`), corrupting the .docx XML. The pack/unpack scripts use `defusedxml.minidom` specifically to avoid this. If you need to programmatically manipulate XML, use `defusedxml.minidom` or `lxml` — never `xml.etree.ElementTree` for writing.

## Troubleshooting

**If resume formatting looks wrong:**
1. Did you edit the baseline XML directly? (Correct approach)
2. Or did you recreate from scratch with docx-js? (Wrong approach - start over)
3. Check that all spacing and indentation values match baseline
4. Verify section headers match baseline casing exactly
5. Confirm paragraph properties are preserved

For LPS/keyword scoring issues, see `references/qa_and_delivery.md` > Verification Checklist.

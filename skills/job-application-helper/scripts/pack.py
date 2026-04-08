"""
Pack a directory back into a .docx file.
Usage: python pack.py <unpacked_dir> <output.docx> [--original <original.docx>]

Uses lxml to reserialize document.xml to preserve namespace declarations and
UTF-8 encoding. Falls back to raw bytes if lxml is unavailable.

The --original flag is unused (kept for CLI compatibility with the upstream
pack.py interface) but the unpacked_dir is expected to already contain all
required files from the original docx.
"""
import sys
import zipfile
import os
import argparse


def reserialize_document_xml(xml_bytes):
    """
    Parse document.xml with lxml and re-serialize, preserving namespace
    declarations. Falls back to returning raw bytes if lxml is unavailable.
    """
    try:
        from lxml import etree
        root = etree.fromstring(xml_bytes)
        return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
    except ImportError:
        # lxml not available — return as-is and warn
        print(
            "WARNING: lxml not installed. document.xml will be packed as-is. "
            "If you edited it with Python stdlib ET.write(), the encoding may be wrong. "
            "Install lxml with: pip install lxml",
            file=sys.stderr
        )
        return xml_bytes


def main():
    parser = argparse.ArgumentParser(description='Pack a directory into a .docx file.')
    parser.add_argument('unpacked_dir', help='Directory containing unpacked docx contents')
    parser.add_argument('output_docx', help='Output .docx path')
    parser.add_argument('--original', help='Original .docx (unused, for CLI compatibility)', default=None)
    args = parser.parse_args()

    unpacked_dir = args.unpacked_dir
    output_docx = args.output_docx

    if not os.path.isdir(unpacked_dir):
        print(f"ERROR: Directory not found: {unpacked_dir}", file=sys.stderr)
        sys.exit(1)

    with zipfile.ZipFile(output_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for root, dirs, files in os.walk(unpacked_dir):
            # Sort for deterministic output
            dirs.sort()
            for fname in sorted(files):
                file_path = os.path.join(root, fname)
                arcname = os.path.relpath(file_path, unpacked_dir).replace('\\', '/')

                if arcname == 'word/document.xml':
                    with open(file_path, 'rb') as f:
                        raw = f.read()
                    zout.writestr(arcname, reserialize_document_xml(raw))
                else:
                    zout.write(file_path, arcname)

    print(f"Packed {unpacked_dir} -> {output_docx} ({os.path.getsize(output_docx)} bytes)")


if __name__ == '__main__':
    main()

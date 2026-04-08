"""
Unpack a .docx file to a directory for XML editing.
Usage: python unpack.py <input.docx> <output_dir>
"""
import sys
import zipfile
import os

def main():
    if len(sys.argv) < 3:
        print("Usage: unpack.py <input.docx> <output_dir>", file=sys.stderr)
        sys.exit(1)

    docx_path = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isfile(docx_path):
        print(f"ERROR: File not found: {docx_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(docx_path, 'r') as z:
        z.extractall(output_dir)

    print(f"Unpacked {docx_path} -> {output_dir}")

if __name__ == '__main__':
    main()

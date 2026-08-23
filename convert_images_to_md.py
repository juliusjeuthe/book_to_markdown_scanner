#!/usr/bin/env python3
"""Starter CLI for converting images to Markdown.

This initial version does not run OCR yet — it scaffolds the pipeline, creates output
folders, writes a starter markdown file per image with the `#{to_be_proof_read}` tag,
and updates a simple `image_to_markdown_page_map.md` table.
"""
import argparse
from pathlib import Path
from datetime import datetime
import re

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp'}


def safe_page_number_from_name(name: str):
    m = re.search(r"(\d+)", name)
    if m:
        return int(m.group(1))
    return None


def main():
    parser = argparse.ArgumentParser(description='Convert images to markdown (starter).')
    parser.add_argument('-i', '--input', required=True, help='Input folder with images')
    parser.add_argument('-o', '--output', required=True, help='Output folder for markdown files')
    parser.add_argument('-m', '--map-file', default=None, help='Path to mapping markdown file')
    parser.add_argument('--mark-to-review', action='store_true', help='Insert #{to_be_proof_read} tag (default behavior)')
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    map_file = Path(args.map_file) if args.map_file else output_dir.parent / 'image_to_markdown_page_map.md'

    if not input_dir.exists():
        print(f"Input folder does not exist: {input_dir}")
        raise SystemExit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / '.gitkeep').write_text('')

    images = [p for p in sorted(input_dir.iterdir()) if p.suffix.lower() in IMAGE_EXTS]
    if not images:
        print('No images found in input folder.')
        return

    # Ensure map file exists with header
    if not map_file.exists():
        map_file.parent.mkdir(parents=True, exist_ok=True)
        map_file.write_text('| image_name | markdown_file | page_number | converted_at |\n|---|---|---:|---:|\n')

    for idx, img in enumerate(images, start=1):
        basename = img.stem
        page_num = safe_page_number_from_name(basename) or idx
        md_name = f"{basename}.md"
        md_path = output_dir / md_name

        tag = f"#{'{'}page {page_num}{'}'}" if args.mark_to_review or True else ''
        # write a starter markdown
        content_lines = [tag, '\n', f'<!-- source image: {img.name} -->', '\n', 'TODO: OCR output will go here.']
        md_path.write_text('\n'.join(content_lines))
        print(f'Wrote {md_path}')

        # append to map file
        ts = datetime.utcnow().isoformat() + 'Z'
        row = f'| {img.name} | {md_name} | {page_num} | {ts} |\n'
        with map_file.open('a', encoding='utf-8') as f:
            f.write(row)

    print('Done. Next: implement OCR and preprocessing, then replace TODO in each md.')


if __name__ == '__main__':
    main()

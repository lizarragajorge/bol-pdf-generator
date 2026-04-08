"""
BoL PDF Generator — Generate Bill of Lading PDFs for testing/scoring a BoL classifier.

Usage:
    python main.py                          # 10 PDFs, mixed templates, output to ./output
    python main.py -n 50                    # 50 PDFs
    python main.py -n 20 -t ocean          # 20 ocean BoLs only
    python main.py -n 30 -t ocean,truck    # 30 PDFs split across ocean & truck templates
    python main.py -o my_folder            # custom output directory
    python main.py --seed 42               # reproducible generation
"""

import argparse
import os
import random
import sys

from data_generator import generate_bol_data
from templates import TEMPLATES


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Bill of Lading PDFs for classifier testing."
    )
    parser.add_argument(
        "-n", "--count", type=int, default=10,
        help="Number of PDFs to generate (default: 10)."
    )
    parser.add_argument(
        "-t", "--templates", type=str, default=None,
        help="Comma-separated list of template types to use. "
             f"Available: {', '.join(TEMPLATES.keys())}. "
             "Default: all templates."
    )
    parser.add_argument(
        "-o", "--output", type=str, default="output",
        help="Output directory (default: ./output)."
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed for reproducible generation."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    # Determine which templates to use
    if args.templates:
        template_names = [t.strip() for t in args.templates.split(",")]
        for t in template_names:
            if t not in TEMPLATES:
                print(f"Error: Unknown template '{t}'. Available: {', '.join(TEMPLATES.keys())}")
                sys.exit(1)
    else:
        template_names = list(TEMPLATES.keys())

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    print(f"Generating {args.count} BoL PDFs using templates: {', '.join(template_names)}")
    print(f"Output directory: {os.path.abspath(args.output)}")
    print()

    # Generate manifest for classifier evaluation
    manifest_lines = ["filename,template_type,bol_number,shipper,consignee"]

    for i in range(1, args.count + 1):
        template_name = random.choice(template_names)
        data = generate_bol_data(template_type=template_name)

        filename = f"bol_{i:04d}_{template_name}.pdf"
        filepath = os.path.join(args.output, filename)

        render_fn = TEMPLATES[template_name]
        render_fn(data, filepath)

        manifest_lines.append(
            f"{filename},{template_name},{data.bol_number},"
            f"\"{data.shipper_name}\",\"{data.consignee_name}\""
        )

        print(f"  [{i}/{args.count}] {filename}  ({template_name})")

    # Write manifest CSV
    manifest_path = os.path.join(args.output, "manifest.csv")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("\n".join(manifest_lines) + "\n")

    print()
    print(f"Done! Generated {args.count} PDFs in {os.path.abspath(args.output)}")
    print(f"Manifest written to {manifest_path}")


if __name__ == "__main__":
    main()

"""
BoL PDF Generator — Generate Bill of Lading and related PDFs for testing/scoring a BoL classifier.

Usage:
    python main.py                          # 10 PDFs, mixed templates, output to ./output
    python main.py -n 50                    # 50 PDFs
    python main.py -n 20 -t ocean          # 20 ocean BoLs only
    python main.py -n 30 -t ocean,truck    # 30 PDFs split across ocean & truck templates
    python main.py -o my_folder            # custom output directory
    python main.py --seed 42               # reproducible generation
    python main.py -c non_bol              # only non-BoL documents (invoices, packing lists, etc.)
    python main.py -c bol_partial          # documents containing BoL content
    python main.py -c all                  # all categories (bol + non_bol + bol_partial)
"""

import argparse
import os
import random
import sys

from data_generator import (
    generate_bol_data, generate_invoice_data, generate_packing_list_data,
    generate_delivery_order_data, generate_cover_letter_data,
    generate_freight_manifest_data,
)
from templates import (
    TEMPLATES, NON_BOL_TEMPLATES, BOL_PARTIAL_TEMPLATES,
    ALL_TEMPLATES, TEMPLATE_CATEGORIES,
)

# Category -> set of template names
CATEGORY_TEMPLATES = {
    "bol": TEMPLATES,
    "non_bol": NON_BOL_TEMPLATES,
    "bol_partial": BOL_PARTIAL_TEMPLATES,
    "all": ALL_TEMPLATES,
}

# Template name -> data generator function
DATA_GENERATORS = {
    "ocean": lambda: generate_bol_data("ocean"),
    "truck": lambda: generate_bol_data("truck"),
    "short": lambda: generate_bol_data("short"),
    "multimodal": lambda: generate_bol_data("multimodal"),
    "ocean_multi": lambda: generate_bol_data("ocean_multi"),
    "truck_multi": lambda: generate_bol_data("truck_multi"),
    "commercial_invoice": generate_invoice_data,
    "packing_list": generate_packing_list_data,
    "delivery_order": generate_delivery_order_data,
    "commercial_invoice_multi": lambda: generate_invoice_data(multi=True),
    "packing_list_multi": lambda: generate_packing_list_data(multi=True),
    "bol_cover_letter": generate_cover_letter_data,
    "freight_manifest": generate_freight_manifest_data,
    "bol_cover_letter_multi": lambda: generate_cover_letter_data(multi=True),
    "freight_manifest_multi": lambda: generate_freight_manifest_data(multi=True),
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Bill of Lading and related PDFs for classifier testing."
    )
    parser.add_argument(
        "-n", "--count", type=int, default=10,
        help="Number of PDFs to generate (default: 10)."
    )
    parser.add_argument(
        "-t", "--templates", type=str, default=None,
        help="Comma-separated list of template types to use. "
             f"Available: {', '.join(ALL_TEMPLATES.keys())}. "
             "Default: determined by --category."
    )
    parser.add_argument(
        "-c", "--category", type=str, default="bol",
        help="Document category: bol, non_bol, bol_partial, all (default: bol). "
             "Ignored when --templates is specified."
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
            if t not in ALL_TEMPLATES:
                print(f"Error: Unknown template '{t}'. Available: {', '.join(ALL_TEMPLATES.keys())}")
                sys.exit(1)
    else:
        if args.category not in CATEGORY_TEMPLATES:
            print(f"Error: Unknown category '{args.category}'. Available: {', '.join(CATEGORY_TEMPLATES.keys())}")
            sys.exit(1)
        template_names = list(CATEGORY_TEMPLATES[args.category].keys())

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    print(f"Generating {args.count} PDFs using templates: {', '.join(template_names)}")
    print(f"Output directory: {os.path.abspath(args.output)}")
    print()

    # Generate manifest for classifier evaluation
    manifest_lines = ["filename,template_type,category,is_bol,identifier"]

    for i in range(1, args.count + 1):
        template_name = random.choice(template_names)
        category = TEMPLATE_CATEGORIES[template_name]
        is_bol = "yes" if category == "bol" else "no"

        # Generate data using the appropriate generator
        data = DATA_GENERATORS[template_name]()

        pages = "multipage" if "_multi" in template_name else "singlepage"
        filename = f"{category}_{i:04d}_{template_name}_{pages}.pdf"
        filepath = os.path.join(args.output, filename)

        render_fn = ALL_TEMPLATES[template_name]
        render_fn(data, filepath)

        # Extract a meaningful identifier from the data
        if hasattr(data, "bol_number"):
            identifier = data.bol_number
        elif hasattr(data, "invoice_number"):
            identifier = data.invoice_number
        elif hasattr(data, "packing_list_number"):
            identifier = data.packing_list_number
        elif hasattr(data, "do_number"):
            identifier = data.do_number
        elif hasattr(data, "reference_number"):
            identifier = data.reference_number
        elif hasattr(data, "manifest_number"):
            identifier = data.manifest_number
        else:
            identifier = ""

        manifest_lines.append(
            f"{filename},{template_name},{category},{is_bol},{identifier}"
        )

        print(f"  [{i}/{args.count}] {filename}  ({template_name} | {category})")

    # Write manifest CSV
    manifest_path = os.path.join(args.output, "manifest.csv")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("\n".join(manifest_lines) + "\n")

    print()
    print(f"Done! Generated {args.count} PDFs in {os.path.abspath(args.output)}")
    print(f"Manifest written to {manifest_path}")


if __name__ == "__main__":
    main()

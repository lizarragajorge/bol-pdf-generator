# BoL PDF Generator

Generate synthetic Bill of Lading (BoL) and related shipping document PDFs for testing and scoring document classifiers — built for use with Azure AI Content Understanding Studio and similar pipelines.

## Features

- **13 distinct templates** across 3 document categories:

  **BoL templates** (`-c bol`) — actual Bills of Lading:
  | Template | Description |
  |----------|-------------|
  | `ocean` | Classic ocean freight BoL — 3-party header, vessel/port routing, container cargo table |
  | `truck` | US-style straight inland BoL — carrier/driver info, NMFC classes, freight charges |
  | `short` | Compact single-page non-negotiable short-form BoL |
  | `multimodal` | FIATA-style combined transport BoL with pre/on-carriage legs (A4) |
  | `ocean_multi` | Multi-page ocean BoL — 6-12 containers + full Terms & Conditions back page |
  | `truck_multi` | Multi-page truck BoL — 15-30 line items + Terms & Conditions page |

  **Non-BoL templates** (`-c non_bol`) — negative examples for classifier training:
  | Template | Description |
  |----------|-------------|
  | `commercial_invoice` | Standard commercial invoice with line items, HS codes, and totals |
  | `packing_list` | Packing list with item dimensions, weights, and package types |
  | `delivery_order` | Port/carrier delivery order for container release |
  | `commercial_invoice_multi` | Multi-page invoice — 15-30 line items + Terms & Conditions page |
  | `packing_list_multi` | Multi-page packing list — 20-40 items + Terms & Conditions page |

  **BoL-partial templates** (`-c bol_partial`) — documents that reference or contain BoL data:
  | Template | Description |
  |----------|-------------|
  | `bol_cover_letter` | Cover letter that references and summarizes a full BoL |
  | `freight_manifest` | Cargo manifest listing multiple BoL numbers and shipment details |

- **Randomized data** — shipper/consignee companies, addresses, vessel names, ports, container numbers, commodities, weights, and volumes via [Faker](https://github.com/joke2k/faker)
- **Ground-truth manifest** — each run produces a `manifest.csv` with `category` and `is_bol` labels for classifier evaluation
- **Reproducible** — optional `--seed` flag for deterministic output

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## Usage

```
python main.py [OPTIONS]

Options:
  -n, --count N          Number of PDFs to generate (default: 10)
  -c, --category CAT     Document category: bol, non_bol, bol_partial, all
                         (default: bol). Ignored when --templates is specified.
  -t, --templates LIST   Comma-separated template types (see table above)
  -o, --output DIR       Output directory (default: ./output)
  --seed N               Random seed for reproducible generation
```

### Examples

```bash
# Generate 10 BoL PDFs using all BoL templates (default)
python main.py

# Generate 50 ocean-only BoLs
python main.py -n 50 -t ocean

# Generate non-BoL documents (invoices, packing lists, delivery orders)
python main.py -n 20 -c non_bol -o output/non_bol

# Generate BoL-partial documents (cover letters, freight manifests)
python main.py -n 20 -c bol_partial -o output/bol_partial

# Generate all document types
python main.py -n 30 -c all

# Mix specific templates across categories
python main.py -n 20 -t ocean,commercial_invoice,freight_manifest

# Reproducible generation
python main.py -n 30 -c all --seed 42
```

## Output

```
output/
├── doc_0001_ocean.pdf
├── doc_0002_commercial_invoice.pdf
├── doc_0003_bol_cover_letter.pdf
├── ...
└── manifest.csv
```

The `manifest.csv` contains:

```csv
filename,template_type,category,is_bol,identifier
doc_0001_ocean.pdf,ocean,bol,yes,MSKU914763202
doc_0002_commercial_invoice.pdf,commercial_invoice,non_bol,no,INV-482910
doc_0003_bol_cover_letter.pdf,bol_cover_letter,bol_partial,no,REF-319204
```

## Project Structure

```
bol-pdf-generator/
├── main.py            # CLI entry point
├── data_generator.py  # Random data generation for all document types
├── templates.py       # PDF rendering templates (ReportLab)
├── requirements.txt
├── LICENSE
└── README.md
```

## License

[MIT](LICENSE)

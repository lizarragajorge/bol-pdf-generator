# BoL PDF Generator

Generate synthetic Bill of Lading (BoL) PDFs for testing and scoring document classifiers — built for use with Azure AI Content Understanding Studio and similar pipelines.

## Features

- **4 distinct templates** with different visual layouts, colors, and field arrangements:
  | Template | Description |
  |----------|-------------|
  | `ocean` | Classic ocean freight BoL — 3-party header, vessel/port routing, container cargo table |
  | `truck` | US-style straight inland BoL — carrier/driver info, NMFC classes, freight charges |
  | `short` | Compact single-page non-negotiable short-form BoL |
  | `multimodal` | FIATA-style combined transport BoL with pre/on-carriage legs (A4) |

- **Randomized data** — shipper/consignee companies, addresses, vessel names, ports, container numbers, commodities, weights, and volumes via [Faker](https://github.com/joke2k/faker)
- **Ground-truth manifest** — each run produces a `manifest.csv` mapping every filename to its template type, BoL number, shipper, and consignee for classifier evaluation
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
  -t, --templates LIST   Comma-separated template types: ocean, truck, short, multimodal
                         (default: all)
  -o, --output DIR       Output directory (default: ./output)
  --seed N               Random seed for reproducible generation
```

### Examples

```bash
# Generate 10 PDFs using all templates
python main.py

# Generate 50 ocean-only BoLs
python main.py -n 50 -t ocean

# Mix of ocean and truck, reproducible
python main.py -n 30 -t ocean,truck --seed 42

# Custom output folder
python main.py -n 20 -o test_data
```

## Output

```
output/
├── bol_0001_ocean.pdf
├── bol_0002_truck.pdf
├── bol_0003_short.pdf
├── bol_0004_multimodal.pdf
├── ...
└── manifest.csv
```

The `manifest.csv` contains:

```csv
filename,template_type,bol_number,shipper,consignee
bol_0001_ocean.pdf,ocean,MSKU914763202,"Roberts-Lee","Edwards, Hogan and Wright"
```

## Project Structure

```
bol-pdf-generator/
├── main.py            # CLI entry point
├── data_generator.py  # Random BoL data generation
├── templates.py       # PDF rendering templates (ReportLab)
├── requirements.txt
├── LICENSE
└── README.md
```

## License

[MIT](LICENSE)

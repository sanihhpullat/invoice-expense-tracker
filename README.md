# Invoice & Expense Tracker (KSA VAT-ready)

A CLI tool that turns a simple CSV of sales and expenses into a monthly
profit/loss and VAT report — built with small Riyadh businesses in mind.

## Why I built this

While applying to gaming PC shops and small IT businesses around Riyadh,
I noticed most of them are still tracking sales and expenses by hand or
in scattered Excel sheets, with no easy way to see monthly profit or
calculate the 15% VAT they owe. This tool solves that in a few seconds
from a single CSV file.

## What it does

- Reads a CSV of transactions (`sale` or `expense` rows)
- Groups everything by month
- Calculates total sales, total expenses, net profit, and VAT due (15%, the KSA standard rate)
- Prints a clean summary table to the terminal
- Optionally exports the same report as a PDF

## CSV format

```csv
date,type,description,amount
2026-06-02,sale,Gaming PC build - custom order,4500
2026-06-15,expense,Shop rent,1500
```

## Usage

```bash
# Print report to terminal
python invoice_tracker.py data/transactions.csv

# Also export as PDF
python invoice_tracker.py data/transactions.csv --pdf report.pdf
```

## Setup

```bash
pip install reportlab --break-system-packages   # only needed for PDF export
```

## Sample output

```
============================================================
Month          Sales    Expenses      Profit     VAT Due
------------------------------------------------------------
2026-06      5450.00      3980.00     1470.00      817.50
2026-07      6100.00      7000.00     -900.00      915.00
============================================================
VAT calculated at 15% (KSA standard rate) on total sales.
```

## What I'd add next

- Multi-currency support
- A simple web dashboard using Streamlit
- ZATCA e-invoicing (Fatoora) compliant XML output

## Author

Sanih Fazalul Rahiman Pullat — Riyadh
[github.com/sanihhpullat](https://github.com/sanihhpullat)

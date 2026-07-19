"""
Invoice & Expense Tracker (KSA VAT-ready)
Author: Sanih Fazalul Rahiman Pullat
GitHub: github.com/sanihhpullat

Reads sales and expense records from a CSV, calculates profit/loss and
15% Saudi VAT, and generates a monthly summary as both a printed report
and a PDF file. Built with small Riyadh shops in mind — the kind of
place still tracking everything in a notebook or a messy spreadsheet.

Usage:
    python invoice_tracker.py data/transactions.csv
    python invoice_tracker.py data/transactions.csv --pdf report.pdf
"""

import argparse
import csv
from collections import defaultdict
from datetime import datetime

VAT_RATE = 0.15  # KSA standard VAT rate


def load_transactions(csv_path):
    transactions = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append({
                "date": row["date"].strip(),
                "type": row["type"].strip().lower(),  # 'sale' or 'expense'
                "description": row["description"].strip(),
                "amount": float(row["amount"]),
            })
    return transactions


def summarize(transactions):
    monthly = defaultdict(lambda: {"sales": 0.0, "expenses": 0.0})

    for t in transactions:
        try:
            dt = datetime.strptime(t["date"], "%Y-%m-%d")
        except ValueError:
            continue
        key = dt.strftime("%Y-%m")
        if t["type"] == "sale":
            monthly[key]["sales"] += t["amount"]
        elif t["type"] == "expense":
            monthly[key]["expenses"] += t["amount"]

    report = {}
    for month, values in sorted(monthly.items()):
        sales = values["sales"]
        expenses = values["expenses"]
        profit = sales - expenses
        vat_due = sales * VAT_RATE
        report[month] = {
            "sales": round(sales, 2),
            "expenses": round(expenses, 2),
            "profit": round(profit, 2),
            "vat_due": round(vat_due, 2),
        }
    return report


def print_report(report):
    print("=" * 60)
    print(f"{'Month':<10}{'Sales':>12}{'Expenses':>12}{'Profit':>12}{'VAT Due':>12}")
    print("-" * 60)
    for month, values in report.items():
        print(f"{month:<10}{values['sales']:>12.2f}{values['expenses']:>12.2f}"
              f"{values['profit']:>12.2f}{values['vat_due']:>12.2f}")
    print("=" * 60)
    print("VAT calculated at 15% (KSA standard rate) on total sales.")


def export_pdf(report, output_path):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError:
        print("reportlab not installed. Run: pip install reportlab --break-system-packages")
        return

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Monthly Sales & Expense Report")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Prepared by Sanih Fazalul Rahiman Pullat")
    y -= 30

    c.setFont("Helvetica-Bold", 11)
    headers = ["Month", "Sales (SAR)", "Expenses (SAR)", "Profit (SAR)", "VAT Due (SAR)"]
    x_positions = [50, 140, 250, 360, 460]
    for x, h in zip(x_positions, headers):
        c.drawString(x, y, h)
    y -= 15
    c.line(50, y, 550, y)
    y -= 15

    c.setFont("Helvetica", 10)
    for month, values in report.items():
        row = [month, f"{values['sales']:.2f}", f"{values['expenses']:.2f}",
               f"{values['profit']:.2f}", f"{values['vat_due']:.2f}"]
        for x, val in zip(x_positions, row):
            c.drawString(x, y, str(val))
        y -= 18
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    print(f"PDF report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Summarize sales/expenses and calculate KSA VAT")
    parser.add_argument("csv_path", help="Path to transactions CSV file")
    parser.add_argument("--pdf", help="Also export report as PDF to this path")
    args = parser.parse_args()

    transactions = load_transactions(args.csv_path)
    report = summarize(transactions)
    print_report(report)

    if args.pdf:
        export_pdf(report, args.pdf)


if __name__ == "__main__":
    main()

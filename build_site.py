"""Build a static HTML dashboard from sample JSON transaction data."""

import html
import json
from pathlib import Path

from risk import classify_transaction

ROOT = Path(__file__).resolve().parent


def build_site():
    transactions = json.loads((ROOT / "data" / "transactions.json").read_text(encoding="utf-8"))
    rows = []
    high_count = 0
    for transaction in transactions:
        label = classify_transaction(transaction["amount"])
        high_count += label == "High Risk"
        risk_class = "high" if label == "High Risk" else "low"
        txn_id = html.escape(str(transaction["id"]))
        amount = f'${transaction["amount"]:,.2f}'
        rows.append(f'<tr><td>{txn_id}</td><td>{amount}</td><td class="{risk_class}">{label}</td></tr>')

    content = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Transaction Risk Dashboard</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 820px; margin: 48px auto; padding: 0 18px; background: #f7f9fc; color: #1d2939; }
    h1 { margin-bottom: 6px; } p { color: #586576; }
    .stats { display: flex; flex-wrap: wrap; gap: 14px; margin: 25px 0; }
    .stat { background: white; border-radius: 12px; padding: 18px; min-width: 135px; box-shadow: 0 1px 5px #dde2e9; }
    .number { font-size: 28px; font-weight: 700; display: block; }
    table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; }
    th, td { text-align: left; padding: 14px; border-bottom: 1px solid #edf0f4; }
    th { background: #e9eff8; } .high { color: #bf2525; font-weight: 700; } .low { color: #168047; font-weight: 700; }
  </style>
</head>
<body>
  <h1>Transaction Risk Dashboard</h1>
  <p>A tiny Python app built, tested, and deployed with GitHub Actions.</p>
  <div class="stats">
    <div class="stat">Transactions<span class="number">__TOTAL__</span></div>
    <div class="stat">High Risk<span class="number">__HIGH__</span></div>
    <div class="stat">Low Risk<span class="number">__LOW__</span></div>
  </div>
  <table><thead><tr><th>ID</th><th>Amount</th><th>Risk</th></tr></thead>
  <tbody>__ROWS__</tbody></table>
  <p>Demo only — simple amount-based rules, not a real fraud or AML detection model.</p>
</body>
</html>
"""
    content = (content.replace("__TOTAL__", str(len(transactions)))
                      .replace("__HIGH__", str(high_count))
                      .replace("__LOW__", str(len(transactions) - high_count))
                      .replace("__ROWS__", "\n".join(rows)))
    output = ROOT / "site" / "index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    print(f"Built {output} ({len(transactions)} transactions)")


if __name__ == "__main__":
    build_site()

# -*- coding: utf-8 -*-
"""
KACY LTD - Historical Driver Analysis & 2026-2028 Income Statement Projection
================================================================================
Reads new_KACY_Financial_Data_2023_2025.xlsx, cleans it into a tidy structure,
derives historical financial drivers programmatically, and projects the
Income Statement for FY2026-FY2028. Every number below is computed from the
source file at runtime - nothing is hardcoded.

Requires: pandas, openpyxl  (pip install pandas openpyxl)
"""

import pandas as pd
import numpy as np

FILE_PATH = "new_KACY_Financial_Data_2023_2025.xlsx"
SHEET_NAME = "Financial_data"
PROJECTION_YEARS = [2026, 2027, 2028,2029,2030]

# ---------------------------------------------------------------------------
# STEP 1 - DATA INGESTION & DIAGNOSTICS
# ---------------------------------------------------------------------------

xl = pd.ExcelFile(FILE_PATH)
print("Sheet names found:", xl.sheet_names)

raw = xl.parse(SHEET_NAME)
year_cols = [c for c in raw.columns if isinstance(c, (int, np.integer))]
year_cols = sorted(year_cols)
print("Year columns detected:", year_cols)

# Tag each row with its statement section by forward-filling section headers,
# then drop the header/blank rows themselves. This makes the line items
# uniform and analysis-ready across all three years.
SECTION_HEADERS = {
    "INCOME STATEMENT (ACTUALS)": "Income Statement",
    "BALANCE SHEET (ACTUALS, AS OF DEC 31)": "Balance Sheet",
}
raw["Account"] = raw["Account"].astype("string").str.strip()
raw["statement_type"] = raw["Account"].map(SECTION_HEADERS)
raw["statement_type"] = raw["statement_type"].ffill()

is_header_row = raw["Account"].isin(SECTION_HEADERS.keys())
is_blank_row = raw["Account"].isna() | (raw[year_cols].isna().all(axis=1))
clean = raw.loc[~(is_header_row | is_blank_row)].copy()

# Wide, tidy table: Account as index, one numeric column per fiscal year
wide = clean.set_index("Account")[year_cols].apply(pd.to_numeric, errors="coerce")
wide.columns = [int(c) for c in wide.columns]

statement_map = clean.set_index("Account")["statement_type"].to_dict()

print("\nCleaned historical dataset:")
print(wide)


def get(account, year):
    """Look up a reported value by account name and fiscal year."""
    return wide.loc[account, year]


# ---------------------------------------------------------------------------
# STEP 2 - HISTORICAL DRIVER CALCULATION
# ---------------------------------------------------------------------------

years_hist = year_cols  # [2023, 2024, 2025]

# --- Revenue growth ---
yoy_growth = {
    years_hist[i]: (get("Revenue", years_hist[i]) / get("Revenue", years_hist[i - 1])) - 1
    for i in range(1, len(years_hist))
}
revenue_cagr = (get("Revenue", years_hist[-1]) / get("Revenue", years_hist[0])) ** (
    1 / (years_hist[-1] - years_hist[0])
) - 1

# --- Margin drivers, computed per year then averaged across all historical years ---
cogs_margin = {y: get("Cost of Sales", y) / get("Revenue", y) for y in years_hist}
opex_line_margin = {y: get("Operating Expenses", y) / get("Revenue", y) for y in years_hist}
admin_margin = {y: get("Administrative Expenses", y) / get("Revenue", y) for y in years_hist}
employment_margin = {y: get("Employment Expenses", y) / get("Revenue", y) for y in years_hist}
total_opex_margin = {
    y: (get("Operating Expenses", y) + get("Administrative Expenses", y)
        + get("Employment Expenses", y)) / get("Revenue", y)
    for y in years_hist
}
tax_rate = {y: get("Income Tax", y) / get("Profit Before Tax", y) for y in years_hist}

avg_cogs_margin = np.mean(list(cogs_margin.values()))
avg_opex_line_margin = np.mean(list(opex_line_margin.values()))
avg_admin_margin = np.mean(list(admin_margin.values()))
avg_employment_margin = np.mean(list(employment_margin.values()))
avg_total_opex_margin = np.mean(list(total_opex_margin.values()))

latest_year = years_hist[-1]                       # 2025
tax_rate_latest = tax_rate[latest_year]             # 2025 effective tax rate
financial_expense_latest = get("Financial Expenses", latest_year)
bank_loan_latest = get("Bank Loan", latest_year)

# --- Anomaly detection: Bank Loan introduction / Financial Expense spike ---
anomalies = []
for y in years_hist:
    prior_years = [yy for yy in years_hist if yy < y]
    if not prior_years:
        continue
    prior = max(prior_years)
    loan_prior, loan_now = get("Bank Loan", prior), get("Bank Loan", y)
    fe_prior, fe_now = get("Financial Expenses", prior), get("Financial Expenses", y)
    if loan_prior == 0 and loan_now > 0:
        fe_growth = (fe_now / fe_prior) - 1 if fe_prior else float("inf")
        anomalies.append(
            f"FY{y}: Bank Loan introduced (FY{prior}: {loan_prior:,.0f} -> FY{y}: {loan_now:,.0f} RWF). "
            f"Financial Expenses grew {fe_growth:.1%} in the same year "
            f"(FY{prior}: {fe_prior:,.0f} -> FY{y}: {fe_now:,.0f} RWF)."
        )

print("\nHistorical drivers computed:")
print("YoY Revenue growth:", {k: f"{v:.2%}" for k, v in yoy_growth.items()})
print(f"Revenue CAGR ({years_hist[0]}-{years_hist[-1]}): {revenue_cagr:.2%}")
print("COGS % of Revenue by year:", {k: f"{v:.2%}" for k, v in cogs_margin.items()},
      f"| 3-yr avg: {avg_cogs_margin:.2%}")
print("Total OpEx % of Revenue by year:", {k: f"{v:.2%}" for k, v in total_opex_margin.items()},
      f"| 3-yr avg: {avg_total_opex_margin:.2%}")
print("Effective Tax Rate by year:", {k: f"{v:.2%}" for k, v in tax_rate.items()},
      f"| FY{latest_year} rate used for projection: {tax_rate_latest:.2%}")
print("\nAnomalies flagged:")
for a in anomalies:
    print(" -", a)

# ---------------------------------------------------------------------------
# STEP 3 - PROJECTION MODELING (2026-2028)
# ---------------------------------------------------------------------------

projection = {}
prior_revenue = get("Revenue", latest_year)

for y in PROJECTION_YEARS:
    revenue_y = prior_revenue * (1 + revenue_cagr)
    cogs_y = revenue_y * avg_cogs_margin
    gross_profit_y = revenue_y - cogs_y
    opex_y = revenue_y * avg_opex_line_margin
    admin_y = revenue_y * avg_admin_margin
    employment_y = revenue_y * avg_employment_margin
    financial_expense_y = financial_expense_latest  # flat, interest-only carry on FY2025 debt
    pbt_y = gross_profit_y - opex_y - admin_y - employment_y - financial_expense_y
    tax_y = pbt_y * tax_rate_latest
    net_profit_y = pbt_y - tax_y

    projection[y] = {
        "Revenue": revenue_y,
        "Cost of Sales": cogs_y,
        "Gross Profit": gross_profit_y,
        "Operating Expenses": opex_y,
        "Administrative Expenses": admin_y,
        "Employment Expenses": employment_y,
        "Total Operating Expenses": opex_y + admin_y + employment_y,
        "Financial Expenses": financial_expense_y,
        "Profit Before Tax": pbt_y,
        "Income Tax": tax_y,
        "Net Profit": net_profit_y,
    }
    prior_revenue = revenue_y  # compound off the newly projected revenue

proj_df = pd.DataFrame(projection).T
proj_df.index.name = "fiscal_year"

print("\nProjected Income Statement (2026-2028):")
print(proj_df.round(0))

# ---------------------------------------------------------------------------
# STEP 4 - OUTPUT: markdown table + assumptions
# ---------------------------------------------------------------------------

IS_LINE_ORDER = ["Revenue", "Cost of Sales", "Gross Profit", "Operating Expenses",
                  "Administrative Expenses", "Employment Expenses", "Financial Expenses",
                  "Profit Before Tax", "Income Tax", "Net Profit"]


def fmt(x):
    return f"{x:,.0f}"


lines = []
lines.append("| Account (RWF) | " + " | ".join(f"FY{y}P" for y in PROJECTION_YEARS) + " |")
lines.append("|---|" + "---:|" * len(PROJECTION_YEARS))
for acc in IS_LINE_ORDER:
    row = [fmt(projection[y][acc]) for y in PROJECTION_YEARS]
    lines.append(f"| {acc} | " + " | ".join(row) + " |")
markdown_table = "\n".join(lines)

print("\n" + markdown_table)

print("\nAssumptions used:")
print(f"- Revenue growth (CAGR {years_hist[0]}-{years_hist[-1]}): {revenue_cagr:.2%} per year")
print(f"- Cost of Sales: {avg_cogs_margin:.2%} of Revenue (3-yr historical average)")
print(f"- Operating Expenses: {avg_opex_line_margin:.2%} of Revenue (3-yr historical average)")
print(f"- Administrative Expenses: {avg_admin_margin:.2%} of Revenue (3-yr historical average)")
print(f"- Employment Expenses: {avg_employment_margin:.2%} of Revenue (3-yr historical average)")
print(f"- Total OpEx (combined): {avg_total_opex_margin:.2%} of Revenue (3-yr historical average)")
print(f"- Financial Expenses: held flat at FY{latest_year} level ({fmt(financial_expense_latest)} RWF/yr)")
print(f"- Tax Rate: {tax_rate_latest:.2%} (FY{latest_year} effective rate)")

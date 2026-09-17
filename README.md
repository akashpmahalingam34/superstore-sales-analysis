# Superstore Sales & Profitability Analysis

Cleaned and analyzed the Sample Superstore dataset (9,994 retail orders, 2017–2020) to find where the business was making and losing money, and turned the findings into a business recommendation.

## Business Questions
- Which categories and regions drive the most sales and profit?
- Are any products or categories actually losing money?
- How does discounting affect profitability?
- What should the business change?

## Data Cleaning
The raw Excel export had real data-quality issues:
- Sales stored as text with a dollar sign (e.g. `"$378.0"`) — stripped and converted to numeric
- Profit stored in accounting format, where losses are wrapped in parentheses (e.g. `"($88)"` means -$88) — parsed into signed numeric values
- Missing Order Dates, Segments, Regions, and Categories — rows missing a date, category, sales, or profit value were dropped; missing Segment/Region were labeled "Unknown" instead

## Key Findings
- **Total sales:** $2,297,066 | **Total profit:** $286,341 | **Margin:** 12.5%
- Furniture generates almost as much in sales as Technology ($742K vs $836K) but only a 2.5% margin, vs. Technology's 17%
- **Tables lose money overall** (-$17,733 total profit) despite $207K in sales
- Orders discounted above 20% lose money on average (-$97/order), vs. +$67/order with no discount
- Sales peak every November–December, consistent with holiday seasonality

## Recommendations
1. Cap standard discounts at 20% — anything higher loses money on average
2. Re-price or re-negotiate supplier costs on Tables and Bookcases — structurally unprofitable at current pricing
3. Shift marketing/inventory investment toward Technology, which converts sales to profit most efficiently
4. Investigate the South region's lower sales — under-marketed vs. genuinely lower demand
5. Build up Q4 inventory ahead of the recurring November–December demand spike

## Files
- `analyze_real.py` — cleaning, analysis, and chart generation (Python: pandas, matplotlib)
- `superstore_raw.csv` — raw dataset
- `superstore_clean.csv` — cleaned dataset
- `Superstore_Analysis_Report.docx` — full written report
- `charts/` — generated charts (profit by category, worst sub-categories, sales by region, monthly trend)

## Tools
Python (pandas, matplotlib). The same analysis is doable in Excel with PivotTables, or Power BI/Tableau for an interactive dashboard version.

## Source
Dataset: [Sample Superstore](https://github.com/Ogunbod/Superstore-Analysis) — a public dataset originally distributed with Tableau, commonly used for BI/analytics practice.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["figure.dpi"] = 150

df = pd.read_csv("/home/claude/superstore_raw.csv")
print("RAW SHAPE:", df.shape)
print("\nNULLS PER COLUMN:\n", df.isnull().sum()[df.isnull().sum() > 0])
print("\nSAMPLE MESSY VALUES:")
print(df[["Sales", "Profit"]].head(3))

# ---------------- CLEANING ----------------
# 1. Sales: strip "$" and convert to float
df["Sales"] = df["Sales"].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False).astype(float)

# 2. Profit: accounting format uses ($88) for -88 -- convert
def parse_profit(x):
    x = str(x).strip()
    neg = x.startswith("(") and x.endswith(")")
    x = x.strip("()").replace("$", "").replace(",", "")
    try:
        val = float(x)
    except ValueError:
        return None
    return -val if neg else val

df["Profit"] = df["Profit"].apply(parse_profit)

# 3. Drop rows with no Order Date / missing Category (can't analyze without them) -- but keep count
before = len(df)
df = df.dropna(subset=["Order Date", "Category", "Sales", "Profit"])
print(f"\nDropped {before - len(df)} rows with missing core fields (date/category/sales/profit)")

# 4. Fill remaining non-critical missing values
df["Segment"] = df["Segment"].fillna("Unknown")
df["Region"] = df["Region"].fillna("Unknown")
df["Discount"] = df["Discount"].fillna(0)

# 5. Parse dates properly
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
df["Year"] = df["Order Date"].dt.year

df.to_csv("/home/claude/superstore_clean.csv", index=False)
print("\nCLEANED SHAPE:", df.shape)

# ---------------- ANALYSIS ----------------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
margin = total_profit / total_sales * 100

by_category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
profit_by_cat = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
by_region = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
by_month = df.groupby("Month")["Sales"].sum()
by_segment = df.groupby("Segment")[["Sales", "Profit"]].sum()
top_subcats = df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False)
loss_subcats = df.groupby("Sub-Category")["Profit"].sum().sort_values()
discount_bins = pd.cut(df["Discount"], [-0.01, 0, 0.2, 1], labels=["No discount", "Low (≤20%)", "High (>20%)"])
discount_impact = df.groupby(discount_bins)["Profit"].mean()

print("\nTOTAL SALES:", round(total_sales, 2))
print("TOTAL PROFIT:", round(total_profit, 2))
print("MARGIN %:", round(margin, 2))
print("\nBY CATEGORY (sales):\n", by_category)
print("\nPROFIT BY CATEGORY:\n", profit_by_cat)
print("\nBY REGION:\n", by_region)
print("\nBY SEGMENT:\n", by_segment)
print("\nTOP 5 SUBCATS BY SALES:\n", top_subcats.head())
print("\nWORST 5 SUBCATS BY PROFIT (biggest losses):\n", loss_subcats.head())
print("\nDISCOUNT IMPACT ON AVG PROFIT:\n", discount_impact)

# ---------------- CHARTS ----------------
plt.figure(figsize=(7, 4))
by_month.plot(kind="line", marker="o", color="#2563eb", markersize=3)
plt.title("Monthly Sales Trend (2017–2020)")
plt.ylabel("Sales ($)")
plt.xlabel("Month")
plt.xticks(rotation=90, fontsize=6)
plt.tight_layout()
plt.savefig("/home/claude/rc_monthly_trend.png")
plt.close()

plt.figure(figsize=(6, 4))
profit_by_cat.plot(kind="bar", color=["#16a34a" if v > 0 else "#dc2626" for v in profit_by_cat])
plt.title("Total Profit by Category")
plt.ylabel("Profit ($)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("/home/claude/rc_profit_by_category.png")
plt.close()

plt.figure(figsize=(6, 4))
by_region.plot(kind="bar", color="#f59e0b")
plt.title("Total Sales by Region")
plt.ylabel("Sales ($)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("/home/claude/rc_sales_by_region.png")
plt.close()

plt.figure(figsize=(6, 4))
loss_subcats.head(6).plot(kind="barh", color="#dc2626")
plt.title("6 Least Profitable Sub-Categories")
plt.xlabel("Total Profit ($) — negative = loss")
plt.tight_layout()
plt.savefig("/home/claude/rc_worst_subcategories.png")
plt.close()

print("\nCharts saved.")

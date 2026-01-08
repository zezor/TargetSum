import pandas as pd
from itertools import combinations

# ===== SETTINGS =====
FILE = "transactions.xlsx"
TARGET = 17500   # <-- change this to your target total
MAX_ITEMS = 10   # limit combination size (important for speed)

# ====================

# Load data
df = pd.read_excel(FILE)

# Clean Amount column
df["Amount"] = (
    df["Amount"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .astype(float)
)

amounts = list(df["Amount"])
ids = list(df["ID"])

found = False

for r in range(1, MAX_ITEMS + 1):
    for combo in combinations(range(len(amounts)), r):
        total = sum(amounts[i] for i in combo)
        if abs(total - TARGET) < 0.01:
            print("\nMATCH FOUND ✅\n")
            for i in combo:
                print(f"ID: {ids[i]} | Amount: {amounts[i]}")
            print(f"\nTOTAL = {total}")
            found = True
            break
    if found:
        break

if not found:
    print("❌ No exact match found within limits.")

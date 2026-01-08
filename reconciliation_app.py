import streamlit as st
import pandas as pd
from itertools import combinations

st.set_page_config(page_title="Transaction Reconciliation App", layout="centered")

st.title("💰 Transaction Reconciliation Tool")
st.write("Upload an Excel file and find which transactions add up to a target amount.")

# File upload
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

# Target amount
target = st.number_input("Enter Target Amount", min_value=0.0, step=0.01)

# Max items
max_items = st.slider("Maximum number of transactions to combine", 3, 20, 5, help="Limit combination size for performance.")

if uploaded_file and target > 0:
    df = pd.read_excel(uploaded_file)

    # Clean Amount column
    df["Amount"] = (
        df["Amount"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    amounts = list(df["Amount"])
    ids = list(df["ID"])

    if st.button("🔍 Find Matching Transactions"):
        found = False
        with st.spinner("Searching..."):
            for r in range(1, max_items + 1):
                for combo in combinations(range(len(amounts)), r):
                    total = sum(amounts[i] for i in combo)
                    if abs(total - target) < 0.01:
                        result = df.iloc[list(combo)]
                        st.success("Match found!")
                        st.dataframe(result)
                        st.write(f"**Total:** {total}")
                        found = True
                        break
                if found:
                    break

        if not found:
            st.warning("No matching combination found within the selected limits.")

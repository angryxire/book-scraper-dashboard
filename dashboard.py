import streamlit as st
import pandas as pd

st.set_page_config(page_title="Book Inventory Intelligence", layout="wide")

st.title("Book Market Analytics Dashboard")
st.markdown("---")


@st.cache_data
def load_data():
	#try:
		df = pd.read_csv("scraped_properties.csv")

		df['Clean_Price'] = df['Price'].str.replace(r'[^\d.]','', regex=True).astype(float)
		return df

	#except Exception:
		return pd.DataFrame(columns=["Listing Title", "Price", "Description", "Cleaned_Price"])

df = load_data()

if df.empty:
	st.warning("No data found. Please execute main.py first to parse the online catalog")
else:

	avg_price = df['Clean_Price'].mean()
	max_price = df['Clean_Price'].max()
	min_price = df['Clean_Price'].min()
	total_books = len(df)

	col1, col2, col3, col4 = st.columns(4)
	col1.metric("Total Titles Tracked", f"{total_books}")
	col2.metric("Average Book Price", f"${avg_price:.2f}")
	col3.metric("Highest Priced Book", f"${max_price:.2f}")
	col4.metric("Lowest Priced Book", f"${min_price:.2f}")

	st.markdown("---")

	st.sidebar.header(" Inventory Filter")


	search_query = st.sidebar.text_input("Search Book Title")

	max_budget = st.sidebar.slider(
		"Maximum Allowed Price",
		float(min_price),
		float(max_price),
		float(max_price)
	)

	filtered_df = df[df['Clean_Price'] <= max_budget]
	if search_query:
		filtered_df = filtered_df[filtered_df['Listing Title'].str.contains(search_query, case=False)]


	st.subheader("Catalog Inventory Record")
	st.dataframe(
		filtered_df[["Listing Title", "Price", "Description"]],
		use_container_width = True
	)

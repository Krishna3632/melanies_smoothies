import streamlit as st
from snowflake.snowpark.functions import col
import requests

st.title("Customize Your Smoothie")

# --- Snowflake connection ---
cnx = st.connection("my_connection", type="snowflake")
session = cnx.session()

# --- User input ---
name_on_order = st.text_input("Name on smoothie:")

# --- Fetch fruit options from Snowflake ---
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
fruit_rows = my_dataframe.collect()
fruit_list = [row['FRUIT_NAME'] for row in fruit_rows]

# --- Multi-select ---
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

ingredients_string = " ".join(ingredients_list)

# --- Fetch fruit nutrition (API) ---
if ingredients_list:
    st.subheader("Nutritional Info")

    for fruit in ingredients_list:
        try:
            url = f"https://my.smoothiefroot.com/api/fruit/{fruit.lower()}"
            response = requests.get(url)

            if response.status_code == 200:
                st.write(f"**{fruit}**")
                st.json(response.json())
            else:
                st.warning(f"Could not fetch data for {fruit}")

        except Exception as e:
            st.error(f"API error for {fruit}: {e}")

# --- Submit order ---
time_to_insert = st.button("Submit Order")

if time_to_insert:
    if not name_on_order or not ingredients_list:
        st.error("Name and ingredients are required.")
    else:
        try:
            my_insert_stmt = """
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES (?, ?)
            """
            session.sql(
                my_insert_stmt,
                params=[ingredients_string, name_on_order]
            ).collect()

            st.success("Your Smoothie is ordered!", icon="✅")

        except Exception as e:
            st.error(f"Order failed: {e}")

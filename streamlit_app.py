import streamlit as st
from snowflake.snowpark.functions import col

st.title("Customize")

cnx = st.connection("my_connection", type="snowflake")
session = cnx.session()

name_on_order = st.text_input("Name on smoothie:")

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

fruit_rows = my_dataframe.collect()
fruit_list = [row['FRUIT_NAME'] for row in fruit_rows]

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

ingredients_string = ' '.join(ingredients_list)

time_to_insert = st.button('Submit Order')

if time_to_insert:
    if not name_on_order or not ingredients_list:
        st.error("Name and ingredients are required.")
    else:
        my_insert_stmt = """
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES (?, ?)
        """
        session.sql(my_insert_stmt, params=[ingredients_string, name_on_order]).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

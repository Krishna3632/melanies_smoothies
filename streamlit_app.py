# Import python packages.
import streamlit as st

# Write directly to the app.
from snowflake.snowpark.functions import col
# from snowflake import pandas
import pandas as pd
import numpy as np
st.title(f"Customize")




# Create a database connection to Snowflake.


# Create a Snowpark session from the connection.
# This provides a few helpers on top of a standard Python connection.
# If you want to use a plain Snowflake connection instead, you can create
# one with conn.cursor().

cnx = st.connection("snowflake")
session = cnx.session()
name_on_order = st.text_input("Name on smoothie: ")
st.write("The name on smoothie will be",name_on_order)
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingedients:',
    my_dataframe,
    max_selections=5
)
if ingredients_list:
       # st.write(ingredients_list)
       # st.text(ingredients_list)
       ingredients_string = ''
       for i in ingredients_list:
           ingredients_string+=i + ' '
       st.write(ingredients_string)
       my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""
       time_to_insert = st.button('Submit Order')
    
       # st.write(my_insert_stmt)
       if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")

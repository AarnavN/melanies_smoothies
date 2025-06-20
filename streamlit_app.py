# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_smoothie = st.text_input('Name on the smoothie' , 'John')
st.write('Name on your smoothie will be ', name_on_smoothie)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for a in ingredients_list:
        st.subheader(a + " Nutrient information")
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == a, 'SEARCH_ON'].iloc[0]
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
        ingredients_string += a + ' ';
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
  

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_smoothie + """')"""
    
    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ,' + name_on_smoothie, icon="✅")






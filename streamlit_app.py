# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f":ghost: Customize Your Smoothie :ghost: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be :", name_on_order)

#option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)
#
#st.write("Your favorite fruit is:", option)

from snowflake.snowpark.functions import col

#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME') ,col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df.my_dataframe.to_pandas()
st.my_dataframe(pd_df);
st.stop()

ingredients_list = st.multiselect('Chosse up to 5 ingredient :', my_dataframe, max_selections=5)


#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

#smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/all")
#st.text(smoothiefroot_response.json())


if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+ name_on_order +'!', icon="✅")

    

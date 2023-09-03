import streamlit
import pandas as pd
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title("My Parents New Healthy Diner!!")
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")
fruits_selected = streamlit.multiselect("Pick some fruits",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
    # write your own comment -what does the next line do? 
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    # write your own comment - what does this do?
    streamlit.dataframe(fruityvice_normalized)
    #streamlit.write('The user entered ', fruit_choice)
except URLError as e:
  streamlit.error(e)





def isnert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    statement =f"insert into fruit_load_list values (\'{new_fruit}\')"
    streamlit.text(statement)
    my_cur.execute(statement)
    return ("Thanks for adding "+ new_fruit)
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button("Add fruit to the list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)
# my_cur.execute("SELECT * from fruit_load_list")
# my_data_row = my_cur.fetchall()
# streamlit.header("The fruit load list contains:")
# streamlit.dataframe(my_data_row)


streamlit.write('Thanks for adding', add_my_fruit)

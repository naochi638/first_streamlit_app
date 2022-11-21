import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit') # index is set to fruit for the multiselect thing


streamlit.title("My Mum's New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Kiwifruit'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# New Seaction to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  # streamlit.text(fruityvice_response.json()) just writes data to the screen
  fruit_choice = streamlit.text_input('What fruit would you like information about?') # input()
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else: 
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice) # normalises the json 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized) # outputs it as a table/dataframe

except URLError as e:
  streamlit.error()
# streamlit.write('The user entered ', fruit_choice)

streamlit.stop ()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall() # can do fetchone
streamlit.text("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'Longan')
my_cur.execute("insert into fruit_load_list values 
streamlit.write('Thanks for adding', add_my_fruit)

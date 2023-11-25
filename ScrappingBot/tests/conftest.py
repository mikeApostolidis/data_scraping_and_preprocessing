import pytest
from selenium import webdriver
import mysql.connector


# @pytest.fixture()  # executes once before every test
# def driver():
#     print("Creating Chrome Driver")
#     chrome_options = webdriver.ChromeOptions()
#
#     prefs = {"download.default_directory": r"C:\Users\mike2\OneDrive\Desktop\sxoli"} #change default download dir
#     chrome_options.add_experimental_option("prefs", prefs)
#
#     chrome_options.add_argument("--headless=new")
#
#     my_driver = webdriver.Chrome(options=chrome_options)
#     yield my_driver  # yield instead return, code before yield will execute before test, code after test will execute after test
#     print("Closing Chrome Driver")
#     my_driver.quit()


@pytest.fixture()  # executes once before every test
def driver():
    print("Creating Chrome Driver")

    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": r"C:\Users\mike2\OneDrive\Desktop\sxoli"}  # change default download dir
    chrome_options.add_experimental_option("prefs", prefs)
    my_driver = webdriver.Chrome(options=chrome_options)

    yield my_driver  # yield instead return, code before yield will execute before test, code after test will execute after test
    print("Closing Chrome Driver")
    my_driver.quit()


@pytest.fixture()  # executes once before every test
def connect_to_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="eanaplirotes",
        password="eanaplirotes2023"
    )
    # Creating an instance of 'cursor' class
    # which is used to execute the 'SQL'
    # statements in 'Python'
    print("Connected to database")
    cursor = mydb.cursor()
    yield cursor


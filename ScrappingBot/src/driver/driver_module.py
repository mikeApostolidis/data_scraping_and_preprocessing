from selenium import webdriver


def driver_fun():
    print("Creating Chrome Driver")

    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": r"C:\sxoli\preprocess_folder"}  # change default download dir
    chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("--headless=new") # comment it if you want headless=false
    my_driver = webdriver.Chrome(options=chrome_options)
    yield my_driver  # yield instead return, code before yield will execute before test, code after test will execute after test
    print("Closing Chrome Driver")
    my_driver.quit()



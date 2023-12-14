import os
import shutil
import time

from selenium.common import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains, Keys

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from ScrappingBot.src.driver.driver_module import driver_fun

from unidecode import unidecode
import re

from datetime import datetime

import ScrappingBot.src.settings as settings


def normalize_greek_text(text):
    # Normalize Greek text to English and convert to lowercase.
    return unidecode(text).lower()


def locate_date_from_string_and_normalize_it(text):
    # Define a regex pattern for the date in the format DD-MM-YY
    date_pattern = r'\b\d{2}-\d{2}-\d{2}\b'

    # Find all occurrences of the pattern in the title
    matches = re.findall(date_pattern, text)

    # Parse the input date string
    parsed_date = datetime.strptime(matches[0], "%d-%m-%y")

    # Format the parsed date as "YYYY-MM-DD"
    normalized_date = parsed_date.strftime("%Y-%m-%d")

    return normalized_date


def is_file_downloaded(download_path, timeout=60):
    start_time = time.time()

    while time.time() - start_time < timeout:
        if os.listdir(download_path):
            return True
        time.sleep(1)  # Adjust the sleep interval if needed

    return False


def add_date_into_file_name(download_path, date_string, last_downloaded_file):
    # Get the filename without the path
    filename = os.path.basename(last_downloaded_file)

    # Construct the new filename using the provided date and the original filename
    new_filename = f"{date_string}_{filename}"

    # Construct the full path of the new file with the correct Excel extension
    new_filepath = os.path.join(download_path, new_filename)

    # Check if the source file exists before attempting to rename
    if not os.path.exists(last_downloaded_file):
        print(f"Source file '{last_downloaded_file}' not found.")
        # return
    try:
        # Move the file to the new path
        os.rename(last_downloaded_file, new_filepath)
        # print(f"File renamed to {new_filename}")
    except FileNotFoundError:
        print(f"Source file '{last_downloaded_file}' not found.")
    except PermissionError:
        print(f"Permission error: Unable to rename file.")
    except Exception as e:
        print(f"An error occurred during renaming: {e}")


def add_orario_into_file_name(download_path, orario_string, last_downloaded_file):
    # Get the filename without the path
    filename = os.path.basename(last_downloaded_file)

    # Construct the new filename using the provided date and the original filename
    new_filename = f"{orario_string}_{filename}"

    # Construct the full path of the new file with the correct Excel extension
    new_filepath = os.path.join(download_path, new_filename)

    # Check if the source file exists before attempting to rename
    if not os.path.exists(last_downloaded_file):
        print(f"Source file '{last_downloaded_file}' not found.")
        # return
    try:
        # Move the file to the new path
        os.rename(last_downloaded_file, new_filepath)
        # print(f"File renamed to {new_filename}")
    except FileNotFoundError:
        print(f"Source file '{last_downloaded_file}' not found.")
    except PermissionError:
        print(f"Permission error: Unable to rename file.")
    except Exception as e:
        print(f"An error occurred during renaming: {e}")


def get_last_downloaded_file(download_path):
    # Get the list of files in the download directory
    files_in_directory = os.listdir(download_path)

    # Filter files to include only the desired file type (e.g., ".xlsx")
    files = [file for file in files_in_directory if file.endswith(".xlsx")]

    # Find the file with the latest creation time
    downloaded_file = max(files, key=lambda x: os.path.getctime(os.path.join(download_path, x)))

    last_downloaded_file = os.path.join(download_path, downloaded_file)

    # print("from get last downloaded file: ", downloaded_file)

    return last_downloaded_file


def scrap(max_date):
    # Extract the date object from the result set
    date_to_compare2 = max_date[0][0]
    date_to_compare = "2023-09-01"
    date_to_compare = datetime.strptime(date_to_compare, '%Y-%m-%d').date()
    print(date_to_compare)
    download_path = settings.folder_path
    global date_for_preprocess, orario_value
    obj_date = None

    # Create the driver generator
    driver_generator = driver_fun()

    # Get the driver from the generator
    driver = next(driver_generator)

    driver.get("https://www.minedu.gov.gr/")

    driver.find_element("xpath", '//*[@id="zentools-1085"]/ul/li/ul/li[6]/a').click()

    while True:
        current_url = driver.current_url

        wait = WebDriverWait(driver, 10)

        tbody_element = wait.until(ec.presence_of_element_located((By.XPATH, "//tbody")))

        tr_elements = tbody_element.find_elements(By.TAG_NAME, "tr")

        for tr_element in tr_elements:
            try:
                td_element = tr_element.find_element(By.TAG_NAME, "td")

                # Find the <a> tag within the <td>
                a_tag = td_element.find_element(By.XPATH, ".//a")

                # Get the text from the <a> tag
                a_tag_text = a_tag.text

                # normalize word
                proslipsis_key_word = normalize_greek_text(a_tag_text)

                if "proslepseis" in proslipsis_key_word or "proslepse" in proslipsis_key_word:
                    print("clicked: ", a_tag_text)
                    date_for_preprocess = locate_date_from_string_and_normalize_it(a_tag_text)
                    obj_date = datetime.strptime(date_for_preprocess, '%Y-%m-%d')
                    obj_date = obj_date.date()
                    print("date object: ", obj_date)
                    # opens new window
                    time.sleep(1)
                    ActionChains(driver).move_to_element(a_tag).key_down(
                        Keys.CONTROL
                    ).click().key_up(Keys.CONTROL).perform()
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(1)
                    # print("anoikse allo parathiro kai kane focus ")

                    # Execute JavaScript to get the entire text content of the page
                    page_text = driver.execute_script("return document.body.innerText;")

                    normalized_page_text = normalize_greek_text(page_text)

                    # print(normalized_page_text)

                    # Check if the keyword is present in the normalized text
                    if "plerous orariou" in normalized_page_text:
                        orario_value = "ΑΠΩ"
                        print("Keyword found on the page!", orario_value)
                    else:
                        print("Keyword not found on the page.")
                    try:
                        # download .xlsx files:
                        xlsx_links_xpath = "//a[contains(@href, '.xlsx')]"

                        # Find all <a> tags matching the XPath expression
                        xlsx_links = wait.until(
                            ec.presence_of_all_elements_located(
                                (By.XPATH, xlsx_links_xpath)
                            )
                        )
                        for link in xlsx_links:
                            # stale element stin periptosei pou den vrei xlsx
                            link.click()

                            # Introduce a delay before renaming
                            time.sleep(2)

                            last_downloaded_file = get_last_downloaded_file(download_path)

                            try:
                                add_orario_into_file_name(download_path, orario_value, last_downloaded_file)
                                orario_value = None
                            except Exception as e:
                                print("Somethings worng with add_orario_into_file_name: ", {e})

                            last_downloaded_file = get_last_downloaded_file(download_path)
                            add_date_into_file_name(download_path, date_for_preprocess, last_downloaded_file)
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        # timeout exception
                    except TimeoutException as e:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        print("TimeoutException with finding excel files:", {e})
                    except Exception as e:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        print("Something is wrong with not finding excel files:", {e})

                    # desired_patterns = [
                    #     ["proslepseis", "genikes", "de"],
                    #     ["proslepseis", "genikes", "pe"],
                    #     ["proslepseis", "mousika"],
                    #     ["edo"],
                    # ]

                if obj_date == date_to_compare:
                    print("eftasa!")
                    driver.quit()

            except StaleElementReferenceException as e:
                print("Stale element reference; element is no longer valid", e)

        else:
            try:
                next_page_link = driver.find_element(
                    By.PARTIAL_LINK_TEXT, "Επόμενο"
                )

                next_page_link.click()

                wait.until(ec.url_changes(current_url))

                next_url = driver.current_url

                if current_url == next_url:
                    raise Exception
            except Exception as e:
                print(
                    "No 'Epomeno' link found; end of pages reached, now Exiting",
                    e,
                )
                driver.quit()

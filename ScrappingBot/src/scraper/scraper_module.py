import os
import shutil
import time
import traceback

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

import patoolib

from selenium import webdriver


def normalize_greek_text(text):
    # Normalize Greek text to English and convert to lowercase.
    return unidecode(text).lower()


def locate_date_from_string_and_normalize_it(text):
    # Define a regex pattern for the date in the format DD-MM-YY or DD-MM-YYYY
    date_pattern = r'\b\d{1,2}\s*-\s*\d{1,2}\s*-\s*\d{2,4}\b'

    # Find all occurrences of the pattern in the title
    matches = re.findall(date_pattern, text)

    if not matches:
        print(f"No matches found for text: {text}")
        return None

    try:
        # Parse the input date string
        date_str = matches[0]
        date_parts = date_str.split('-')

        if len(date_parts[2]) == 2:
            format_str = "%d-%m-%y"
        else:
            format_str = "%d-%m-%Y"

        # Remove spaces and parse the date
        date_str_no_space = '-'.join(date_parts).replace(' ', '')
        parsed_date = datetime.strptime(date_str_no_space, format_str)

        normalized_date = parsed_date.strftime("%Y-%m-%d")
        return normalized_date
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


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
    # print("filename: ", filename)

    # Construct the new filename using the provided date and the original filename
    new_filename = f"{orario_string}_{filename}"
    print("orario string: ", orario_string)
    # print("new filename: ", new_filename)

    # Construct the full path of the new file with the correct Excel extension
    new_filepath = os.path.join(download_path, new_filename)
    # print("new filepath :", new_filepath)

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
    files = [file for file in files_in_directory if file.endswith((".xlsx", ".rar"))]

    # Find the file with the latest creation time
    downloaded_file = max(files, key=lambda x: os.path.getctime(os.path.join(download_path, x)))

    last_downloaded_file = os.path.join(download_path, downloaded_file)

    # print("from get_last_downloaded() file: ", downloaded_file)

    return last_downloaded_file


def get_last_downloaded_fileRAR(download_path):
    # Get the list of files in the download directory
    files_in_directory = os.listdir(download_path)

    # Filter files to include only the desired file type (e.g., ".xlsx")
    files = [file for file in files_in_directory if file.endswith(".rar")]

    # Find the file with the latest creation time
    downloaded_file = max(files, key=lambda x: os.path.getctime(os.path.join(download_path, x)))

    last_downloaded_file = os.path.join(download_path, downloaded_file)

    # print("from get last downloaded file: ", downloaded_file)

    return last_downloaded_file


def scrap(max_date):
    zip_folder_process = settings.zip_folder_path
    # Extract the date object from the result set
    # date_to_compare = max_date[0][0]
    date_to_compare = max_date
    print(date_to_compare)
    date_to_compare2 = "2023-09-01"
    # date_to_compare = datetime.strptime(max_date[0][0], '%Y-%m-%d').date()

    download_path = settings.folder_path
    global date_for_preprocess, orario_value
    orario_value = None
    obj_date = None

    # Create the driver generator
    driver_generator = driver_fun()

    # Get the driver from the generator
    driver = next(driver_generator)

    driver.get("https://www.minedu.gov.gr/")

    driver.find_element("xpath", '//*[@id="zentools-1085"]/ul/li/ul/li[6]/a').click()

    # driver.get("https://www.minedu.gov.gr/news?start=3000")
    # driver.get("https://www.minedu.gov.gr/news?start=3150")

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
                    print("normalized date:", date_for_preprocess)
                    obj_date = datetime.strptime(date_for_preprocess, '%Y-%m-%d').date()
                    print("date object: ", obj_date)

                    if obj_date == date_to_compare:
                        # print("mpika stin if")
                        break
                    print("den mpika stin if")

                    # opens new window
                    # Open the link in a new tab using the "send_keys" method with Keys.CONTROL + Keys.RETURN
                    a_tag.send_keys(Keys.CONTROL + Keys.RETURN)
                    time.sleep(1)

                    # Switch to the newly opened tab
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(1)

                    # # opens new window
                    # time.sleep(1)
                    # ActionChains(driver).move_to_element(a_tag).key_down(
                    #     Keys.CONTROL
                    # ).click().key_up(Keys.CONTROL).perform()
                    # time.sleep(1)
                    # driver.switch_to.window(driver.window_handles[1])
                    # time.sleep(1)

                    # Execute JavaScript to get the entire text content of the page
                    page_text = driver.execute_script("return document.body.innerText;")

                    normalized_page_text = normalize_greek_text(page_text)

                    # print(normalized_page_text)
                    keywords_to_check = {
                        "anaplerotes",
                        "anapleroton",
                        "anapliroton",
                        "anaplerotis",
                        "anaplirotis",
                        "ekpaideutikon",
                        "ekpaideutikous",
                        "ekpaideutikoi"
                    }
                    if any(keyword in normalized_page_text for keyword in keywords_to_check):
                        # if "anaplerotes" in normalized_page_text or "anapleroton" in normalized_page_text or "anapliroton" in normalized_page_text or "anaplerotis" in normalized_page_text or "ekpaideutikon" in normalized_page_text or "ekpaideutikous" in normalized_page_text or "ekpaideutikoi" in normalized_page_text:

                        # print("mpika stin 1h if")

                        # Check if the keyword is present in the normalized text
                        if "plerous orariou" in normalized_page_text:
                            orario_value = "ΑΠΩ"
                            print("Keyword found on the page!", orario_value)
                        elif "meiomenou orariou" in normalized_page_text:
                            orario_value = "ΑΜΩ"
                            print("Keyword found on the page!", orario_value)
                        else:
                            print("Keyword not found on the page.")
                        try:
                            # download .xlsx files:
                            # xlsx_links_xpath = "//a[contains(@href, '.xlsx')]"
                            rar_links_xpath = "//a[contains(@href, '.rar')]"
                            # Combine both XPaths using the OR operator (|) to select elements that match either condition
                            combined_xpath = "//a[contains(@href, '.rar') or contains(@href, '.xlsx')]"

                            try:
                                # xlsx_links = wait.until(
                                #     ec.presence_of_all_elements_located((By.XPATH, xlsx_links_xpath)))

                                # rar_links = wait.until(
                                #     ec.presence_of_all_elements_located((By.XPATH, rar_links_xpath)))

                                # Wait for the presence of all elements matching the combined XPath
                                links = wait.until(ec.presence_of_all_elements_located((By.XPATH, combined_xpath)))

                            except StaleElementReferenceException:

                                # Wait for the presence of all elements matching the combined XPath
                                links = wait.until(ec.presence_of_all_elements_located((By.XPATH, combined_xpath)))
                                # Try locating the elements again
                                # xlsx_links = wait.until(
                                #     ec.presence_of_all_elements_located((By.XPATH, xlsx_links_xpath)))

                                # rar_links = wait.until(
                                #     ec.presence_of_all_elements_located((By.XPATH, rar_links_xpath)))

                            for link in links:
                                # Check if the element is interactable before clicking
                                if link.is_displayed() and link.is_enabled():
                                    # print("checkara ta links: ")
                                    link.click()
                                    print("downloaded: ", link.text)

                                else:
                                    print("Element is not interactable:", link.text)

                                    # # Handle .rar file
                                    # for link in rar_links:
                                    #     # Check if the element is interactable before clicking
                                    #     if link.is_displayed() and link.is_enabled():
                                    #         link.click()
                                    #         print("downloaded: ", link.text)
                                    #     else:
                                    #         print("Element is not interactable:", link.text)

                                # Introduce a delay before renaming
                                time.sleep(2)

                                # Handle rar files
                                # handleRarFile = get_last_downloaded_fileRAR(download_path)

                                last_downloaded_file = get_last_downloaded_file(download_path)
                                # print("last file that got downloaded: ", last_downloaded_file)

                                # patoolib.extract_archive(last_downloaded_file, outdir=download_path)

                                try:
                                    add_orario_into_file_name(download_path, orario_value, last_downloaded_file)
                                    orario_value = None
                                except Exception as e:
                                    print("Somethings wrong with add_orario_into_file_name: ", {e})
                                #  update the name of the last file
                                last_downloaded_file = get_last_downloaded_file(download_path)
                                add_date_into_file_name(download_path, date_for_preprocess, last_downloaded_file)
                                #  update the name of the last file
                                last_downloaded_file = get_last_downloaded_file(download_path)
                                if last_downloaded_file.endswith(".rar"):

                                    source_file = os.path.dirname(last_downloaded_file)
                                    # print(source_file)

                                    # move .rar to the other folder in order to handle it better
                                    last_downloaded_file = get_last_downloaded_file(download_path)
                                    new_directory_path = os.path.join(download_path,
                                                                      os.path.basename(last_downloaded_file))

                                    # print(new_directory_path)
                                    new_rar_path = shutil.move(new_directory_path, zip_folder_process)
                                    print(": ", new_rar_path)

                                    # to metafero mesa stin for gia na min exei thema me ta onomata
                                    # # Get the prefix from the filename (until the second '_')
                                    # prefix = new_rar_path.split('_')[0] + '_' + new_rar_path.split('_')[1] + '_'

                                    patoolib.extract_archive(new_rar_path, outdir=zip_folder_process, verbosity=1)

                                    # Reset original_prefix for the new .rar file
                                    original_prefix = ""

                                    # Rename each extracted file one by one
                                    for filename in os.listdir(zip_folder_process):
                                        if filename.endswith(".xlsx"):
                                            # Get the prefix from the original file name (until the second '_')
                                            original_prefix = os.path.basename(last_downloaded_file).split('_')[
                                                                  0] + '_' + \
                                                              os.path.basename(last_downloaded_file).split('_')[1] + '_'

                                            current_path = os.path.join(zip_folder_process, filename)
                                            new_filename = original_prefix + filename
                                            new_path = os.path.join(zip_folder_process, new_filename)
                                            os.rename(current_path, new_path)
                                    # Move a copy of the renamed files to the download_path folder
                                    for filename in os.listdir(zip_folder_process):
                                        if filename.endswith(".xlsx"):
                                            current_path = os.path.join(zip_folder_process, filename)
                                            new_path = os.path.join(download_path, filename)
                                            shutil.copy(current_path, new_path)

                                            # Delete the .xlsx file in the zip_folder_process
                                            os.remove(current_path)
                                else:
                                    print("not found")

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
                            traceback.print_exc()
                    else:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
            except StaleElementReferenceException as e:
                print("Stale element reference; element is no longer valid", e)
                traceback.print_exc()

        if obj_date == date_to_compare:
            print("eftasa!")
            # breaks to driver.quit
            break

        # 'else' block belongs to the 'for' loop
        try:
            next_page_link = driver.find_element(
                By.XPATH, '//*[@id="adminForm"]/div/ul/li[13]/a'
            )
            next_page_link.click()
            wait.until(ec.url_changes(current_url))
            next_url = driver.current_url

            if current_url == next_url:
                raise TimeoutException("No 'Epomeno' link found; end of pages reached")

        except TimeoutException as e:
            print(e)
            # If 'Epomeno' link is not found, exit the loop and quit the driver
            # breaks to driver.quit
            break

    print("Now exiting...")
    driver.quit()

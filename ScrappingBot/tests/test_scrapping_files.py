import time

import pytest
# from mysql.connector import cursor
from selenium.common import StaleElementReferenceException
from selenium.webdriver import ActionChains, Keys

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import pandas as pd
import os

from unidecode import unidecode


def normalize_greek_text(text):
    # Normalize Greek text to English and convert to lowercase.
    return unidecode(text).lower()


class TestScrappingPage:
    input_folder = r"C:\Users\mike2\OneDrive\Desktop\sxoli"

    # @pytest.mark.scrap
    def test_land_first_page(self, driver, connect_to_db):
        driver.get("https://www.minedu.gov.gr/")
        # connect_to_db.execute("SHOW TABLES")
        # for x in connect_to_db:
        #     print(x)

    # @pytest.mark.scrap
    def test_navigate_to_page(self, driver):
        driver.find_element("xpath", '//*[@id="zentools-1085"]/ul/li/ul/li[6]/a').click()
        print("navigated")

    @pytest.mark.scrap
    def test_scrap(driver):
        driver.get("https://www.minedu.gov.gr/")



        driver.find_element("xpath", '//*[@id="zentools-1085"]/ul/li/ul/li[6]/a').click()

        while True:
            current_url = driver.current_url

            wait = WebDriverWait(driver, 10)

            tbody_element = wait.until(ec.presence_of_element_located((By.XPATH, "//tbody")))
            # tbody_element = self.find_element((By.XPATH, "//tbody"))

            tr_elements = tbody_element.find_elements(By.TAG_NAME, "tr")

            for tr_element in tr_elements:
                try:
                    td_element = tr_element.find_element(By.TAG_NAME, "td")

                    # Find the <a> tag within the <td>
                    a_tag = td_element.find_element(By.XPATH, ".//a")

                    # Get the text from the <a> tag
                    a_tag_text = a_tag.text

                    #normalize word
                    proslipsis_key_word = normalize_greek_text(a_tag_text)

                    if "proslepseis" in proslipsis_key_word:
                        print("clicked: ", a_tag_text)
                        # opens new window
                        time.sleep(1)
                        ActionChains(driver).move_to_element(a_tag).key_down(
                            Keys.CONTROL
                        ).click().key_up(Keys.CONTROL).perform()
                        time.sleep(1)
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(1)
                        # print("anoikse allo parathiro kai focus ")

                        # download .xlsx files:
                        xlsx_links_xpath = "//a[contains(@href, '.xlsx')]"

                        # Find all <a> tags matching the XPath expression
                        xlsx_links = wait.until(
                            ec.presence_of_all_elements_located(
                                (By.XPATH, xlsx_links_xpath)
                            )
                        )

                        desired_patterns = [
                            ["proslepseis", "genikes", "de"],
                            ["proslepseis", "genikes", "pe"],
                            ["proslepseis", "mousika"],
                            ["edo"],
                        ]

                        for link in xlsx_links:
                            link_text = link.text

                            normalized_into_english = normalize_greek_text(link_text)

                            normalized_final = normalized_into_english.replace('_', ' ')
                            print(normalized_final)

                            # Check if the normalized text matches any desired pattern
                            for pattern in desired_patterns:
                                if all(word in normalized_final for word in pattern):
                                    link.click() #downloads desired xlsx_link

                        # closes the new tab
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    # print("ekleisa to neo tab kai ekana focus sto prwto")
                # else:
                # print("den to patisa :", a_tag_text)

                except StaleElementReferenceException as e:
                    print("Stale element reference; element is no longer valid", e)

            else:
                try:
                    next_page_link = driver.find_element(
                        By.PARTIAL_LINK_TEXT, "Επόμενο"
                    )

                    next_page_link.click()
                    # print("Patisa to epomeno link")
                    wait.until(ec.url_changes(current_url))

                    next_url = driver.current_url

                    if current_url == next_url:
                        # print("Eimai mesa sthn if")
                        raise Exception
                except Exception as e:
                    print(
                        "No 'Epomeno' link found; end of pages reached, now Exiting",
                        e,
                    )
                    driver.quit()

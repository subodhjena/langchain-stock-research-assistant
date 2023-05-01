import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_all_links(url: str) -> List[str]:
    """
    Takes in a URL and returns a list of all the links found in the div with the
    class "topictab_cnot" after removing the div with the class "pagenation".

    Input:
        url (str)

    Output:
        links (List[str]): A list of all the links found in the specified div
    """

    # Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Select chrome as the browser
    driver = webdriver.Chrome(options=chrome_options)

    # Load the URL
    driver.get(url)

    links = []
    try:
        # Remove the div with the class "pagenation"
        pagenation_element = driver.find_element(By.CLASS_NAME, "pagenation")
        driver.execute_script("arguments[0].remove();", pagenation_element)

        # Get the div with the class "topictab_cnot"
        topictab_cnot_element = driver.find_element(
            By.CLASS_NAME, "topictab_cnot")

        # Find all the links in the div
        link_elements = topictab_cnot_element.find_elements(By.TAG_NAME, "a")

        # Extract the href attribute for each link
        links = [link.get_attribute("href") for link in link_elements]

    except NoSuchElementException:
        print("No element found. Continuing...")

    # Close the WebDriver
    driver.quit()

    return links


def process_url(url: str, folder_path: str, elements_to_ignore=None, classes_to_ignore=None, ids_to_ignore=None):
    """
    Takes in a url and copies the content of the page using selenium webdriver

    Input:
        url (str)
        folder_path (str)
        elements_to_ignore (list): List of element tags to ignore
        classes_to_ignore (list): List of classes to ignore
        ids_to_ignore (list): List of ids to ignore

    Output:
        page_text (str): Text content of the page
    """

    if elements_to_ignore is None:
        elements_to_ignore = []
    if classes_to_ignore is None:
        classes_to_ignore = []
    if ids_to_ignore is None:
        ids_to_ignore = []

    # Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Select chrome as the browser
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load the url
        driver.get(url)

        # Remove elements based on the given criteria
        for element in elements_to_ignore:
            try:
                elements = driver.find_elements(By.TAG_NAME, element)
                for el in elements:
                    driver.execute_script("arguments[0].remove();", el)
            except NoSuchElementException:
                pass

        for class_name in classes_to_ignore:
            try:
                elements = driver.find_elements(By.CLASS_NAME, class_name)
                for el in elements:
                    driver.execute_script("arguments[0].remove();", el)
            except NoSuchElementException:
                pass

        for id_name in ids_to_ignore:
            try:
                element = driver.find_element(By.ID, id_name)
                driver.execute_script("arguments[0].remove();", element)
            except NoSuchElementException:
                pass

        # Get the text content of the page
        page_text = driver.find_element(By.TAG_NAME, "body").text
        return page_text
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
    finally:
        # Close the WebDriver
        driver.quit()


async def process_urls_async(urls: List[str], folder_path: str, elements_to_ignore=None, classes_to_ignore=None, ids_to_ignore=None):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        tasks = [
            loop.run_in_executor(
                executor,
                process_url,
                url,
                folder_path,
                elements_to_ignore,
                classes_to_ignore,
                ids_to_ignore
            )
            for url in urls
        ]
        results = await asyncio.gather(*tasks)

        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)

        # Save the text content as UTF-8 encoded text in the specified folder
        file_name = "data.txt"
        with open(os.path.join(folder_path, file_name), "w", encoding="utf-8") as f:
            for result in results:
                f.write(result)
                f.write("\n\n========================================\n\n")

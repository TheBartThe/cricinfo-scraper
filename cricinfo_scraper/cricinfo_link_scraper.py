"""
Scrape IPL data from cricinfo website

Functions:
    get_links() -> List[str]
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from typing import List


def get_links() -> List[str]:
    """
    Gets links from cricinfo website to scorecards.
            Returns:
                    links (List[str]): A list of links to scorecards
    """
    with make_driver() as driver:
        driver = get_cricinfo_driver(driver)
        links: List[str] = get_all_links(driver)
        return links


def make_driver() -> webdriver:
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    return driver


def get_cricinfo_driver(driver: webdriver) -> webdriver:
    driver.get(
            "https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/match-results"
        )
    return driver


def get_all_links(driver) -> List[str]:
    links: List[str] = driver.find_elements(
        By.CSS_SELECTOR,
        "a[href^='/series/indian-premier-league-2022-1298423/'][href$='full-scorecard']",
    )
    links = [link.get_attribute("href") for link in links]
    return links

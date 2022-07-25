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
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    with webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    ) as driver:
        driver.get(
            "https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/match-results"
        )
        assert "cricinfo" in driver.title
        links: List[str] = driver.find_elements(
            By.CSS_SELECTOR,
            "a[href^='/series/indian-premier-league-2022-1298423/'][href$='full-scorecard']",
        )
        return links

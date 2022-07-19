"""
Scrape IPL data from cricinfo website
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")

with webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
) as driver:
    driver.get("https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/match-results")
    assert "cricinfo" in driver.title
    links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/series/indian-premier-league-2022-1298423/'][href$='full-scorecard']")
    for link in links:
        print(link.get_attribute("href"))
    print(len(links))

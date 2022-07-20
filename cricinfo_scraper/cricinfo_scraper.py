"""
Scrape IPL data from cricinfo website
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

chrome_options = Options()
chrome_options.add_argument("--headless")

with webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
) as driver:
    driver.get("https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/gujarat-titans-vs-rajasthan-royals-final-1312200/full-scorecard")
    columns = driver.find_element(By.CSS_SELECTOR, "table.ds-w-full.ds-table.ds-table-xs.ds-table-fixed.ci-scorecard-table thead tr.ds-border-b.ds-border-line.ds-text-tight-s")
    columns = columns.find_elements(By.CSS_SELECTOR, "th")
    del columns[1]
    columns = [element.get_attribute("innerHTML") for element in columns]
    batters = driver.find_elements(By.CSS_SELECTOR, "table.ds-w-full.ds-table.ds-table-xs.ds-table-fixed.ci-scorecard-table tbody tr.ds-border-b.ds-border-line.ds-text-tight-s")
    print(",".join(columns))
    for batter in batters:
        try:
            name = batter.find_element(By.CSS_SELECTOR, "span.ds-inline-flex.ds-items-center.ds-leading-none a.ds-text-ui-typo.ds-underline.ds-underline-offset-4.ds-decoration-ui-stroke").get_attribute("title")
            #runs, balls, minutes, fours, sixes, strike_rate = (element.text for element in batter.find_elements(By.CSS_SELECTOR, "td.ds-min-w-max.ds-text-right"))
            runs = batter.find_element(By.CSS_SELECTOR, "td.ds-min-w-max.ds-text-right strong").get_attribute("innerHTML")
            content = [element.get_attribute("innerHTML") for element in batter.find_elements(By.CSS_SELECTOR, "td.ds-min-w-max.ds-text-right")[1:]]
            content.insert(0, runs)
            content.insert(0, name)
        except NoSuchElementException:
            pass
        else:
            print(','.join(content))

"""
Scrape IPL data from cricinfo website
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")

with webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
) as driver:
    driver.get(
        "https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/gujarat-titans-vs-rajasthan-royals-final-1312200/full-scorecard"
    )

    columns = driver.find_element(
        By.CSS_SELECTOR,
        "table.ds-w-full.ds-table.ds-table-xs.ds-table-fixed.ci-scorecard-table:first-of-type thead tr.ds-border-b.ds-border-line.ds-text-tight-s",
    )
    columns = columns.find_elements(By.CSS_SELECTOR, "th")
    columns = [element.get_attribute("innerHTML") for element in columns]
    print(",".join(columns))

    batters = driver.find_elements(
        By.CSS_SELECTOR,
        "table.ds-w-full.ds-table.ds-table-xs.ds-table-fixed.ci-scorecard-table tbody tr.ds-border-b.ds-border-line.ds-text-tight-s",
    )
    for batter in batters:
        try:
            name = batter.find_element(
                By.CSS_SELECTOR,
                "td.ds-min-w-max > span.ds-inline-flex.ds-items-center.ds-leading-none > a.ds-text-ui-typo.ds-underline.ds-underline-offset-4.ds-decoration-ui-stroke",
            ).get_attribute("title")
            # dismissal = batter.find_element(By.CSS_SELECTOR, "td.ds-min-w-max > span.ds-flex.ds-cursor-pointer.ds-items-center > span").get_attribute("innerHTML")
            # dismissal = batter.find_element(By.CSS_SELECTOR, "td.ds-min-w-max:nth-of-type(2)").get_attribute("innerHTML")
            runs = batter.find_element(
                By.CSS_SELECTOR, "td.ds-min-w-max.ds-text-right strong"
            ).get_attribute("innerHTML")
            content = [
                element.get_attribute("innerHTML")
                for element in batter.find_elements(
                    By.CSS_SELECTOR, "td.ds-min-w-max.ds-text-right"
                )[1:]
            ]
            try:
                dismissal = batter.find_element(
                    By.CSS_SELECTOR,
                    "td.ds-min-w-max > span.ds-flex.ds-cursor-pointer.ds-items-center > span",
                ).get_attribute("innerHTML")
            except NoSuchElementException:
                try:
                    dismissal = batter.find_element(
                        By.CSS_SELECTOR, "td.ds-min-w-max:nth-of-type(2)"
                    ).get_attribute("innerHTML")
                except NoSuchElementException:
                    pass
            content.insert(0, runs)
            content.insert(0, dismissal)
            content.insert(0, name)
        except NoSuchElementException:
            pass
        else:
            print(",".join(content))

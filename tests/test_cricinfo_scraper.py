from unittest.mock import patch, Mock
import pytest
import pandas as pd
from pandas import DataFrame
from pandas.testing import assert_frame_equal
from numpy import NaN
from cricinfo_scraper import __version__
from cricinfo_scraper.pandas_scraper import read_scorecard
from cricinfo_scraper.batters_cleaning import (
    clean_batters_dataframe,
    remove_unwanted_columns,
    remove_unwanted_rows,
    rename_columns,
    remove_dashes,
    clean_name,
    out_column,
    change_column_types,
)
from cricinfo_scraper.batters_totals import batters_totals
# from cricinfo_scraper.cricinfo_link_scraper import get_links, get_all_links
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from typing import List
# import os


@pytest.fixture
def split_df_1() -> DataFrame:
    return DataFrame(
        {
            "BATTING": [
                "Joe Root",
                "Virat Kholi (c)",
                NaN,
                "Virat Kholi",
                "Did not bat: Stuart Broad",
            ],
            "Unnamed: 1": ["not out", "caught", "dgdh", "not out", "run out"],
            "R": ["41", "12", "0", "51", "13"],
            "B": ["32", "31", "1", "7", "23"],
            "M": ["53", "42", "1", "-", "42"],
            "4s": ["4", "1", "5", "36", "59"],
            "6s": ["7", "4", "14", "4", "51"],
            "SR": ["84.24", "53.14", "103.24", "5.24", "6.42"],
            "Unnamed: 8": [NaN, "dsg", NaN, NaN, "rwg"],
            "Unnamed: 9": [NaN, "dsg", NaN, NaN, "rwg"],
        }
    )


@pytest.fixture
def split_df_2() -> DataFrame:
    return DataFrame(
        {
            "BATTING": [
                "Fall of wickets: dfrsgvsf",
                "Jos Buttler †",
                "Joe Root",
                "Sanga (c) †",
                "drop this",
            ],
            "Unnamed: 1": ["lbw", "bowled", "not out", "not out", "svfs"],
            "R": ["6", "132", "93", "221", "0"],
            "B": ["17", "103", "63", "148", NaN],
            "M": ["25", "124", "8", "103", "4"],
            "4s": ["64", "102", "12", "135", "8"],
            "6s": ["92", "193", "31", "241", "1"],
            "SR": ["40.52", "14.53", "152.52", "-", "204.41"],
            "Unnamed: 8": ["dfg", "fgds", NaN, "efg", NaN],
            "Unnamed: 9": ["dfg", "fgds", NaN, "efg", NaN],
        }
    )


@pytest.fixture
def dirty_df() -> DataFrame:
    return DataFrame(
        {
            "BATTING": [
                "Joe Root",
                "Virat Kholi (c)",
                NaN,
                "Virat Kholi",
                "Did not bat: Stuart Broad",
                "Fall of wickets: dfrsgvsf",
                "Jos Buttler †",
                "Joe Root",
                "Sanga (c) †",
                "drop this",
            ],
            "Unnamed: 1": [
                "not out",
                "caught",
                "dgdh",
                "not out",
                "run out",
                "lbw",
                "bowled",
                "not out",
                "not out",
                "svfs",
            ],
            "R": ["41", "12", "0", "51", "13", "6", "132", "93", "221", "0"],
            "B": ["32", "31", "1", "7", "23", "17", "103", "63", "148", NaN],
            "M": ["53", "42", "1", "-", "42", "25", "124", "8", "103", "4"],
            "4s": ["4", "1", "5", "36", "59", "64", "102", "12", "135", "8"],
            "6s": ["7", "4", "14", "4", "51", "92", "193", "31", "241", "1"],
            "SR": [
                "84.24",
                "53.14",
                "103.24",
                "5.24",
                "6.42",
                "40.52",
                "14.53",
                "152.52",
                "-",
                "204.41",
            ],
            "Unnamed: 8": [NaN, "dsg", NaN, NaN, "rwg", "dfg", "fgds", NaN, "efg", NaN],
            "Unnamed: 9": [NaN, "dsg", NaN, NaN, "rwg", "dfg", "fgds", NaN, "efg", NaN],
        }
    )


@pytest.fixture
def removed_columns_df() -> DataFrame:
    return DataFrame(
        {
            "BATTING": [
                "Joe Root",
                "Virat Kholi (c)",
                NaN,
                "Virat Kholi",
                "Did not bat: Stuart Broad",
                "Fall of wickets: dfrsgvsf",
                "Jos Buttler †",
                "Joe Root",
                "Sanga (c) †",
                "drop this",
            ],
            "Unnamed: 1": [
                "not out",
                "caught",
                "dgdh",
                "not out",
                "run out",
                "lbw",
                "bowled",
                "not out",
                "not out",
                "svfs",
            ],
            "R": ["41", "12", "0", "51", "13", "6", "132", "93", "221", "0"],
            "B": ["32", "31", "1", "7", "23", "17", "103", "63", "148", NaN],
            "M": ["53", "42", "1", "-", "42", "25", "124", "8", "103", "4"],
            "4s": ["4", "1", "5", "36", "59", "64", "102", "12", "135", "8"],
            "6s": ["7", "4", "14", "4", "51", "92", "193", "31", "241", "1"],
            "SR": [
                "84.24",
                "53.14",
                "103.24",
                "5.24",
                "6.42",
                "40.52",
                "14.53",
                "152.52",
                "-",
                "204.41",
            ],
        }
    )


@pytest.fixture
def removed_rows_df() -> DataFrame:
    return DataFrame(
        {
            "BATTING": [
                "Joe Root",
                "Virat Kholi (c)",
                "Virat Kholi",
                "Jos Buttler †",
                "Joe Root",
                "Sanga (c) †",
            ],
            "Unnamed: 1": [
                "not out",
                "caught",
                "not out",
                "bowled",
                "not out",
                "not out",
            ],
            "R": ["41", "12", "51", "132", "93", "221"],
            "B": ["32", "31", "7", "103", "63", "148"],
            "M": ["53", "42", "-", "124", "8", "103"],
            "4s": ["4", "1", "36", "102", "12", "135"],
            "6s": ["7", "4", "4", "193", "31", "241"],
            "SR": [
                "84.24",
                "53.14",
                "5.24",
                "14.53",
                "152.52",
                "-",
            ],
        }
    )


@pytest.fixture
def renamed_columns_df() -> DataFrame:
    return DataFrame(
        {
            "Batter": [
                "Joe Root",
                "Virat Kholi (c)",
                "Virat Kholi",
                "Jos Buttler †",
                "Joe Root",
                "Sanga (c) †",
            ],
            "Dismissal": [
                "not out",
                "caught",
                "not out",
                "bowled",
                "not out",
                "not out",
            ],
            "Runs": ["41", "12", "51", "132", "93", "221"],
            "Balls": ["32", "31", "7", "103", "63", "148"],
            "Minutes": ["53", "42", "-", "124", "8", "103"],
            "Fours": ["4", "1", "36", "102", "12", "135"],
            "Sixes": ["7", "4", "4", "193", "31", "241"],
            "StrikeRate": [
                "84.24",
                "53.14",
                "5.24",
                "14.53",
                "152.52",
                "-",
            ],
        }
    )


@pytest.fixture
def removed_dashes_df() -> DataFrame:
    return DataFrame(
        {
            "Batter": [
                "Joe Root",
                "Virat Kholi (c)",
                "Virat Kholi",
                "Jos Buttler †",
                "Joe Root",
                "Sanga (c) †",
            ],
            "Dismissal": [
                "not out",
                "caught",
                "not out",
                "bowled",
                "not out",
                "not out",
            ],
            "Runs": ["41", "12", "51", "132", "93", "221"],
            "Balls": ["32", "31", "7", "103", "63", "148"],
            "Minutes": ["53", "42", "0", "124", "8", "103"],
            "Fours": ["4", "1", "36", "102", "12", "135"],
            "Sixes": ["7", "4", "4", "193", "31", "241"],
            "StrikeRate": [
                "84.24",
                "53.14",
                "5.24",
                "14.53",
                "152.52",
                "0",
            ],
        }
    )


@pytest.fixture
def cleaned_names_df() -> DataFrame:
    return DataFrame(
        {
            "Batter": [
                "Joe Root",
                "Virat Kholi",
                "Virat Kholi",
                "Jos Buttler",
                "Joe Root",
                "Sanga",
            ],
            "Dismissal": [
                "not out",
                "caught",
                "not out",
                "bowled",
                "not out",
                "not out",
            ],
            "Runs": ["41", "12", "51", "132", "93", "221"],
            "Balls": ["32", "31", "7", "103", "63", "148"],
            "Minutes": ["53", "42", "0", "124", "8", "103"],
            "Fours": ["4", "1", "36", "102", "12", "135"],
            "Sixes": ["7", "4", "4", "193", "31", "241"],
            "StrikeRate": [
                "84.24",
                "53.14",
                "5.24",
                "14.53",
                "152.52",
                "0",
            ],
        }
    )


@pytest.fixture
def out_column_df() -> DataFrame:
    return DataFrame(
        {
            "Batter": [
                "Joe Root",
                "Virat Kholi",
                "Virat Kholi",
                "Jos Buttler",
                "Joe Root",
                "Sanga",
            ],
            "Dismissal": [
                "not out",
                "caught",
                "not out",
                "bowled",
                "not out",
                "not out",
            ],
            "Runs": ["41", "12", "51", "132", "93", "221"],
            "Balls": ["32", "31", "7", "103", "63", "148"],
            "Minutes": ["53", "42", "0", "124", "8", "103"],
            "Fours": ["4", "1", "36", "102", "12", "135"],
            "Sixes": ["7", "4", "4", "193", "31", "241"],
            "StrikeRate": [
                "84.24",
                "53.14",
                "5.24",
                "14.53",
                "152.52",
                "0",
            ],
            "Out": [False, True, False, True, False, False],
        }
    )


@pytest.fixture
def changed_types_df() -> DataFrame:
    return DataFrame(
        {
            "Batter": [
                "Joe Root",
                "Virat Kholi",
                "Virat Kholi",
                "Jos Buttler",
                "Joe Root",
                "Sanga",
            ],
            "Dismissal": [
                "not out",
                "caught",
                "not out",
                "bowled",
                "not out",
                "not out",
            ],
            "Runs": [41, 12, 51, 132, 93, 221],
            "Balls": [32, 31, 7, 103, 63, 148],
            "Minutes": [53, 42, 0, 124, 8, 103],
            "Fours": [4, 1, 36, 102, 12, 135],
            "Sixes": [7, 4, 4, 193, 31, 241],
            "StrikeRate": [
                84.24,
                53.14,
                5.24,
                14.53,
                152.52,
                0,
            ],
            "Out": [False, True, False, True, False, False],
        }
    )


@pytest.fixture
def totals_df() -> DataFrame:
    return DataFrame(
        {
            "Batter": [
                "Joe Root",
                "Virat Kholi",
                "Jos Buttler",
                "Sanga",
            ],
            "Runs": [134, 63, 132, 221],
            "Balls": [95, 38, 103, 148],
            "Minutes": [61, 42, 124, 103],
            "Fours": [16, 37, 102, 135],
            "Sixes": [38, 8, 193, 241],
            "Out": [0, 1, 1, 0],
        }
    )


def test_version():
    assert __version__ == "0.1.0"


def test_remove_columns(dirty_df: DataFrame, removed_columns_df: DataFrame):
    new_df = remove_unwanted_columns(dirty_df)
    assert_frame_equal(new_df, removed_columns_df)


def test_remove_rows(removed_columns_df: DataFrame, removed_rows_df: DataFrame):
    new_df = remove_unwanted_rows(removed_columns_df)
    assert_frame_equal(new_df, removed_rows_df)


def test_rename_columns(removed_rows_df: DataFrame, renamed_columns_df: DataFrame):
    new_df = rename_columns(removed_rows_df)
    assert_frame_equal(new_df, renamed_columns_df)


def test_remove_dashes(renamed_columns_df: DataFrame, removed_dashes_df: DataFrame):
    new_df = remove_dashes(renamed_columns_df)
    assert_frame_equal(new_df, removed_dashes_df)


def test_clean_names(removed_dashes_df: DataFrame, cleaned_names_df: DataFrame):
    new_df = clean_name(removed_dashes_df)
    assert_frame_equal(new_df, cleaned_names_df)


def test_out_column(cleaned_names_df: DataFrame, out_column_df: DataFrame):
    new_df = out_column(cleaned_names_df)
    assert_frame_equal(new_df, out_column_df)


def test_change_types(out_column_df: DataFrame, changed_types_df):
    new_df = change_column_types(out_column_df)
    numeric_cols = ["Runs", "Balls", "Minutes", "Fours", "Sixes", "StrikeRate"]
    assert all(pd.api.types.is_numeric_dtype(new_df[col]) for col in numeric_cols)
    assert_frame_equal(new_df, changed_types_df)


def test_clean_dataframe(dirty_df: DataFrame, changed_types_df: DataFrame):
    new_df = clean_batters_dataframe(dirty_df)
    assert_frame_equal(new_df, changed_types_df)


@patch("cricinfo_scraper.pandas_scraper.pd.read_html")
def test_scrape_dataframe(
    read_html_mock: Mock,
    split_df_1: DataFrame,
    split_df_2: DataFrame,
    dirty_df: DataFrame,
):
    read_html_mock.return_value = [split_df_1, split_df_2]
    new_df = read_scorecard("test")
    assert_frame_equal(new_df.reset_index(drop=True), dirty_df)


def test_totals_dataframe(changed_types_df: DataFrame, totals_df: DataFrame):
    new_df = batters_totals(changed_types_df).sort_values(by="Batter")
    assert_frame_equal(
        new_df, totals_df.sort_values(by="Batter").reset_index(drop=True)
    )


# @patch("cricinfo_scraper.cricinfo_link_scraper.webdriver.Chrome.get")
# def test_scrape_links(webdriver_get_mock: Mock):
#     file_path = os.path.abspath("tests/cricinfo_snapshot.html")
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")

#     with webdriver.Chrome(
#         service=Service(ChromeDriverManager().install()), options=chrome_options
#     ) as driver:
#         #webdriver_get_mock.return_value = driver.get(f"file://{file_path}")
#         webdriver_get_mock.return_value = driver.get("/home/vieran/cricinfo-scraper/tests/cricinfo_snapshot.html")
#     links: List[str] = get_links()
#     assert len(links) == 37


# @patch("cricinfo_scraper.cricinfo_link_scraper.webdriver.Chrome.get")
# def test_scrape_links(webdriver_get_mock: Mock):
#     file_path = os.path.abspath("tests/cricinfo_snapshot.html")
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")

#     with webdriver.Chrome(
#         service=Service(ChromeDriverManager().install()), options=chrome_options
#     ) as driver:
#         #webdriver_get_mock.return_value = driver.get(f"file://{file_path}")
#         driver.get("file:///home/vieran/cricinfo-scraper/tests/cricinfo_snapshot.html")
#         links: List[str] = get_all_links(driver=driver)
#     assert len(links) == 37

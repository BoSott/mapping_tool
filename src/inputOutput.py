"""Manages input and ouput functions."""
import sys
import pandas as pd
import geopandas as gpd
import fiona
import json
from definitions import logger_f
import re
import matplotlib.colors as mcolors

##################### INPUT ######################


def read_file(fpath, driver):
    """Read file based on given path and driver.

    Args:
        fpath (Path): a pathlib path
        driver (String): self defined list of drivers: gpd, fiona, txt

    Returns:
        file: returns a file in the format of the provided driver
    """
    try:
        # returns geopandas.GeoDataframe
        if driver == "gpd":
            data = gpd.read_file(fpath)

        # returns a Fiona collection object as list of dicts.
        elif driver == "fiona":
            with fiona.open(fpath, "r") as f:
                data = list(f)

        # returns a string
        elif driver == "txt":
            with open(fpath, "r") as f:
                data = f.read()

        elif driver == "json":
            with open(fpath, "r") as f:
                data = json.load(f)

        else:
            logger_f.error(f"read method '{driver}' not found")
            data = None
    except FileNotFoundError as err:
        logger_f.error(f"{fpath} could not be found ", err)
        sys.exit(1)
    except OSError as err:
        logger_f.error("system-related error: ", err)
    except Exception as err:
        logger_f.error("could not open file", err)
        sys.exit(1)
    return data


def save_osm(path, driver, file):
    """Save given file under given path with given driver.

    Args:
        path (Path): pathlib path
        driver (String): JSON, GeoJSON, gpkg
        file (file): the file to be saved
    """
    try:
        if driver == "JSON":
            with open(path, "w+") as json_file:  # ATTENTION! will overwrite
                json.dump(file, json_file)
        elif driver == "GeoJSON":
            file.to_file(path, driver=driver)
        elif driver == "gpkg":
            file.to_file(path, driver=driver.upper())
        else:
            logger_f.error(f"file method ({driver}) not found")
    except FileNotFoundError as err:
        logger_f.error(f"{path} could not be found ", err)
        sys.exit(1)
    except OSError as err:
        logger_f.error("system-related error: ", err)
    except Exception as err:
        logger_f.error("something unexpected happened: ", err)
        sys.exit(1)


# does more or less the same as the function below, just for string input
# changed it to json input -> cleaner input, easier to test
'''
def get_params(input_file):
    """Convert the input file string to parameter settings and names as pandas dataframe.

    Args:
        input_file ([string]): [content of the input file as string with first row as column names]

    Returns:
        [DataFrame]: [returns a pandas Dataframe with one row per requested layer]
    """
    input_params = input_file.splitlines()

    params = [x.split(",") for x in input_params]

    params = [list(map(str.strip, params[x])) for x in range(len(params))]  # strips input of whitespaces

    df = pd.DataFrame(columns=params[0], data=params[1:])

    return df
'''


def get_params(input_file):
    """Convert dictionary from json input to dataframe.

    Args:
        input_file (dict): dictionary of input json

    Returns:
        DataFrame: [returns a pandas Dataframe with one row per requested layer]
    """
    df = pd.DataFrame(input_file)
    params = [list(df["layers"][i].values()) for i in range(len(df))]
    cols = [i.capitalize() for i in df["layers"][0].keys()]  # capitalize layer parameter names
    df = pd.DataFrame(columns=cols, data=params)
    return df


def check_download_input(df):
    """Check required download user input.

    Args:
        df (DataFrame): dataframe with given user input
    """
    try:
        # check if name is a string, uncritical
        for name in df["Name"]:
            assert type(name) == str

        # check if '=' is in filter string -> if not, cannot be correct
        for filter in df["Filter"]:
            assert "=" in filter, f"{filter} is not a correct filter, requires at least one '=' "

        # check input polygon
        for pol in df["Polygon"]:
            ending = ("GEOJSON" in pol.upper()) or ("GPKG" in pol.upper())  # no case sensitivity required
            assert ending, "the input polygon file should be of type .geojson or .gpkg"
    except KeyError as err:
        logger_f.warning("Given user download input is not correct, wrong column names", err)
        return False
    except AssertionError as err:
        logger_f.warning("Given user download input is not correct", err)
        return False
    return True


def check_color(color):
    """Check if given color hextech or name is valid.

    Args:
        color (String): hextech color string

    Returns:
        bool: True if color is valid, False if not
    """
    valid = False
    if color.startswith("#"):
        # check if hext
        valid = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color)
    else:
        valid = color in mcolors.CSS4_COLORS
    return valid


def check_plotting_input(df):
    """Check required plotting user input for column names and values.

    Args:
        df (DataFrame): DataFrame with given user input

    Returns:
        bool: True if plotting input is valid, False if not
    """
    try:
        for name in df["Name"]:
            assert type(name) == str

        for color in df["Color"]:
            assert check_color(color), f"color {color} is not correct"

    except KeyError as err:
        logger_f.warning("Given user download input is not correct, wrong column names: ", err)
        return False
    except AssertionError as err:
        logger_f.warning("Given user plotting input is not correct: ", err)
        return False
    return True

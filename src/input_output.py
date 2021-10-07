"""Manages input and ouput functions."""
import sys
import pandas as pd
import geopandas as gpd
import fiona
import json

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
        else:
            print(f"read method '{driver}' not found")
            data = None
    except FileNotFoundError as err:
        print(f"{fpath} could not be found ", err)
        sys.exit(1)
    except OSError as err:
        print("system-related error: ", err)
    except Exception as err:
        print("something unexpected happened: ", err)
        sys.exit(1)
    return data


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


# def findfile(directory, filename):
#     return glob.glob(f"{directory}/{filename}*")

################## OUTPUT ##########################


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
            print(f"file method ({driver}) not found")
    except FileNotFoundError as err:
        print(f"{path} could not be found ", err)
        sys.exit(1)
    except OSError as err:
        print("system-related error: ", err)
    except Exception as err:
        print("something unexpected happened: ", err)
        sys.exit(1)


if __name__ == "__main__":
    pass

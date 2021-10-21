import sys
import os
import geopandas as gpd
from pathlib import Path
import pandas as pd
from ohsome_api import download_osm
from shapely.geometry import Point
import json
from bokeh.plotting.figure import figure
from mapping import change_crs, create_statistics, get_cx_providers

# what a hacky thing to do.. nonetheless, anything else did not work out
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from definitions import DATA_PATH, logger_m
from inputOutput import get_params, save_osm, read_file


DATA_PATH_TEST = Path(DATA_PATH / "test_data")


def test_read_file_types():
    """Test to read files."""
    fname = "test_input.GeoJSON"
    fpath = DATA_PATH_TEST / fname

    test_file_gpd = read_file(fpath, "gpd")
    test_file_fiona = read_file(fpath, "fiona")
    test_file_txt = read_file(fpath, "txt")

    assert type(test_file_gpd) == gpd.GeoDataFrame, "Should be GeoDataFrame"
    assert type(test_file_fiona) == list, "Should be a list"
    assert type(test_file_txt) == str, "Should be a string"


def test_read_file_content():
    """Test to read file content correctly."""
    fname = "test_input.GeoJSON"
    fpath = DATA_PATH_TEST / fname

    test_file_gpd = read_file(fpath, "gpd")
    test_file_fiona = read_file(fpath, "fiona")
    test_file_txt = read_file(fpath, "txt")
    test_file_json = read_file(fpath, "json")

    assert test_file_gpd["name"][0] == "test_feature", "should be 'test_feature'"
    assert type(test_file_gpd["geometry"][0]).isinstance(type(Point(8.70131, 49.40866))), "should be a shapely point"
    assert test_file_gpd["geometry"][0].x == 8.7013112, "x coordinate should be 8.7013112"

    assert test_file_fiona[0]["properties"]["name"] == "test_feature", "access structure should result in 'test_feature'"
    assert test_file_fiona[0]["geometry"]["type"] == "Point", "type should be Point"
    assert test_file_fiona[0]["geometry"]["coordinates"][0] == 8.7013112, "x coordinate should be 8.7013112"

    test_txt = json.loads(test_file_txt)
    assert test_txt["features"][0]["properties"]["name"] == "test_feature", "should be 'test_feature'"
    assert test_txt["features"][0]["geometry"]["type"] == "Point", "type should be Point"
    assert test_txt["features"][0]["geometry"]["coordinates"][0] == 8.7013112, "x coordinate should be 8.7013112"

    assert test_file_json["features"][0]["properties"]["name"] == "test_feature", "should be 'test_feature'"
    assert test_file_json["features"][0]["geometry"]["type"] == "Point", "type should be Point"
    assert test_file_json["features"][0]["geometry"]["coordinates"][0] == 8.7013112, "x coordinate should be 8.7013112"


def test_save_osm():
    """Test to save data correctly."""
    fname = "test_input.GeoJSON"
    fpath_in = DATA_PATH_TEST / fname
    input_file = read_file(fpath_in, "gpd")

    fname_gpkg = "test_output.gpkg"
    fpath_out = DATA_PATH_TEST / fname_gpkg

    save_osm(path=fpath_out, driver="gpkg", file=input_file)
    file = read_file(fpath_out, "gpd")
    assert file["name"][0] == "test_feature", "should be 'test_feature'"
    assert fpath_out.is_file(), "file was not saved correctly"

    fname_gpkg = "test_output.GeoJSON"
    fpath_out = DATA_PATH_TEST / fname_gpkg
    save_osm(fpath_out, "GeoJSON", input_file)
    file = read_file(fpath_out, "gpd")
    assert file["name"][0] == "test_feature", "should be 'test_feature'"
    assert fpath_out.is_file(), "file was not saved correctly"
    # delete file again
    fpath_out.unlink()


def test_get_params():
    """Test the conversion of input data to df."""
    fname = "input_download.json"
    fpath = DATA_PATH_TEST / fname
    input_file = read_file(fpath, "json")

    in_params = get_params(input_file=input_file)

    assert len(in_params) == 3, "number of rows is wrong, should be 3"
    assert list(in_params.keys()) == ["Name", "Filter", "Time", "Polygon"], "column names are not correct"
    assert list(in_params["Name"]) == ["bicycle_parking", "highways", "buildings"], "rows are not correct"


def test_download_osm():
    """Test ohsome download functions."""
    filter = "amenity=bicycle_parking and geometry:point."
    time = None
    bpolys = gpd.read_file(DATA_PATH_TEST / "input_polygon.geojson")
    response = download_osm(filter=filter, time=time, bpolys=bpolys)

    assert response is not None, "response should not be empty"
    assert "geometry" in response.keys(), "response should have a geometry column"

    filter = "natural=tree and geometry:point"
    response = download_osm(filter=filter, time=time, bpolys=bpolys)

    assert response is None, "response should be None"


def test_change_crs():
    """Test to change the CRS of a nested geopandas dataframe works correctly."""
    data = [["highway", "red"]]
    gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy([8.42], [49.25]), crs="EPSG:4326")
    lay = []
    lay.append(gdf)
    df = pd.DataFrame({"name": ["TestDataFrame"]})
    df1 = df.assign(Layers=lay)
    gdf_crs = change_crs(df1, 3857)
    assert gdf_crs["Layers"][0].crs.srs == "epsg:3857", "changing the CRS did not work"


def test_get_cx_providers():
    """Test if the xyz basemap providers works correctly."""
    providers = get_cx_providers()
    assert type(providers) == dict, "Providers should be of type dict"

    # check if any OpenStreetMap or Stamen provider are listed in the provider dictionary.
    # If not, it is assumed that this did not work correctly as those two are very important providers
    provider_check = any([(("OpenStreetMap" or "Stamen") in x) for x in providers.keys()])
    assert provider_check, "no OSM provider listed"


def test_create_statistics():
    """Test the provision of statistics."""
    map_layer = pd.DataFrame({"Name": ["first"], "Layers": [[1, 2, 3, 4, 5]], "Color": "grey"})

    p_test = figure()
    p_test.vbar()

    p = create_statistics(map_layer)

    assert type(p.vbar.__func__).isinstance(type(p_test.vbar.__func__)), "should be the same type"
    assert p.height == 300, "figure height should be 300"


if __name__ == "__main__":
    """Execute tests"""
    test_download_osm()  # takes some time
    test_read_file_types()
    test_read_file_content()
    test_save_osm()
    test_get_params()
    test_change_crs()
    test_get_cx_providers()
    test_create_statistics()

    logger_m.info("All tests passed")

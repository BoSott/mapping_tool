from definitions import DATA_PATH, INPUT_PATH_DOWNLOAD, INPUT_PATH_PLOTLY, logger
from mapping import change_crs, map_plotly
from ohsome_api import download_osm
import input_output

## create tool structure -> possibly with clicks
driver = "gpkg"
properties = "tags"
map_input = INPUT_PATH_PLOTLY
crs_epsg = 3857


def main(download=False):
    """Main function of this program executes everything else.

    Args:
        download (bool, optional): Decide if files shall be downloaded or not. Defaults to False.
    """
    # load input parameters as dataframe
    in_file = input_output.read_file(fpath=INPUT_PATH_DOWNLOAD, driver="txt")
    in_params = input_output.get_params(input_file=in_file)

    # download each layer with the given parameters and save each to the data folder
    # TODO check if download is completed and not empty
    # TODO check if layer already exists
    # TODO strip input from spaces!
    if download:
        for index, row in in_params[2:].iterrows():  # start of the download changed
            name = row[0]
            filter = row[1]
            f = lambda x: None if x == "None" else x  # converts string "None" to None
            time = f(row[2])
            bpolys_path = DATA_PATH / row[3]
            bpolys = input_output.read_file(bpolys_path, driver="gpd")

            layer = download_osm(name=name, filter=filter, time=time, bpolys=bpolys, properties=properties)
            save_path = DATA_PATH / f"{row[0]}.{driver}"
            input_output.save_osm(save_path, driver=driver, file=layer)

    # bit double the effort but makes it possible to use on its own with downloading everything again

    # get the map style paramters
    in_file_plotly = input_output.read_file(fpath=map_input, driver="txt")
    in_params_plotly = input_output.get_params(input_file=in_file_plotly)

    # get the map layer and create list of layers
    layers = []
    for index, row in in_params.iterrows():
        name = row[0]
        # color=row[1]
        layer_path = DATA_PATH / f"{name}.{driver}"
        layer = input_output.read_file(fpath=layer_path, driver="gpd")
        # layer_crs = layer.to_crs(epsg=crs_epsg)
        layers.append(layer)

    # combine osm layers with the plotly input params
    map_layer = in_params_plotly.assign(Layers=layers)

    # change crs of layers
    map_layer = change_crs(map_layer, crs_epsg)

    # create map with plotly

    # reverse dataframe so that the last item is going to be plotted first and the others on top of it
    reverse_map = map_layer.iloc[::-1]
    # map_plotly(map_layer)
    map_plotly(reverse_map)


if __name__ == "__main__":
    logger.info("start main process")
    main(download=False)

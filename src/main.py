from logging import log
from definitions import DATA_PATH, INPUT_PATH, INPUT_PATH_DOWNLOAD, INPUT_PATH_GPD, logger
from mapping import change_crs, map_plotly
from ohsome_api import download_osm
from processing import download, plotting
import input_output
import click
from pathlib import Path

## create tool structure -> possibly with clicks
driver = "gpkg"
properties = "tags"
map_input = INPUT_PATH_GPD
crs_epsg = 3857




_driver_option = [
    click.option(
       "--driver",
       "-d",
       default="gpkg",
       type=str,
       help="Specify the type in which the OSM layers should be saved. GeoJSON or Default: gpkg",
    )
]

_properties_option = [
    click.option(
        "--properties",
        "-prop",
        default="tags",
        type=str,
        help="Specifies the kind of property that the ohsome API is filtered for. Just leave it as it is. Default: tags",
    )
]

_crs_epsg_option = [
    click.option(
        "--crs_epsg",
        "-ce",
        default=3857,
        type=int,
        help="Specify the CRS EPSG that the layer should be converted to. Plotly requires the default: 3857",
    )
]

_plot_package_option = [
    click.option(
        "--plot_package",
        "-pp",
        default="gpd",
        type=str,
        help="Specify which plotting package should be used: gpd, bokeh. Default: gpd",
    )
]

_input_polygon_option = [
    click.option(
        "--input_polygon",
        "-pol",
        default="input_polygon.geojson",
        type=str,
        help="Specify the name with .geojson ending of the polygon for the extent. Default: input_polygon.geojson", 
    )
]

_title_option = [
    click.option(
        "--title",
        "-t",
        default="Map with OSM layer",
        type=str,
        help="Specify the title of the plot. Default: Map with OSM layer"
    )
]

_save_plot_option = [
    click.option(
        "--save_plot",
        "-sp",
        default=False,
        type=bool,
        help="Specify whether the plot should be saved or not"
    )
]

_overwrite_option = [
    click.option(
        "--overwrite",
        "-o",
        default=False,
        type=bool,
        help="Specify whether existing layers should be overwritten by downloaded ones or not. Default: False"
    )
]

# _xxx_option = [
#     click.option(
        
#     )
# ]


def add_options(options):
    """Functions adds options to cli."""

    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


@click.group()
@click.option('--verbose', '-v', is_flag=False, help="Will print verbose messages.")
def cli(verbose: bool) -> None:
    if verbose:
        click.echo("We are in the verbose mode. Which does not make any"
                   "difference right now.. but hey, have fun!")
        #TODO change logger from warning to info level


@cli.command()
@add_options(_driver_option)
@add_options(_properties_option)
@add_options(_input_polygon_option)
@add_options(_overwrite_option)
def run_download(
    driver: str,
    properties: str,
    input_polygon: str,
    overwrite: bool
) -> None:
    """Executes command to download and save OSM layer """
    in_file = input_output.read_file(fpath=INPUT_PATH_DOWNLOAD, driver="txt")
    in_params = input_output.get_params(input_file=in_file)

    # download each layer with the given parameters and save each to the data folder
    for index, row in in_params.iterrows():  # start of the download changed
        name = row[0]
        filter = row[1]
        f = lambda x: None if x == "None" else x  # converts string "None" to None
        time = f(row[2])
        bpolys_path = INPUT_PATH / row[-1]
        bpolys = input_output.read_file(bpolys_path, driver="gpd")

        # check if data already exists and only download and overwrite if wanted
        layer_path = DATA_PATH / f"{name}.{driver}"
        if Path(layer_path).is_file() and not overwrite:
            logger.info(f"file {name}.{driver} is already downloaded")
            continue

        layer = download_osm(name=name, filter=filter, time=time, bpolys=bpolys, properties=properties)
        
        # if no features could be found, continue with the next layer
        if layer is None:
            logger.warning(
                f"requested layer with filter: {filter} did not return any features for the given search ares. \
                Skip layer {name}.")
            continue
        
        save_path = DATA_PATH / f"{name}.{driver}"
        input_output.save_osm(save_path, driver=driver, file=layer)


cli.command()
@add_options(_plot_package_option)
@add_options(_crs_epsg_option)
@add_options(_title_option)
@add_options(_save_plot_option)
def run_plotting(
    plot_package: str,
    crs_epsg: int,
    title: str,
    save_plot: bool
) -> None:
    """Execute command to plot the given layer based on input files"""
    # TODO add plotting stuff
    # take into account:
    # - different plotting packages
    # - empty input / files
    
    ################# MAPPING ###################
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



@cli.command()
@add_options(_driver_option)
@add_options(_properties_option)
@add_options(_crs_epsg_option)
@add_options(_plot_package_option)
@add_options(_input_polygon_option)
@add_options(_title_option)
@add_options(_save_plot_option)
@add_options(_overwrite_option)
@click.pass_context
def run(
    ctx,
    driver: str,
    properties: str,
    crs_epsg: int,
    plot_package: str,
    input_polygon: str,
    title: str,
    save_plot: bool,
    overwrite: bool
) -> None:
    """Executes downloading and plotting"""
    ctx.invoke(
        run_download,
        driver=driver,
        properties=properties,
        input_polygon=input_polygon,
        overwrite=overwrite
    )
    
    ctx.invoke(
        run_plotting,
        crs_epsg=crs_epsg,
        plot_package=plot_package,
        title=title,
        save_plot=save_plot
    )


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


    ################# MAPPING ###################
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
    # main(download=False)
    # run_download(driver="gpkg", properties="tags", input_polygon="input_polygon.geojson", overwrite=False)
    # run_download(["-d", "gpkg"], ["-prop", "tags"], ["-pol", "input_polygon.geojson"], ["-o", False])
    # run_download()
    run_plotting()


## TODO
# fuse the main into the clicks stuff and add the stuff that is in the comments there -> download stuff
# add bokeh plot
# add somnx plot - just because I want such a map :D
# edit logger
# write stuff down -> should be okay by then I guess...

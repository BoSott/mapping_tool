#!/usr/bin/env python
# -*- coding: utf-8 -*-
from definitions import (
    DATA_PATH,
    INPUT_PATH,
    INPUT_PATH_BOKEH,
    INPUT_PATH_DOWNLOAD,
    INPUT_PATH_GPD,
    logger_m,
    logger_f,
    OUTPUT_PATH,
)
from mapping import change_crs, get_cx_providers, map_bokeh, map_gpd, map_multiple
from ohsome_api import download_osm
import inputOutput
import click
from pathlib import Path
import sys
from bokeh.io import show
from bokeh.plotting import output_file
from bokeh.plotting import save
from bokeh.io import export_png

_driver_option = [
    click.option(
        "--driver",
        "-d",
        default="GeoJSON",
        type=str,
        help="Specify the type in which the OSM layers should be saved. gpkg or Default: GeoJSON",
    )
]

_crs_epsg_option = [
    click.option(
        "--crs_epsg",
        "-ce",
        default=3857,
        type=int,
        help="Specify the CRS EPSG that the layer should be converted to. GPD requires the default: 3857",
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

_title_option = [
    click.option(
        "--title", "-t", default="Map with OSM layer", type=str, help="Specify the title of the plot. Default: Map with OSM layer"
    )
]

_save_plot_option = [
    click.option(
        "--save_plot", "-sp", default=True, type=bool, help="Specify whether the plot should be saved or not. Default: True"
    )
]

_overwrite_option = [
    click.option(
        "--overwrite",
        "-o",
        default=False,
        type=bool,
        help="Specify whether existing layers should be overwritten by downloaded ones or not. Default: False",
    )
]

_basemap_option = [
    click.option(
        "--basemap",
        "-b",
        default="Stamen.TonerLite",
        type=str,
        help="See https://leaflet-extras.github.io/leaflet-providers/preview/index.html for all layer options. \
            or here: https://contextily.readthedocs.io/en/latest/providers_deepdive.html for a list and more specifications. \
            Default: 'Stamen.TonerLite' \
            provider selection: 'OpenStreetMap.Mapnik', 'OpenTopoMap','Stamen.Toner','Stamen.TonerLite', \
            'Stamen.Terrain', 'Stamen.TerrainBackground', 'Stamen.Watercolor', 'NASAGIBS.ViirsEarthAtNight2012', \
            'CartoDB.Positron', 'CartoDB.Voyager' "
        # TODO OR: random -> to generate four plots with different background maps, only gdl"
    )
]

_random_baserlayer_option = [
    click.option(
        "--random_baselayer",
        "-rb",
        default=False,
        type=bool,
        help="If True, creates four bokeh plots with the given layers and randomly chosen basemaps.",
    )
]

# _xxx_option = [
#     click.option(

#     )
# ]


def add_options(options):
    """Functions adds options to cli."""

    def _add_options(func):
        """Add clicks options."""
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Will print verbose messages.")
def cli(verbose: bool) -> None:
    """Activate verbose mode."""
    if not verbose:
        del logger_f.handlers[0]
        del logger_m.handlers[0]


@cli.command()
@add_options(_driver_option)
@add_options(_overwrite_option)
def run_download(driver: str, overwrite: bool) -> None:
    """Executes command to download and save OSM layer."""
    in_file = inputOutput.read_file(fpath=INPUT_PATH_DOWNLOAD, driver="json")
    in_params = inputOutput.get_params(input_file=in_file)

    if inputOutput.check_download_input(in_params):
        logger_f.info("Given user download input is correct (time parameter not checked)")
    else:
        logger_f.warning("Download input is not correct. End Program.")
        sys.exit()

    # download each layer with the given parameters and save each to the data folder
    for index, row in in_params.iterrows():  # start of the download changed
        name = row[0]
        filter = row[1]
        f_none = lambda x: None if x == "None" else x  # converts string "None" to None
        time = f_none(row[2])
        bpolys_path = INPUT_PATH / row[-1]
        bpolys = inputOutput.read_file(bpolys_path, driver="gpd")

        # check if data already exists and only download and overwrite if wanted
        layer_path = DATA_PATH / f"{name}.{driver}"
        if Path(layer_path).is_file() and not overwrite:
            logger_m.info(f"file {name}.{driver} is already downloaded")
            continue

        layer = download_osm(filter=filter, time=time, bpolys=bpolys)

        # if no features could be found, continue with the next layer
        if layer is None:
            logger_m.warning(
                f"requested layer with filter: {filter} did not return any features for the given search areas. \
                Skip layer {name}."
            )
            continue

        save_path = DATA_PATH / f"{name}.{driver}"
        inputOutput.save_osm(save_path, driver=driver, file=layer)


@cli.command()
@add_options(_plot_package_option)
@add_options(_driver_option)
@add_options(_crs_epsg_option)
@add_options(_title_option)
@add_options(_save_plot_option)
@add_options(_basemap_option)
@add_options(_random_baserlayer_option)
def run_plotting(
    plot_package: str, driver: str, crs_epsg: int, title: str, save_plot: bool, basemap: str, random_baselayer: bool
) -> None:
    """Execute command to plot the given layer based on input files."""
    # choose plot parameter file location based on plot_package
    input_dict_download = {"gpd": INPUT_PATH_GPD, "bokeh": INPUT_PATH_BOKEH}
    map_input = input_dict_download[plot_package]

    # get the plotting style parameters
    input_file_plot = inputOutput.read_file(fpath=map_input, driver="json")
    in_params_plot = inputOutput.get_params(input_file=input_file_plot)

    # check user plotting input
    if inputOutput.check_plotting_input(in_params_plot):
        logger_f.info("Given user plotting input is correct")
    else:
        logger_f.warning("Plotting input is not correct. End Program.")
        sys.exit()

    # get general layer information about layer -> load input parameters as dataframe
    in_file = inputOutput.read_file(fpath=INPUT_PATH_DOWNLOAD, driver="json")
    in_params = inputOutput.get_params(input_file=in_file)

    # check user layer information (download) input
    if inputOutput.check_download_input(in_params):
        logger_f.info("Given user download input is correct (time parameter not checked)")
    else:
        logger_f.warning("Download input is not correct. End Program.")
        sys.exit()

    # get the map layer and create list of layers
    layers = []
    for index, row in in_params.iterrows():
        name = row[0]
        layer_path = DATA_PATH / f"{name}.{driver}"

        # check if layer exists. If not: continue.
        if not Path(layer_path).is_file():
            logger_m.warning(f"file {name}.{driver} does not exist. Continue with the next.")
            continue

        layer = inputOutput.read_file(fpath=layer_path, driver="gpd")
        layers.append(layer)
    # exit program if no valid layer is given
    if not len(layers):
        logger_m.error("No valid layer given.")
        sys.exit()

    # combine osm layers with the gpd input params
    # no need to handle empty files, they will not be saved in the first place (see run_download: 178f)
    map_layer = in_params_plot.assign(Layers=layers)

    # change crs of layers
    map_layer = change_crs(map_layer, crs_epsg)

    # reverse dataframe so that the last item is going to be plotted first and the others on top of it
    reverse_map = map_layer.iloc[::-1]

    # reset index
    reverse_map.reset_index(inplace=True, drop=True)

    # create map with gpd
    if plot_package == "gpd":
        # check if basemap exists, if not choose default
        if basemap not in get_cx_providers():
            basemap = "Stamen.TonerLite"
            logger_m.warning("Given baselayer name does not exist. Changed to default.")

        map_gpd(reverse_map, crs_epsg, basemap, title, save_plot)

    elif plot_package == "bokeh":
        if not random_baselayer:
            p = map_bokeh(reverse_map, basemap, title)
        else:
            p = map_multiple(reverse_map, basemap, title)
            # show(grid)

        # save plot if wanted
        # title_underscore = title.replace(" ", "_")
        title_underscore = title
        save_to = OUTPUT_PATH / f"bokeh_{title_underscore}.html"
        output_file(title=title_underscore, filename=save_to)
        if save_plot:
            # save_to = OUTPUT_PATH / f"bokeh_{title_underscore}.html"
            save(p)
            save_to_png = OUTPUT_PATH / f"bokeh_{title_underscore}.png"
            export_png(obj=p, filename=save_to_png)
        show(p)

    else:
        logger_m.warning(f"plot package {plot_package} not implemented. Abort plotting.")
        sys.exit(1)


@cli.command()
@add_options(_driver_option)
@add_options(_crs_epsg_option)
@add_options(_plot_package_option)
@add_options(_title_option)
@add_options(_save_plot_option)
@add_options(_overwrite_option)
@add_options(_random_baserlayer_option)
@click.pass_context
def run(
    ctx,
    driver: str,
    crs_epsg: int,
    plot_package: str,
    title: str,
    save_plot: bool,
    overwrite: bool,
    random_baselayer: str,
) -> None:
    """Execute command to download and plot."""
    ctx.invoke(run_download, driver=driver, overwrite=overwrite)

    ctx.invoke(
        run_plotting,
        crs_epsg=crs_epsg,
        plot_package=plot_package,
        title=title,
        save_plot=save_plot,
        random_baselayer=random_baselayer,
    )


if __name__ == "__main__":
    logger_m.info("start main proc<ess")

    # define the click parameters as shown below
    # giving no parameters will run the application with default parameters

    # run_download(driver="gpkg", input_polygon="input_polygon.geojson", overwrite=False)
    # run_download(["-d", "gpkg"], ["-prop", "tags"], ["-pol", "input_polygon.geojson"], ["-o", False])
    # run_download()
    # run_plotting(["-pp", "gpd"], ["-ce", 3857], ["-t", "Map with OSM layers"], ["-sp", False])
    # run_plotting(["-pp", "gpd"])
    run_plotting(["-pp", "bokeh"], ["-rb", True])

    # run_plotting(["-pp", "bokeh"], ["-sp", True])
    # mapping_tool run-plotting --plotting_package bokeh --save_plot True --basemap Stamen.Watercolor
    # run()

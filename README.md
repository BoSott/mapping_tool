# OSM Mapping Tool

This commandline mapping tool provides functionality to download and display OSM data via Geopandas Pyplot (static) or Bokeh (interactive). Running this tool thus yields a map of the given search area and specified OSM tag filters. The result will pop up (plotly) or will be displayed in the standard browser of your system. It can be saved automatically or via the GUI.


Example Plots with gpd and bokeh and the given input example parameters.

## Map Examples
Bokeh example:
![bokeh example](https://github.com/BoSott/mapping_tool/blob/main/data/example_output/example_map_bokeh.png)

Gepandas Plotly example:
![plotly example](https://github.com/BoSott/mapping_tool/blob/main/data/example_output/example_map_plotly.png)

## Setting up:
- installed version of Python 3.9
- fork and clone this repository
- create new environment via pip or conda (recommended)
- activate environment and use given requirements.txt/environment.yml files to install dependencies respectively.

To run the program from the command line:
- activate the corresponding virtual environment
- change directory to .\src\ and execute `pip install --editable .` now *mapping_tool* is ready to be used as command in the command line when you switch back to mapping_tool roots directory.

## Required Input files
This tool requires some input data which has to be put in the *Input* folder with the given names and structure as in the example files.
Example data and file structure is given. Modify content but not file names or structure if different input is wanted. It is not possible to add more paramters through the files then the ones listed.
- *input_download.json*: Specify name, filter, time and name of the boundary polygon as input for each layer
- *input_polygon.geojson*: Polygon of the area of interest.
- *input_bokeh.json*: Specify parameters for plotting with bokeh. Name and color. Name has to be the name of the input file (the same as in the download parameters)
- *input_gpd.json*: Specify parameters for plotting with Pyplot. Name and color. Name has to be the name of the input file (the same as in the download parameters)

## How to run the tool
The folder to execute this programm has to be the root folder of the repository (mappint_tool)!
Executing commands without specifying any parameters will use default parameters only.

```
$ mapping_tool

Usage: mapping_tool [OPTIONS] COMMAND [ARGS]...

  Activate verbose mode.

Options:
  -v, --verbose  Will print verbose messages.
  --help         Show this message and exit.

Commands:
  run           Execute command to download and plot.
  run-download  Executes command to download and save OSM layer.
  run-plotting  Execute command to plot the given layer based on input...
```

### run everything
```
$ mapping_tool run --help

Usage: mapping_tool run [OPTIONS]

  Execute command to download and plot.

Options:
  -d, --driver TEXT               Specify the type in which the OSM layers
                                  should be saved. gpkg or Default: GeoJSON

  -ce, --crs_epsg INTEGER         Specify the CRS EPSG that the layer should
                                  be converted to. GPD requires the default:
                                  3857

  -pp, --plot_package TEXT        Specify which plotting package should be
                                  used: gpd, bokeh. Default: gpd

  -t, --title TEXT                Specify the title of the plot. Default: Map
                                  with OSM layer

  -sp, --save_plot BOOLEAN        Specify whether the plot should be saved or
                                  not

  -o, --overwrite BOOLEAN         Specify whether existing layers should be
                                  overwritten by downloaded ones or not.
                                  Default: False

  -rb, --random_baselayer BOOLEAN
                                  If True, creates four bokeh plots with the
                                  given layers and randomly chosen basemaps.

  --help                          Show this message and exit.
```

### Download only:
```
$ mapping_tool run-download --help

Usage: mapping_tool run-download [OPTIONS]

  Executes command to download and save OSM layer.

Options:
  -d, --driver TEXT        Specify the type in which the OSM layers should be
                           saved. gpkg or Default: GeoJSON

  -o, --overwrite BOOLEAN  Specify whether existing layers should be
                           overwritten by downloaded ones or not. Default:
                           False

  --help                   Show this message and exit.
```

### Plotting only
```
§ mapping_tool run-plotting --help

Usage: mapping_tool run-plotting [OPTIONS]

  Execute command to plot the given layer based on input files.

Options:
  -pp, --plot_package TEXT        Specify which plotting package should be
                                  used: gpd, bokeh. Default: gpd

  -d, --driver TEXT               Specify the type in which the OSM layers
                                  should be saved. gpkg or Default: GeoJSON

  -ce, --crs_epsg INTEGER         Specify the CRS EPSG that the layer should
                                  be converted to. GPD requires the default:
                                  3857

  -t, --title TEXT                Specify the title of the plot. Default: Map
                                  with OSM layer

  -sp, --save_plot BOOLEAN        Specify whether the plot should be saved or
                                  not

  -basemap, -b TEXT               See https://leaflet-
                                  extras.github.io/leaflet-
                                  providers/preview/index.html for all layer
                                  options.             or here: https://contex
                                  tily.readthedocs.io/en/latest/providers_deep
                                  dive.html for a list and more
                                  specifications.             Default:
                                  'Stamen.TonerLite'             provider
                                  selection: 'OpenStreetMap.Mapnik', 'OpenTopo
                                  Map','Stamen.Toner','Stamen.TonerLite',
                                  'Stamen.Terrain',
                                  'Stamen.TerrainBackground',
                                  'Stamen.Watercolor',
                                  'NASAGIBS.ViirsEarthAtNight2012',
                                  'CartoDB.Positron', 'CartoDB.Voyager'

  -rb, --random_baselayer BOOLEAN
                                  If True, creates four bokeh plots with the
                                  given layers and randomly chosen basemaps.

  --help                          Show this message and exit.
```

## Example
`mapping_tool run-plotting --plotting_package bokeh --save_plot True --basemap Stamen.Watercolor --title waterColorHeidelberg`

or

`mapping_tool run-plot --plot_package gpd --save_plot True --basemap Stamen.TonerLite --title StamenTonerLiteHeidelberg`

Both these commands will execute plotting and save a PNG to the ./data/output folder. The *bokeh* example will also save an interactive .html with the same name to the same location.

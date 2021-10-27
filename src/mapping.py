from bokeh.models.widgets.inputs import ColorPicker, Spinner
from definitions import OUTPUT_PATH, logger_f
import pandas as pd
from datetime import datetime
import contextily as cx
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib_scalebar.scalebar import ScaleBar
from bokeh.models import (
    ColumnDataSource,
    GeoJSONDataSource,
)
from bokeh.layouts import column, gridplot, grid
from bokeh.layouts import row as brow
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider
from xyzservices import TileProvider
import random
import sys


def change_crs(map_layer, crs_epsg):
    """Change the crs of a geopandasdataframes column in another dataframe, has to be the last column.

    Args:
        map_layer ([DataFrame]): with the last column GeoDataFrames
        crs_epsg ([Integer]): [four-digit epsg number]

    Returns:
        [DataFrame]: [input dataframe with changed CRS of the last column]
    """
    layers = pd.Series([lay.to_crs(epsg=crs_epsg) for lay in map_layer.iloc[:, -1]])
    map_layer.iloc[:, -1] = layers
    return map_layer


def get_cx_providers():
    """Get all built in providers of contextily in a flat directory.

    Returns:
        dictionary: flat dictionary of all contextily basemap providers
    """
    # code from: https://contextily.readthedocs.io/en/latest/providers_deepdive.html
    providers = {}

    def get_providers(provider):
        if "url" in provider:
            providers[provider["name"]] = provider
        else:
            for prov in provider.values():
                get_providers(prov)

    get_providers(cx.providers)

    return providers


# geopandasmapping
def map_gpd(map_layer, crs_epsg, provider, title, save_plot):
    """Create gpd plotly plot with given layers and basemap.

    Args:
        reverse_map (DataFrame): DataFrame. First columns are layer parameter with last column as layer GeoDataFrame
        crs_epsg (String): used EPSG
        basemap (String): Provider of the Contextily / xyzservices provider
        title (String): Title of the plot
        save_plot (Boolean): True: Save plot.

    Returns:
        gpd plotly figure: One plot with all given layers and given baselayer
    """
    logger_f.info("start mapping")
    start_time = datetime.now()

    fig, ax = plt.subplots(figsize=(10, 8))

    legend_elements = []
    zorder = 5
    for index, row in map_layer.iterrows():

        name = row[0].capitalize()
        color = row[1]
        geometry = row[-1]

        logger_f.info(f"start to plot: {row[0]}")

        # create colormap based on the given color
        cmap = ListedColormap([color], name=name)

        # work around to color the layer in one color and still manage the legend correctly
        geometry.insert(loc=geometry.shape[1] - 1, column="coloring", value=1)

        geometry.plot(ax=ax, column="coloring", cmap=cmap, categorical=True, legend=True, zorder=zorder)
        zorder += 5  # increase zorder for the next layer to plot the next on top

        # add legend_items and icon based on their geometry type
        if geometry.iloc[:, -1][index].geom_type == ("Point" or "MultiPoint"):
            legend_element = Line2D([0], [0], marker="o", color="w", label=name, markerfacecolor=color, markersize=10)
        elif geometry.iloc[:, -1][index].geom_type == ("LineString" or "LinearRing" or "MultiLineString"):
            legend_element = Line2D([0], [0], color=color, lw=2, label=name)
        elif geometry.iloc[:, -1][index].geom_type == ("Polygon" or "MultiPolygon" or "GeometryCollection"):
            legend_element = Patch(facecolor=color, edgecolor="black", label=name)
        else:
            logger_f.info(f"{name} layer could not be displayed in the legend due to mismatched geometrytype")
        legend_elements.append(legend_element)

    # reverse legend to account for the right order
    legend_elements = legend_elements[::-1]

    providers = get_cx_providers()

    try:
        cx.add_basemap(ax, source=providers[provider], crs=f"EPSG:{crs_epsg}")
        # bring the labels upfront if provider Stamen
        if "Stamen" in provider:
            cx.add_basemap(ax, source=cx.providers.Stamen.TonerLabels, crs=f"EPSG:{crs_epsg}", zorder=1000)
    except TimeoutError as err:
        logger_f.error("Connection to basemap provider could not be established. Check internet connection. Err:", err)
        sys.exit()
    except Exception as err:
        logger_f.error("Could not load baseap. Check connections:. Error:", err)
        sys.exit()

    # add legend and define position
    ax.legend(handles=legend_elements, frameon=False)
    leg = ax.get_legend()  # set legend's position and size
    leg.set_bbox_to_anchor((1.2, 0.3))

    font = {
        "family": "Verdana",
        "color": "black",
        "weight": "bold",
        "size": 20,
    }

    # set title
    ax.set_title(label=title, fontdict=font, pad=12)  # add title to map

    ax.set_axis_off()  # remove the axis ticks

    # add scalebar
    ax.add_artist(
        ScaleBar(
            dx=1,
            units="m",
            location="lower right",
            box_alpha=0.8,  # slight transparent box
        )
    )
    plt.tight_layout()  # adjust padding

    # save if wanted, default False
    title_underscore = title.replace(" ", "_")
    # title_underscore = title
    if save_plot:
        save_to = OUTPUT_PATH / f"{title_underscore}.png"
        plt.savefig(save_to)

    end_time = datetime.now() - start_time
    logger_f.info(f"mapping of {title} finished, Time elapsed: {end_time}")
    plt.show()


##################################### BOKEH #######################################################


def create_statistics(map_layer):
    """Return bokeh figure bar plot with number of elements per layer.

    Args:
        map_layer ([DataFrame]): [DataFrame. First columns are layer parameter with last column as layer GeoDataFrame]

    Returns:
        [bokeh figure]: [bokeh figure bar plot]
    """
    categories = list(map_layer["Name"])
    values = [len(map_layer["Layers"][i]) for i in range(len(map_layer))]

    color = list(map_layer["Color"])

    source = ColumnDataSource(data=dict(categories=categories, values=values, color=color))

    p = figure(x_range=categories, plot_height=300, title="Number of Elements")

    # create bar plot
    p.vbar(
        x="categories", top="values", width=0.9, fill_alpha=0.5, line_alpha=0.5, color="color", line_color="black", source=source
    )

    # when color is picked, this updates all bars and not only the one changed - no solution found
    # for index, picker in enumerate(pickers):
    #     picker.js_link("color", vbar.glyph, "fill_color")

    p.xgrid.grid_line_color = None

    p.xaxis.axis_label = "Layer"
    p.yaxis.axis_label = "Number of elements"

    return p


def map_bokeh(map_layer, provider, title, add_func=True):
    """Create bokeh plot with given layers and basemap.

    Args:
        reverse_map (DataFrame): DataFrame. First columns are layer parameter with last column as layer GeoDataFrame
        basemap (String): Provider of the Contextily / xyzservices provider
        title (String): Title of the plot
        add_func(Boolean): add additional functionality widgets to the plot (True) or not (False). Default: True.

    Returns:
        Bokeh plot: One plot with all given layers and given baselayer
    """
    logger_f.info("start mapping bokeh")
    start_time = datetime.now()

    p = figure(title=title, height=950, width=950, toolbar_location="right", tools="pan, wheel_zoom, box_zoom, reset , save")

    # hide grid
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    # hide axes
    p.axis.visible = False
    picker = None
    pickers = []
    spinners = []

    for index, row in map_layer.iterrows():
        name = row[0].capitalize()
        color = row[1]
        geom_layer = row[-1]

        logger_f.info(f"start to plot: {row[0]}")

        geosource = GeoJSONDataSource(geojson=geom_layer.to_json())

        ## POINTS
        if geom_layer.iloc[:, -1][index].geom_type == ("Point" or "MultiPoint"):

            points = p.circle("x", "y", source=geosource, color=color, size=10, legend_label=name)
            # p.add_tools(HoverTool(
            #     renderers = [points],
            #     tooltips = [("Name", name)]
            # ))
            picker = ColorPicker(title=f"{name} Point Color", color=color)
            picker.js_link("color", points.glyph, "fill_color")
            pickers.append(picker)

            spinner = Spinner(title=f"{name} size", low=1, high=40, step=1, value=10, width=80)
            spinner.js_link("value", points.glyph, "size")

            spinners.append(spinner)
        ## LINES
        elif geom_layer.iloc[:, -1][index].geom_type == ("LineString" or "LinearRing" or "MultiLineString"):

            lines = p.multi_line("xs", "ys", source=geosource, line_color=color, line_width=3, legend_label=name)
            picker = ColorPicker(title=f"{name} Line Color", color=color)
            picker.js_link("color", lines.glyph, "line_color")
            pickers.append(picker)

            spinner = Spinner(title=f"{name} size", low=1, high=20, step=0.5, value=3, width=80)
            spinner.js_link("value", lines.glyph, "line_width")

            spinners.append(spinner)
            # p.add_tools(HoverTool(
            #     renderers = [lines],
            #     tooltips = [("Highway", "@highway"),
            #                 ("Name", "@name")]
            # ))

        # POLYGONS
        elif geom_layer.iloc[:, -1][index].geom_type == ("Polygon" or "MultiPolygon" or "GeometryCollection"):
            polygons = p.patches(
                "xs",
                "ys",
                source=geosource,
                fill_color=color,
                line_color="black",
                line_width=0.25,
                fill_alpha=1,
                legend_label=name,
            )
            # p.add_tools(HoverTool(
            #     renderers = [polygons],
            #     tooltips = [("Name", name)]
            # ))
            picker = ColorPicker(title=f"{name} Polygon Color", color=color)
            picker.js_link("color", polygons.glyph, "fill_color")
            pickers.append(picker)
        else:
            logger_f.info(f"{name} layer geometrytype not found. Could not display layer")

    ######################### BASEMAP ##################################

    providers = get_cx_providers()

    # add basemap and labels
    private_provider = TileProvider(providers[provider])
    tile_provider = get_provider(private_provider)
    p.add_tile(tile_provider)

    # add labels if baselayer is Stamen -> only Stamen because not all other provider have an extra label baselayer
    # thus -> exclusive Stamen feature
    if provider.split(".")[0] == "Stamen":
        labels = "Stamen.TonerLabels"
        private_provider = TileProvider(providers[labels])
        tile_provider = get_provider(private_provider)
        p.add_tile(tile_provider, level="overlay")  # overlay -> put the labels on top of everything else

    ######################### Title and Legend #########################

    p.title.text = title
    p.title.align = "center"
    p.title.text_font_size = "40px"

    # adjust legend position and functions
    p.legend.location = "bottom_right"
    p.legend.click_policy = "hide"  # de-/activates layer
    p.legend.orientation = "vertical"

    # if multiple plots are required, skip adding additional functionality to plot
    if not add_func:
        return p

    # below would work with my own bokeh server -> surpasses this course unfortunately
    # would add the possiblitity to choose the background tile dynamically
    # add_select()

    ######################## Create Layout #############################

    p_stats = create_statistics(map_layer=map_layer)

    stats_col = column(p_stats)
    spinners_row = brow(spinners)
    pickers_col = column(pickers)

    col = column([pickers_col, spinners_row, stats_col])

    # I even opened a stackoverflow question to address this.. drove me nuts
    # see here for more details:
    # https://stackoverflow.com/questions/69545161/bokeh-widget-distorts-plot-with-tile-provider-why
    p.match_aspect = True

    # # create layout
    grid_layout = grid([p, col], ncols=2, sizing_mode="scale_both")

    # different way to create layout
    # l1 = grid([stats_col, pickers_col, spinners_row], sizing_mode="fixed")
    # grid_layout = grid([p, l1], ncols=2, sizing_mode="fixed")

    end_time = datetime.now() - start_time
    logger_f.info(f"mapping of {title} finished, Time elapsed: {end_time}")
    return grid_layout


def map_multiple(reverse_map, basemap, title):
    """Create grid with four bokeh figures with random baselayer.

    Args:
        reverse_map (DataFrame): DataFrame. First columns are layer parameter with last column as layer GeoDataFrame
        basemap (String): Provider of the Contextily / xyzservices provider
        title (String): Title of the plot


    Returns:
        Bokeh Gridplot: 2x2 grid with four plots with randomly different baselayer
    """
    logger_f.info("start mapping bokeh gridplot")
    start_time = datetime.now()
    providers = get_cx_providers()
    map_list = []
    for i in range(4):
        check = True
        # randomly choose a provider which does not require an API key (too comples for now)
        while check:
            provider = random.choice(list(providers.keys()))
            check = TileProvider(providers[provider]).requires_token()

        basemap = provider

        title = f"{provider}"
        add_func = False
        map_list.append(map_bokeh(reverse_map, basemap, title, add_func))

    # create 2x2 grid
    grid = gridplot(
        [[map_list[0], map_list[1]], [map_list[2], map_list[3]]], plot_width=600, plot_height=600, toolbar_location="right"
    )

    end_time = datetime.now() - start_time
    logger_f.info(f"mapping of {title} finished, Time elapsed: {end_time}")
    return grid


"""
below would work with my own bokeh server -> surpasses this course unfortunately
def add_select():
    tile_prov_select = Select(title="Tile Provider", value="NA", options=["OpenStreetMap c", "ESRI"])

    tiles = {"OpenStreetMap c": WMTSTileSource(url="http://c.tile.openstreetmap.org/{Z}/{X}/{Y}.png 1"),
            "ESRI": WMTSTileSource(url="https://server.arcgisonline.com/ArcGIS/
                                    rest/services/World_Imagery/MapServer/tile/{Z}/{Y}/{X}.jpg")}
    #callback
    def change_tiles_callback(attr, old, new):
        #removing the renderer corresponding to the tile layer
        p.renderers = [x for x in p.renderers if not str(x).startswith('TileRenderer')]
        #inserting the new tile renderer
        tile_renderer = renderers.TileRenderer(tile_source=tiles[new])
        p.renderers.insert(0, tile_renderer)

    # #Assign callback to select menu
    tile_prov_select.on_change("value", change_tiles_callback)
"""

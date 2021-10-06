from definitions import logger
import pandas as pd
from datetime import datetime
import contextily as cx
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib_scalebar.scalebar import ScaleBar


# made for two layer
def map_plotly(map_layer):
    """Plot all given layers on one map, based on the given parameters.

    Args:
        map_layer ([DataFrame]): [DataFrame with parameters and geometry GeoDataFrame as last column]
    """
    logger.info("start mapping")
    start_time = datetime.now()

    fig, ax = plt.subplots(figsize=(12, 8))

    legend_elements = []
    zorder = 5
    for index, row in map_layer.iterrows():

        name = row[0].capitalize()
        color = row[1]
        geometry = row[-1]

        logger.alter_format(name, "plotly")
        logger.info(f"start to plot: {row[0]}")

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
            logger.info(f"{name} layer could not be displayed in the legend due to mismatched geometrytype")
        legend_elements.append(legend_element)

    # reverse legend to account for the right order
    legend_elements = legend_elements[::-1]

    cx.add_basemap(ax, source=cx.providers.Stamen.TonerLite)

    # add legend and define position
    ax.legend(title="OSM layer", handles=legend_elements, frameon=False)
    leg = ax.get_legend()  # set legend's position and size
    leg.set_bbox_to_anchor((1.18, 0.3))

    font = {
        "family": "Verdana",
        "color": "black",
        "weight": "bold",
        "size": 20,
    }

    # set title
    ax.set_title(label="Map with OSM layers", fontdict=font, pad=12)  # add title to map

    # fig.suptitle("Map with OSM layers", fontsize=14, fontweight="bold")

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

    # plt.savefig("somename.png") # optional

    end_time = datetime.now() - start_time
    logger.info(f"download finished, Time elapsed: {end_time}")

    plt.show()


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

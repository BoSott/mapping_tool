from mercantile import Bbox
from definitions import DATA_PATH, ROOT_DIR, logger
import geopandas as gpd
from pathlib import Path
from datetime import datetime
import contextily as cx
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib_scalebar.scalebar import ScaleBar

def read_data(name):
    return gpd.read_file(DATA_PATH / name)


# made for two layer
def mapping(*argv):
    
    num = len(argv)    
    layer = [lay.to_crs(epsg=3857) for lay in argv] # important to convert to EPSG: 3857 (Sperical Mercator)
    
    
    pol = layer[0]
    fig, ax = plt.subplots(figsize=(10,10))
    
    # TODO need to incorporate a figure.. somehow somewhat https://kodu.ut.ee/~kmoch/geopython2020/L6/static-maps.html
    # possibly change the order 
    # ax = pol.geometry.boundary.plot(figsize=(10,10),
    #                                 color=None,
    #                                 edgecolor="black",
    #                                 linewidth=2)

    pol.geometry.boundary.plot(ax=ax,
                                color=None,
                                edgecolor="black",
                                linewidth=2)
    
    # lay1.plot(ax=ax)
    # lay2.plot(ax=ax)
    
    # add layer to map

    # for lay in layer[1:]:
    #     lay.plot(ax=ax)
    
    highways = layer[1]
    buildings = layer[2]
    
    cmap = ListedColormap(["grey"], name="highways")
    cmap2 = ListedColormap(["#094884"], name="buildings")
    
    highways["way"] = "way"
    buildings["buildings"] = "buildings"
    
    highways.plot(ax=ax,
                column="way",
                cmap=cmap,
                categorical=True,
                legend=True,
                label="Streets"
                )

    buildings.plot(ax=ax, 
                   column="buildings",
                   cmap=cmap2,
                   categorical=True,
                   legend=True,
                   label="Building")
                #    color="blue")
    
    
    legend_elements = [Line2D([0], [0], color='grey', lw=4, label='Streets'),
                #    Line2D([0], [0], marker='o', color='w', label='Streets',
                #           markerfacecolor='g', markersize=15),
                   Patch(facecolor='#094884', edgecolor='black',
                         label='Buildings')]
    
    
    # add baselayer
    cx.add_basemap(ax, source=cx.providers.Stamen.TonerLite)
    
    #add legend and title
    ax.legend(title="OSM layer", handles=legend_elements)
    leg = ax.get_legend() # set legend's position and size
    leg.set_bbox_to_anchor((1.15, 0.5))
    
    # fig.update_layout(legend=dict(
    #     yanchor="top",
    #     y=0.99,
    #     xanchor="left",
    #     x=0.01
    # ))
    
    ax.set(title="some title") # add title to map
    
    ax.set_axis_off() # remove the axis ticks
    
    ax.add_artist(ScaleBar(dx=1,
                           units="m",
                           location="lower right",
                           box_alpha=0.8, # slight transparent box
                           ))
    
    plt.tight_layout() # adjust padding
    
    # plt.savefig("somename.png") # optional
    
    plt.show()
    
# from https://medium.com/geekculture/plotting-maps-with-geopandas-and-contextily-8d4b1f02603d
def makeLayeredMap():
    """This function accepts an arbitrary number of geodataframes, plots them on top of a Contextily basemap. 
    NOTE: Please edit the Plotting-section to specify parameters for the number of layers and the formatting of each layer.
    Output: Saved file and layered map for display."""
    
    # Convert the CRS for all layers to EPSG3857 to match Contextily
    args = list(map(lambda x: x.to_crs(epsg=3857), args))
    # Create figure
    fig, ax = plt.subplots(1, figsize=(20, 20))
    #Set aspect to equal
    ax.set_aspect('equal')
    
    # PLOTTING: Specify layers to plot how to format each layer (colours, transparency, etc.):
    # Layer 1:
    args[0].boundary.plot(ax=ax, color='blue', edgecolor='k', alpha=0.5, zorder=1)
    # Layer 2:
    args[1].plot(ax=ax, color='blue', alpha=0.5, zorder=2)
    # ADD LAYERS here as needed:
    #args[2].plot(ax=ax, color='red', alpha=0.3, zorder=3)
    
    # Contextily basemap:
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)
    
    
    
    # Turn off axis
    ax.axis('off')
    # Save as file
    fig.savefig('layered_map.png', dpi=300) #Comment out or delete if you don't want a PNG image saved
    layered_map = plt.show()
    return(layered_map)


if __name__=="__main__":
    highways = read_data("highways.gpkg")
    buildings = read_data("buildings.gpkg")
    polygon = read_data("testpolygon.geojson")
    mapping(polygon, highways, buildings)


def somestuff():
    fig, axs = plt.subplots(1,2,sharey=True)
    ax1,ax2 = axs
    ax1.hist(data_a, alpha=0.5, color='navy', label="Data a")
    ax1.hist(data_b, alpha=0.5, color='darkred', label="Data b")
    ax2.hist(data_c, alpha=0.5, color='darkgreen', label="Data c")
    ax1.set_title("Two histograms")
    ax2.set_title("Another histogram")
    ax1.set_xlabel("Data values")
    ax2.set_xlabel("Other data values")
    ax1.legend()
    ax2.legend()
    ax1.set_ylabel("Frequency")
    for ax in axs:
        ax.grid(True, linestyle=':', which='major', color='black',  alpha=0.5)
        ax.set_axisbelow(True)
# https://docs.python-guide.org/writing/tests/
from context import src
import geopandas as gpd

from mapping import change_crs


print("Hello Test")

src.main.hello()

src.sample.sample2()


# test change_crs
data = [["highway", "red"]]
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy([8.42], [49.25]), crs="EPSG:4326")
gdf_crs = change_crs(gdf, 3857)
# assert if gdf crs changed from 4326 to 3875
# gdf_crs.iloc[:,-1][0].crs



# from mapping.py map_pyplot
if __name__=="__main__":
    # highways = read_data("highways.gpkg")
    # buildings = read_data("buildings.gpkg")
    # polygon = read_data("testpolygon.geojson")
    # mapping(polygon, highways, buildings)

    # data = [["highway", "red", highways]]
    
    # df = pd.DataFrame(data, columns=["Name", "Color", "layers"])
    
    # df2 = change_crs(df, 3857)
    # print(df2.iloc[:,-1][0].crs)
    pass
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






##################### ohsome API
def helper1():
    testpolstr = Path("C:/Users/Bosse/Documents/Uni/2_semester/Advanced_Geo/mapping/mapping_tool/data/testpolygon.geojson")
    testpol = gpd.read_file(testpolstr)
    time = None
    tagfilter1="highway=* and type:way"
    properties="tags"
    name1="highways"
    return name1, testpol, tagfilter1, time, properties


def helper2():
    testpolstr = Path("C:/Users/Bosse/Documents/Uni/2_semester/Advanced_Geo/mapping/mapping_tool/data/testpolygon.geojson")
    testpol = gpd.read_file(testpolstr)
    time = None
    tagfilter2="building=* and geometry:polygon"
    properties="tags"
    name2="buildings"
    return name2, testpol, tagfilter2, time, properties

if __name__=="__main__":
    # name1, testpol1, tagfilter1, time1, properties1 = helper1()
    name2, testpol2, tagfilter2, time2, properties2 = helper2()
    
    # download_osm(name=name1, filter=tagfilter1, time=time1, bpolys=testpol1, properties=properties1)
    download_osm(name=name2, filter=tagfilter2, time=time2, bpolys=testpol2, properties=properties2)
# advanced geoscripting project ideas

## packages
- GeoViews - PyViz/HoloViz https://geoviews.org/#, [example](https://towardsdatascience.com/interactive-geospatial-data-visualization-with-geoviews-in-python-7d5335c8efd1), [example2](https://towardsdatascience.com/how-to-visualize-data-on-top-of-a-map-in-python-using-the-geoviews-library-c4f444ca2929),
- Folium, on top of Leaflet.js, [example](https://codeburst.io/how-i-understood-displaying-interactive-maps-using-python-leaflet-js-and-folium-bd9b98c26e0e), [example2](https://python-bloggers.com/2020/12/how-to-make-stunning-interactive-maps-with-python-and-folium-in-minutes/), [example3](https://medium.com/@saidakbarp/interactive-map-visualization-with-folium-in-python-2e95544d8d9b), [example4](https://blog.prototypr.io/interactive-maps-with-python-part-1-aa1563dbe5a9) (this one is neat! **do this first**)
- [mapboxgl](https://github.com/mapbox/mapboxgl-jupyter), [example](https://www.earthdatascience.org/courses/scientists-guide-to-plotting-data-in-python/plot-spatial-data/customize-raster-plots/interactive-maps/)
- Plotly/Plotly Express, [example](https://python.plainenglish.io/how-to-create-a-interative-map-using-plotly-express-geojson-to-brazil-in-python-fb5527ae38fc), [example2](https://www.jphwang.com/interactive-maps-with-python-pandas-and-plotly/)
- Altair, [example](https://prog.world/how-to-make-an-interactive-map-using-python-and-open-source-libraries/) (also Plotly and Folium examples)
- IpyLeaflet
- KeplerGL for Jupyter [here](https://github.com/keplergl/kepler.gl/blob/master/docs/keplergl-jupyter/README.md) built on top of dek.gl
- Geopandas + [Contextily](https://github.com/geopandas/contextily) (basemaps) and [IPYMPL](https://github.com/matplotlib/ipympl) for interactive plots
- [bokeh](https://docs.bokeh.org/en/latest/index.html)
- Flask, [example](https://developer.here.com/blog/here-map-with-python-flask)
- Heroku [example](https://medium.com/analytics-vidhya/data-visualization-deploying-an-interactive-map-as-a-web-app-with-heroku-51a323029e4)
- OSMNX [example](https://towardsdatascience.com/making-artistic-maps-with-python-9d37f5ea8af0), [example2](https://towardsdatascience.com/creating-beautiful-maps-with-python-6e1aae54c55c)**sehr nices Weihnachtsgeschenk**
- Cartopy, [example](https://rabernat.github.io/research_computing_2018/maps-with-cartopy.html)

**focus:**
- folium, plotly, geopandas + contextily and IPYML (?),

## thematic topics



## data
- [crisis data](https://acleddata.com/data-export-tool/)
- airports world wide
- yeeey


## what ever else..

Comparison between multiple map creation libraries

Possible and required to build a tool?


Combine with docker setup?
https://www.youtube.com/watch?v=-lFuMQQ3qh8
https://github.com/maximilianKoeper/jupyter-notebook-on-docker-wsl2/blob/main/README.md
allerdings: warum? -> geht doch auch so?

or: focus on big data? The csv files are huge! Especially the ones from the US flights


-	Required time (speed)
-	Natively supported number of datapoints
-	Visual appeal
-	Quality of documentation
-	Simplicity of usage
-	Interactive possibilities


1.	Airport stuff
a.	Big data
b.	Cleaning the data might actually be already quite some work! -> airport thru data (-> airport is latest), SEQ_ID vs ID etc., only get one connection per route
c.	Requires database
d.	Produce one interactive map
e.	Maybe timeline
f.	Maybe filterable between multiple carriers, origin countries etc.
2.	Compare map creation packages (not so hyped)
3.	Create tool to create beautiful maps with different OSM layers

Dash

Basemap
Maßstab
Geoplot (mehrere Karten?)

Workflow ohsome
+ polygon und Co
+


Package bauen?



# NOTES

# setup of the module
- initialize git
- setup structure and architecture of the module (1. commit)

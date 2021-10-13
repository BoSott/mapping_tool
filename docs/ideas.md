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
- geoplot [Example](https://residentmario.github.io/geoplot/user_guide/Customizing_Plots.html) compare to this!

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


# extentions:
maybe improve polygon by including https://www.geoboundaries.org/index.html#getdata


# NOTES

# setup of the module
- initialize git
- setup structure and architecture of the module (1. commit)
- install requirements: geopandas, requests, ohsome [follow this guide](https://pypi.org/project/ohsome/)
- download data from ohsome
- load iput with Path from pathlib
- create static map with plotly



# MAPPING
### basemap
- use xyzservices as tile provider



plotly vs. geoplot


## plotly: + dash (?)
https://blog.matthewgove.com/2021/06/11/python-geopandas-easily-create-stunning-maps-without-a-gis-program/

https://github.com/derekbanas/plotly-tutorial/blob/master/Plotly%20Tut.ipynb

https://plotly.com/python/

https://towardsdatascience.com/mapping-geograph-data-in-python-610a963d2d7f

- getting the legend right is a pain in the ass!
alter legend text and sign answer: https://matplotlib.org/stable/gallery/text_labels_and_annotations/custom_legends.html



https://www.earthdatascience.org/courses/scientists-guide-to-plotting-data-in-python/plot-spatial-data/customize-vector-plots/python-customize-map-legends-geopandas/


## geoplot
https://towardsdatascience.com/visualizing-geospatial-data-in-python-e070374fe621




## bokeh
major problem: does not take geometry objects but only fking coordinates! MultiLinestring stuff was quite some work to get right
so eine Kacke.. GeoJSONDataSource hilft weiter wenn man das richtige File lädt..
https://pauliacomi.com/2020/06/07/plotly-v-bokeh.html

-> widget distorts the whole plot when you use it as before everything else
-> if you move the area of the plot first, no distortion happens

# text

guide to set up a mapping tool for automatic OSM downloading and displaying as a map
including:
- python environment with conda -> vs poetry? https://mitelman.engineering/blog/python-best-practice/automating-python-best-practices-for-a-new-project/
- project structure
- git and pre-commit hooks (black and flake8 -> PEP8 style guide)
- logging
- testing [pytest](https://mitelman.engineering/blog/python-best-practice/automating-python-best-practices-for-a-new-project/)
- documentation
- packages:
    - Path management using pathlib (?)
    - Clicks for a command line project
    - ohsome for downloading OSM data
    - plotly for static plots together with geopandas and contextily (+ interactivity?)
    - folium / geoplot / OSMNX?

maybe more:
- Mypy -> static type checker
- isort -> import sorting

setting up the environment
packages which ones and why

Generally: not very robust, difficulties towrite tests for the plotting functions -> too complex, output hard to verify or to falsify
-> depends very strongly on the correct input -> false input is not corrected and often not checked -> e.g. input polygon -> exists, name is correct but no geometry check


geopandas vs plotly: https://www.reaktor.com/blog/creating-an-interactive-geoplotting-demo-experiences-with-geopandas-and-plotly/


understanding plotly
https://plotly.com/python/figure-structure/
scaleabar: https://githubmemory.com/repo/ppinard/matplotlib-scalebar

in R:
https://bookdown.org/nicohahn/making_maps_with_r5/docs/tmap.html
might be the best option (?)



refinement:
change txt input to json

improve logging: -> errors are not logged well
1. https://coderzcolumn.com/tutorials/python/logging-config-simple-guide-to-configure-loggers-from-dictionary-and-config-files-in-python
2. https://coderzcolumn.com/tutorials/python/logging-simple-guide-to-log-events-in-python


# further
add hover tool with complete list of keys and values if value not None (?)
when changing color -> statistics do not change
can one change the tool so that the plot is the self of a class?

"""Handles Ohsome API OSM data extraction."""
from definitions import logger
from ohsome import OhsomeClient
from datetime import datetime
import sys


def download_osm(name, filter, time, bpolys, properties):
    """Download osm data via the ohsome extraction API.

    Args:
        name ([string]): [name of the layer]
        filter ([string]): [query for the ohsome api]
        time ([string]): [time parameter]
        bpolys ([gepandas dataframe]): [area of interest]
        properties ([string]): [what kind of property is requested, here: tags]
    """
    logger.alter_format(name, filter)
    logger.info("start downloading")
    start_time = datetime.now()

    client = OhsomeClient()
    response = client.elements.geometry.post(bpolys=bpolys, filter=filter, time=time, properties=properties)
    # TODO check if response is empty and if yes, log and skip
    try:
        response_gdf = response.as_dataframe()
    except TypeError as err:
        logger.error(
            "Error Type : {}, Error Message : {}".format(
                type(err).__name__, f"the ohsome request did not work. Check input for correct spelling and logic: {err}"
            )
        )
        sys.exit(1)

    end_time = datetime.now() - start_time
    logger.info(f"download finished, Time elapsed: {end_time}")
    return response_gdf


if __name__ == "__main__":
    pass

    # TODO
    # ohsome logs are not saved in the right place -> https://docs.ohsome.org/ohsome-api/stable/response-parameters.html

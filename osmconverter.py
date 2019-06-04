#!/usr/bin/env python
"""
OSM Projection Converter
Planning and Transport Research Centre (PATREC)

This script is used to convert OSM database files from one projection to 
another. Note it does use Python 2 as there seems to be some issues with 
geographic libraries on macOS with Python 3 still.
"""


__author__ = "Tristan Reed"
__version__ = "0.1.0"


""" Import required libraries. """
import json, geopandas, sys, textwrap
import shapely.geometry as shgeo
import xml.etree.ElementTree as ElementTree


def main():

    """ Check that we have supplied four arguments. """
    if (len(sys.argv) == 5):

        """ Open up the input file using ElementTree. """
        et_data = ElementTree.parse(sys.argv[1])

        """ Iterate through each element. """
        for element in et_data.getroot():

            """ See if it is the Bounds. """
            if (element.tag == "bounds"):

                """ Create a DataFrame from this. """
                bounds_gdf = geopandas.GeoDataFrame([
                    {"name": "min", "geometry": shgeo.Point(
                        float(element.attrib['minlon']), 
                        float(element.attrib['minlat']))},
                    {"name": "max", "geometry": shgeo.Point(
                        float(element.attrib['maxlon']), 
                        float(element.attrib['maxlat']))}], 
                    crs = "epsg:" + sys.argv[2])

                """ Adjust the GeoDataFrame to the correct one. """
                bounds_gdf = bounds_gdf.to_crs(crs = "epsg:" + sys.argv[4])

                """ Convert to a Dictionary. """
                bounds_dict = bounds_gdf.to_dict()

                """ Update the XML file. """
                print(bounds_dict)
                # element.update('minlon')
                # element.update('minlat')
                # element.update('maxlon')
            
            """ See if it is a Node. """
            if (element.tag == "node"):

                """ Create a DataFrame from this. """
                node_gdf = geopandas.GeoDataFrame([{"geometry": shgeo.Point(
                    float(element.attrib['lat']),
                    float(element.attrib['lon']))}],
                    crs = "epsg:" + sys.argv[2])

                """ Adjust the GeoDataFrame to the correct one. """
                node_gdf = node_gdf.to_crs(crs = "epsg:" + sys.argv[4])

                """ Convert to a Dictionary. """
                node_dict = node_dict.to_dict()
                #print(element.attrib)

    else:

        """ Print the help information for the user. """
        print(textwrap.dedent("""
        OSM Projection Converter: Usage Instructions
        --------------------------------------------
        osmconverter.py <in_file> <in_epsg> <out_file> <out_epsg>
        --------------------------------------------
        'in_file': path to the input network;
        'in_epsg': EPSG of the input network;
        'out_file': path to write the output network to;
        'out_epsg': EPSG of the output network.
        --------------------------------------------
        e.g.: osmconverter.py osm_network.osm 4326 osm_out.osm 28350
        """))


if __name__ == "__main__":

    """ This is executed when run from the command line. """
    main()

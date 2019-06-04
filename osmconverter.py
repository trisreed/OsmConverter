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
import functools, json, pyproj, sys, textwrap, tqdm
import shapely.geometry, shapely.ops # macOS is weird.
import xml.etree.ElementTree as ElementTree


def main():

    """ Check that we have supplied four arguments. """
    if (len(sys.argv) == 5):

        """ Open up the input file using ElementTree. """
        et_data = ElementTree.parse(sys.argv[1])

        """ Create the Input and Output EPSG PyProj objects. """
        source_proj = pyproj.Proj(init = 'epsg:' + sys.argv[2])
        dest_proj = pyproj.Proj(init = 'epsg:' + sys.argv[4])

        """ Create the Projection function. """
        projection = functools.partial(pyproj.transform, source_proj, dest_proj)

        """ Iterate through each element. """
        for element in tqdm.tqdm(et_data.getroot()):

            """ See if it is the Bounds. """
            if (element.tag == "bounds"):

                """ Project the minimun values. """
                min_proj = shapely.ops.transform(projection, 
                    shapely.geometry.Point(float(element.attrib['minlon']), 
                    float(element.attrib['minlat'])))

                """ Project the maximum values. """
                max_proj = shapely.ops.transform(projection, 
                    shapely.geometry.Point(float(element.attrib['maxlon']), 
                    float(element.attrib['maxlat'])))

                """ Update the XML file. """
                element.update('minlon', min_proj.x)
                element.update('minlat', min_proj.y)
                element.update('maxlon', max_proj.x)
                element.update('maxlat', max_proj.y)
            
            """ See if it is a Node. """
            if (element.tag == "node"):

                """ Project the maximum values. """
                node_proj = shapely.ops.transform(projection, 
                    shapely.geometry.Point(float(element.attrib['lon']), 
                    float(element.attrib['lat'])))

                """ Update the XML file. """
                element.update('lon', node_proj.x)
                element.update('lat', node_proj.y)
        
        """ Write the output to file. """
        et_data.write(sys.argv[3])

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

from app.utils.fs import get_files
import csv
from io import StringIO
from shapely import geos, wkt
from pathlib import Path

geos.WKBWriter.defaults['include_srid'] = True
point_cache = {}

def xyz_to_csv_buffer(path, layer_name):

    files = get_files(path + '/*')
    csv_buffer = StringIO()

    for file in files:
        #Parse the XYZ data, generate a new csv file with data for postgis bulk import
        #wkt.loads takes a few seconds to parse all of the points. Use caching for parsed points so that they can be re-used for subsequent years
        #row[0] = lat
        #row[1] = lon
        #row[2] = value
        date_string = Path(file).stem
        with open(file) as csvfile:
            data = list(csv.reader(csvfile, delimiter=' '))
            writer = csv.writer(csv_buffer, delimiter=',')
            for row in data: #[::10]:  # step every n rows to reduce resolution - need to do this properly
                
                point = f'POINT({row[0]} {row[1]})'
                if point in point_cache:
                    wkb_hex = point_cache[point]
                else:
                    p = wkt.loads(point)
                    geos.lgeos.GEOSSetSRID(p._geom, 4326)
                    wkb_hex = p.wkb_hex
                    point_cache[point] = wkb_hex

                if row[2] != 'nan':
                    writer.writerow([row[2], date_string, wkb_hex, layer_name])
    
    return csv_buffer

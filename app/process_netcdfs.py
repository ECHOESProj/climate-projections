from app.init import get_env
from app.utils.fs import ensure_folder
from osgeo import gdal
import pandas
from app.init import get_env
import xarray
import logging
import uuid
from os import path

from app.xyz_apply_transformation import xyz_apply_transformation
from app.xyz_filter_nan import xyz_filter_nan

temp_path = get_env('Temp_Dir') + '/climate_projections'
ensure_folder(temp_path)

#gdal.SetConfigOption('GDAL_NUM_THREADS', 'ALL_CPUS')

def calculate_levels(x, y, min_size):
    levels = []
    factor = 1
    while (x/factor > min_size) or (y/factor > min_size):
        factor *= 2
        levels.append(factor)
    return levels


def process_netcdfs(files, projWin = None, data_transform = None):
    logging.info(f'Processing {len(files)} netcdf file(s)')

    unique_path = f'{temp_path}/{str(uuid.uuid1())}'
    ensure_folder(unique_path)

    geotiff_path = path.join(unique_path, 'tif')
    ensure_folder(geotiff_path)

    xyz_path = path.join(unique_path, 'xyz')  
    ensure_folder(xyz_path)

    # loop through each netcdf file in the directory

    for f in files:
        logging.info(f'Processing NETCDF: {f}')
        gdal_dataset = gdal.Open(f)
        try:
            dataset = xarray.open_dataset(f)
        except:
            print(f'Could not open the file, or file is not a netcdf: {f}')
            continue

        # loop through each year
        for i, time in enumerate(dataset.variables['time'].data):
            
            # generate the current year date string in the required fromat
            date_string = pandas.to_datetime(str(time)).strftime('%Y%m%d')

            # First, convert NETCDF to GeoTIFF of the current band, cropping to projWin and reproject to 4326
            logging.info(f'Converting NETCDF band {i+1} to a GeoTIFF in 4326')
            geotiff_ds = gdal.Translate(
                f'{unique_path}/temp.tif',
                srcDS=gdal_dataset,
                format='GTiff',
                bandList=[i+1],
                noData='-nan',
                creationOptions=['ALPHA=YES']
            )
            logging.info(f'Reprojecting the GeoTIFF to 4326')
            wrap_options = gdal.WarpOptions(dstSRS='EPSG:4326')
            reprojected_ds = gdal.Warp(f'{unique_path}/temp_4326.tif', geotiff_ds, options=wrap_options)

            #  Next, convert the GeoTIFF to XYZ to extract the raw data
            logging.info(f'Creating temp_4326.xyz')
            xyz_file = f'{xyz_path}/{date_string}.xyz'
            xyz = gdal.Translate(
                xyz_file,
                format='XYZ',
                srcDS=reprojected_ds,
                projWin=projWin,
                projWinSRS='EPSG:4326'
            )    
            xyz = None
            xyz_filter_nan(xyz_file)
            if data_transform != None:
                logging.info(f'Applying data transformation')
                xyz_apply_transformation(xyz_file, data_transform)

            # Next, convert the XYZ back into a GeoTiff with compression and overviews
            logging.info(f'Compressing the reprojected GeoTIFF to {date_string}.tif')
            compressed_ds = gdal.Translate(
                f'{geotiff_path}/{date_string}.tif',
                srcDS=xyz_file,
                format='GTiff',
                creationOptions = ['ALPHA=YES', 'COMPRESS=LZW', 'PREDICTOR=2', 'TILED=YES'],
                outputSRS='EPSG:4326'
            )

            # logging.info(f'Adding overviews to {date_string}.tif')
            # #compressed_ds = gdal.Open(f'{geotiff_path}/{date_string}.tif', gdal.OF_RASTER | gdal.OF_READONLY)
            # levels = calculate_levels(compressed_ds.RasterXSize, compressed_ds.RasterYSize, 256)
            # gdal.SetConfigOption('COMPRESS_OVERVIEW', 'LZW')
            # gdal.SetConfigOption('PREDICTOR_OVERVIEW', '2')
            # compressed_ds.BuildOverviews('AVERAGE', levels)

            # # Use gdal.Translate to convert the current year band in the netcdf to a GeoTiff, using the original netcdf projection
            # logging.info(f'Converting NETCDF band {i+1} to a GeoTIFF')
            # geotiff_ds = gdal.Translate(
            #     f'{unique_path}/temp.tif',
            #     srcDS=gdal_dataset,
            #     format='GTiff',
            #     bandList=[i+1],
            #     noData='-nan',
            #     creationOptions=['ALPHA=YES']
            # )

            # # Use gdal.Warp to reproject to 4326 and save the geotiff with relavant name
            # logging.info(f'Reprojecting the GeoTIFF to 4326')
            # # #wrap_options = gdal.WarpOptions(dstSRS='EPSG:4326', srcSRS='EPSG:27700')
            # wrap_options = gdal.WarpOptions(dstSRS='EPSG:4326')
            # # #reprojected_ds = gdal.Warp(f'{geotiff_path}/{date_string}.tif', geotiff_ds, options=wrap_options)
            # reprojected_ds = gdal.Warp(f'{unique_path}/temp_4326.tif', geotiff_ds, options=wrap_options)

            # logging.info(f'Compressing the reprojected GeoTIFF to {date_string}.tif')
            # gdal.Translate(
            #     f'{geotiff_path}/{date_string}.tif',
            #     srcDS=reprojected_ds,
            #     format='GTiff',
            #     creationOptions = ['ALPHA=YES', 'COMPRESS=LZW', 'PREDICTOR=2', 'TILED=YES'],
            #     #creationOptions = ['ALPHA=YES', 'TILED=YES'],
            #     projWin=projWin,
            #     projWinSRS='EPSG:4326'
            # )

            # logging.info(f'Adding overviews to {date_string}.tif')
            # compressed_ds = gdal.Open(f'{geotiff_path}/{date_string}.tif', gdal.OF_RASTER | gdal.OF_READONLY)
            # levels = calculate_levels(compressed_ds.RasterXSize, compressed_ds.RasterYSize, 256)
            # gdal.SetConfigOption('COMPRESS_OVERVIEW', 'LZW')
            # gdal.SetConfigOption('PREDICTOR_OVERVIEW', '2')
            # compressed_ds.BuildOverviews('AVERAGE', levels)

            # # Use gdal.Translate to extract the raw data from the reprojected geotiff in XYZ format (csv)
            # logging.info(f'Creating {date_string}.xyz')
            # #xyz_paths.append(xyz_path)
            # xyz = gdal.Translate(
            #     f'{xyz_path}/{date_string}.xyz',
            #     format='XYZ',
            #     srcDS=compressed_ds,
            #     #creationOptions = ['ADD_HEADER_LINE=YES']
            # )

            # unload resources
            geotiff_ds = None
            reprojected_ds = None
            xyz = None
            compressed_ds = None

    return geotiff_path, xyz_path

from app.generate_sld import generate_sld
from app.get_xyz_max_min import get_xyz_max_min
from app.xyz_to_csv_buffer import xyz_to_csv_buffer
from app.data_sources.ceda_data import get_ceda_data
from app.process_netcdfs import process_netcdfs
from app.db import delete_climate_projections_data_by_layer, refresh_climate_projections_view, save_buffer_to_db
from app.data_sources.cds_data import get_cds_data
from app.utils.fs import clear_folder, copy_folder
from app.init import get_env, get_path
from app.utils.geo_server import publish_timeseries
import shutil
from os import path

temp_path = path.join(get_env('Temp_Dir'), 'climate_projections')
geoserver_workspace_name = get_env('GeoServer_Workspace')

# xMin, yMax, xMax, yMin
# ulx, uly, lrx, lry  
# http://bboxfinder.com Lng / Lat, Use Center tool on upper left, lower right
#projWin=[-180, 90, 180, -90],
projWin = [-12.8, 60, 3.4, 49.2]

def kelvinToCelsius(kelvin):
    return round(float(kelvin) - 273.15, 1)

def process_cds_data(coverage_name, name, attributes, sld, projWin = None, data_transform = None):

    geotiff_path, xyz_path = process_netcdfs(
        get_cds_data(
            name,
            attributes
        ),
        projWin,
        data_transform
    )

    csv_buffer = xyz_to_csv_buffer(
        xyz_path, f'{geoserver_workspace_name}:{coverage_name}')

    if isinstance(sld, str):
        style_data = open(get_path(sld))
    else:
        minValue, maxValue = get_xyz_max_min(xyz_path)
        style_data = generate_sld(
            name=coverage_name + '_style',
            min=minValue,
            max=maxValue,
            min_color=sld['min_color'],
            max_color=sld['max_color']
        )

    publish_timeseries(
        workspace_name=geoserver_workspace_name,
        store_name=coverage_name,
        layer_name=coverage_name,
        zip_path=create_timeseries_zip(geotiff_path),
        style_data=style_data,
        footprint=None,
        accurate_resolution_computation=True
    )

    delete_climate_projections_data_by_layer(
        f'{geoserver_workspace_name}:{coverage_name}')
    save_buffer_to_db(csv_buffer)


def process_ceda_data(coverage_name, ftp_path, sld, projWin = None, data_transform = None):
    geotiff_path, xyz_path = process_netcdfs(
        get_ceda_data(ftp_path),
        projWin,
        data_transform
    )

    csv_buffer = xyz_to_csv_buffer(
        xyz_path, f'{geoserver_workspace_name}:{coverage_name}')

    if isinstance(sld, str):
        style_data = open(get_path(sld))
    else:
        minValue, maxValue = get_xyz_max_min(xyz_path)
        style_data = generate_sld(
            name=coverage_name + '_style',
            min=minValue,
            max=maxValue,
            min_color=sld['min_color'],
            max_color=sld['max_color']
        )

    publish_timeseries(
        workspace_name=geoserver_workspace_name,
        store_name=coverage_name,
        layer_name=coverage_name,
        zip_path=create_timeseries_zip(geotiff_path),
        style_data=style_data,
        footprint=None,
        accurate_resolution_computation=True
    )

    delete_climate_projections_data_by_layer(
        f'{geoserver_workspace_name}:{coverage_name}')
    save_buffer_to_db(csv_buffer)


def create_timeseries_zip(path: str):
    copy_folder(get_path('assets/timeseries_files'), path)
    return shutil.make_archive(path, 'zip', path)


def climate_projections():
    clear_folder(temp_path)

    # https://www.color-hex.com/color-palettes/

    # https://cds.climate.copernicus.eu/cdsapp#!/dataset/sis-biodiversity-cmip5-global?tab=overview
    process_cds_data(
        'cds_temperature_annual_mean_rcp4_5',
        'sis-biodiversity-cmip5-global',
        {
            'version': '1.0',
            'format': 'zip',
            'variable': 'annual_mean_temperature',
            'model': 'hadgem2_cc',
            'ensemble_member': 'r1i1p1',
            'experiment': 'rcp4_5',
            'temporal_aggregation': 'annual',
        },
        {
            'min_color': '#fff5f0',
            'max_color': '#a50f15',
        },
        projWin,
        kelvinToCelsius
    )

    process_cds_data(
        'cds_precipitation_annual_maximum_of_daily_mean_rcp4_5',
        'sis-biodiversity-cmip5-global',
        {
                'version': '1.0',
                'format': 'zip',
                'variable': 'precipitation',
                'derived_variable': 'annual_maximum_of_daily_mean',
                'model': 'hadgem2_cc',
                'ensemble_member': 'r1i1p1',
                'experiment': 'rcp4_5',
                'temporal_aggregation': 'climatology',
                'statistic': 'mean',
        },
        {
            'min_color': '#f7fbff',
            'max_color': '#08306b',
        },
        projWin
    )

    process_cds_data(
        'cds_dry_days_annual_sum_rcp4_5',
        'sis-biodiversity-cmip5-global',
        {
            'version': '1.0',
            'format': 'zip',
            'variable': 'dry_days',
            'derived_variable': 'annual_sum',
            'model': 'hadgem2_cc',
            'ensemble_member': 'r1i1p1',
            'experiment': 'rcp4_5',
            'temporal_aggregation': 'annual',
        },
        {
            'min_color': '#eeeeee',
            'max_color': '#6f561f',
        },
        projWin
    )

    process_cds_data(
        'cds_volumetric_soil_water_annual_mean_rcp4_5',
        'sis-biodiversity-cmip5-global',
        {
            'version': '1.0',
            'format': 'zip',
            'variable': 'volumetric_soil_water',
            'derived_variable': 'annual_mean',
            'model': 'hadgem2_cc',
            'ensemble_member': 'r1i1p1',
            'experiment': 'rcp4_5',
            'temporal_aggregation': 'annual',
        },
        {
            'min_color': '#cde6f2',
            'max_color': '#0783bf',
        },
        projWin
    )

    process_cds_data(
        'cds_temperature_annual_mean_rcp8_5',
        'sis-biodiversity-cmip5-global',
        {
            'version': '1.0',
            'format': 'zip',
            'variable': 'annual_mean_temperature',
            'model': 'hadgem2_cc',
            'ensemble_member': 'r1i1p1',
            'experiment': 'rcp8_5',
            'temporal_aggregation': 'annual',
        },
        {
            'min_color': '#fff5f0',
            'max_color': '#a50f15',
        },
        projWin,
        kelvinToCelsius
    )

    process_cds_data(
        'cds_precipitation_annual_maximum_of_daily_mean_rcp8_5',
        'sis-biodiversity-cmip5-global',
        {
                'version': '1.0',
                'format': 'zip',
                'variable': 'precipitation',
                'derived_variable': 'annual_maximum_of_daily_mean',
                'model': 'hadgem2_cc',
                'ensemble_member': 'r1i1p1',
                'experiment': 'rcp8_5',
                'temporal_aggregation': 'climatology',
                'statistic': 'mean',
        },
        {
            'min_color': '#f7fbff',
            'max_color': '#08306b',
        },
        projWin
    )

    process_cds_data(
        'cds_dry_days_annual_sum_rcp8_5',
        'sis-biodiversity-cmip5-global',
        {
            'version': '1.0',
            'format': 'zip',
            'variable': 'dry_days',
            'derived_variable': 'annual_sum',
            'model': 'hadgem2_cc',
            'ensemble_member': 'r1i1p1',
            'experiment': 'rcp8_5',
            'temporal_aggregation': 'annual',
        },
        {
            'min_color': '#eeeeee',
            'max_color': '#6f561f',
        },
        projWin
    )

    process_cds_data(
        'cds_volumetric_soil_water_annual_mean_rcp8_5',
        'sis-biodiversity-cmip5-global',
        {
            'version': '1.0',
            'format': 'zip',
            'variable': 'volumetric_soil_water',
            'derived_variable': 'annual_mean',
            'model': 'hadgem2_cc',
            'ensemble_member': 'r1i1p1',
            'experiment': 'rcp8_5',
            'temporal_aggregation': 'annual',
        },
        {
            'min_color': '#cde6f2',
            'max_color': '#0783bf',
        },
        projWin
    )

    process_ceda_data(
        'ceda_temperature_yearly',
        'badc/ukcp18/data/land-cpm/uk/5km/rcp85/15/tas/ann/latest',
        {
            'min_color': '#fff5f0',
            'max_color': '#a50f15',
        },
        projWin
    )

    process_ceda_data(
        'ceda_wind_yearly',
        'badc/ukcp18/data/land-cpm/uk/5km/rcp85/15/sfcWind/ann/latest',
        {
            'min_color': '#afe0b5',
            'max_color': '#627b54',
        },
        projWin
    )

    process_ceda_data(
        'ceda_precipitation_yearly',
        'badc/ukcp18/data/land-cpm/uk/5km/rcp85/15/pr/ann/latest',
        {
            'min_color': '#cfe7f3',
            'max_color': '#1189c4',
        },
        projWin
    )

    process_ceda_data(
        'ceda_surface_snow_amount_yearly',
        'badc/ukcp18/data/land-cpm/uk/5km/rcp85/15/snw/ann/latest',
        get_path('assets/styles/ceda_snow.sld'),
        projWin
    )

    refresh_climate_projections_view()


# https://catalogue.ceda.ac.uk/uuid/e304987739e04cdc960598fa5e4439d0
# CEDA_TemperatureDir = badc/ukcp18/data/land-cpm/uk/5km/rcp85/15/tas/ann/latest
# CEDA_WindDir = badc/ukcp18/data/land-cpm/uk/5km/rcp85/15/sfcWind/ann/latest
# CEDA_PrecipitationDir = badc/ukcp18/data/land-cpm/uk/5km/rcp85/15/pr/ann/latest
# https://cds.climate.copernicus.eu/cdsapp#!/dataset/sis-biodiversity-cmip5-global?tab=overview
# # https://cds.climate.copernicus.eu/cdsapp#!/dataset/sis-temperature-statistics?tab=overview
# process_cds_data(
#     'cds_average_temperature_rcp4_5',
#     'sis-temperature-statistics',
#     {
#         'variable': 'average_temperature',
#         'period': 'year',
#         'statistic': 'time_average',
#         'experiment': 'rcp4_5',
#         'ensemble_statistic': 'ensemble_members_average',
#     },
#     {
#         'min_color': '#fff5f0',
#         'max_color': '#a50f15',
#     },
#     projWin
# )

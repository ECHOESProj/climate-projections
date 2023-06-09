from app.init import get_env, get_path
import psycopg2
import logging

hostname = get_env('PostgreSQL_Hostname')
username = get_env('PostgreSQL_Username')
password = get_env('PostgreSQL_Password')
database = get_env('PostgreSQL_Database')
schema = get_env('PostgreSQL_Schema')

conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
cursor = conn.cursor()

table_name = f'public."EchoesClimateProjections"' 
view_name = f'public."EchoesClimateProjectionsAvgGriddedView"' 


def refresh_climate_projections_view():
    logging.info(f'REFRESH MATERIALIZED VIEW {view_name} table')
    cursor.execute(f'''
        REFRESH MATERIALIZED VIEW {view_name};
    ''')
    conn.commit()

def clear_climate_projections_table():
    logging.info(f'Trucating {view_name} table')
    cursor.execute(f'''
        TRUNCATE TABLE {table_name};
    ''')
    conn.commit()

def delete_climate_projections_data_by_layer(layer):
    logging.info(f'Deleting rows from {table_name} where Layer is {layer}')
    cursor.execute(f'''
        DELETE FROM {table_name} WHERE "Layer" = '{layer}';
    ''')
    conn.commit()

def save_buffer_to_db(buffer): 
    #table_name = f'public."EchoesClimateProjections"' 
    buffer.seek(0)  
    
    # bulk insert data and map table columns to csv columns (by order)
    logging.info(f'Bulk insert data into table {table_name}')
    cursor.copy_from(buffer, table_name, columns=('"Value"', '"Date"', '"Point"', '"Layer"'), sep=',', null='')

    conn.commit()
    logging.info(f'Finished bulk insert')

# def create_climate_projections_table(table):
#     table_name = f'{schema}."{table}"'
#     logging.info('Dropping existing table')
#     drop = f'''
#         DROP TABLE IF EXISTS {table_name};
#     '''

# #        DROP INDEX IF EXISTS {schema}."{table}_Date_Index";
# #        DROP INDEX IF EXISTS {schema}."{table}_Point_Index";

#     cursor.execute(drop)
#     conn.commit()

#     logging.info(f'Creating table {table_name}')
#     # create table if doesn't exist
#     create_table = f'''
#         CREATE TABLE {table_name} (
#             "Id" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
#             "Point" geometry,
#             "Date" date,
#             "Value" numeric,
#             "Type" integer,
#             CONSTRAINT "{table}_pkey" PRIMARY KEY ("Id")
#         )

#         TABLESPACE pg_default;

#         CREATE INDEX "{table}_Date_Index"
#             ON {table_name} USING btree
#             ("Date" ASC NULLS LAST)
#             TABLESPACE pg_default;
        
#         CREATE INDEX "{table}_Point_Index"
#             ON {table_name} USING gist
#             ("Point")
#             TABLESPACE pg_default;   
#     '''
#     cursor.execute(create_table)
#     conn.commit()

# def empty_climate_projections_table():
#     logging.info(f'Clearing table {table_name}')
#     cursor.execute(f'truncate {table_name};')

# def save_buffer_to_db(table, buffer): 
#     table_name = f'{schema}."{table}"' 
#     buffer.seek(0)  
    
#     # bulk insert data and map table columns to csv columns (by order)
#     logging.info(f'Bulk insert data into table {table_name}')
#     cursor.copy_from(buffer, table_name, columns=('"Value"', '"Date"', '"Point"'), sep=',', null='')

#     conn.commit()
#     conn.close()
#     logging.info(f'Finished bulk insert')





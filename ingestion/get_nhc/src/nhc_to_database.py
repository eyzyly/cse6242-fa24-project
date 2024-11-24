import pandas as pd
import geopandas as gpd
import folium
import os

def nhc_to_gdf(folder:str):
    '''
    Takes as input a directory containing the zip files of NHC best track shapefiles and returns
    a dictionary of 4 merged GeoPandas geodataframes for points, lines, polygons, and radii. 
    See https://www.nhc.noaa.gov/gis/archive_besttrack.php for source data.
    '''
    # initialize the master gdfs
    gdf_points = gpd.GeoDataFrame()
    gdf_lines = gpd.GeoDataFrame()
    gdf_windswath = gpd.GeoDataFrame()
    gdf_radii = gpd.GeoDataFrame()

    # open storm names
    dict_stormNames = pd.read_csv('../data/raw/nhc/stormNames.csv').to_dict(orient='records')

    # loop through files
    for file in os.listdir(folder):
        
        # skip files that aren't zip
        if file.endswith('.zip'):
            zip_path = os.path.join(folder,file)
            storm_id = file.split('_best_track.zip')[0].upper()

            # create the storm's gdfs and add to master gdfs
            ## points
            try:
                ### handle nhc filename case inconsistentincy
                try:
                    temp_points = gpd.read_file(f"zip://./{zip_path}!{storm_id}_pts.shp")
                except:
                    temp_points = gpd.read_file(f"zip://./{zip_path}!{storm_id.lower()}_pts.shp")

                temp_points['stormid'] = storm_id
                temp_points.rename(columns={'YEAR': 'year'}, inplace=True)
                gdf_points = pd.concat([gdf_points, temp_points])
            except:
                pass

            ## lines
            try:
                ### handle nhc filename case inconsistentincy
                try:
                    temp_lines = gpd.read_file(f"zip://./{zip_path}!{storm_id}_lin.shp")
                except:
                    temp_lines = gpd.read_file(f"zip://./{zip_path}!{storm_id.lower()}_lin.shp")

                temp_lines['stormid'] = storm_id
                temp_lines['year'] = float(storm_id[-4:])
                gdf_lines = pd.concat([gdf_lines, temp_lines])
            except:
                pass

            ## windswath
            try:
                ### handle nhc filename case inconsistentincy
                try:
                    temp_windswath = gpd.read_file(f"zip://./{zip_path}!{storm_id}_windswath.shp")
                except:
                    temp_windswath = gpd.read_file(f"zip://./{zip_path}!{storm_id.lower()}_windswath.shp")

                temp_windswath['year'] = float(storm_id[-4:])
                gdf_windswath = pd.concat([gdf_windswath, temp_windswath])
            except:
                pass

            ## radii
            try:
                ### handle nhc filename case inconsistentincy
                try:
                    temp_radii = gpd.read_file(f"zip://./{zip_path}!{storm_id}_radii.shp")
                except:
                    temp_radii = gpd.read_file(f"zip://./{zip_path}!{storm_id.lower()}_radii.shp")
                temp_radii['year'] = float(storm_id[-4:])
                gdf_radii = pd.concat([gdf_radii, temp_radii])
            except:
                pass

    return {'points':gdf_points, 'lines':gdf_lines, 'windswath':gdf_windswath, 'radii':gdf_radii}

if __name__ == '__main__':

    # get the data in gdfs
    gdfs = nhc_to_gdf('../data/raw/nhc')

    #export to database
    gdfs['points'].to_file('../data/database/nhc.sqlite', driver='SQLite', spatialite=True, layer='points', crs='EPSG:4326')
    gdfs['lines'].to_file('../data/database/nhc.sqlite', driver='SQLite', spatialite=True, layer='lines', crs='EPSG:4326')
    gdfs['windswath'].to_file('../data/database/nhc.sqlite', driver='SQLite', spatialite=True, layer='windswath', crs='EPSG:4326')
    gdfs['radii'].to_file('../data/database/nhc.sqlite', driver='SQLite', spatialite=True, layer='radii', crs='EPSG:4326')

    # start a map with polygons as the bottom layer
    m = gdfs['windswath'].explore(color='gray', 
                                 style_kwds={'fillOpacity': 0.25},
                                 name='windswath')
    
    # add lines to the map
    gdfs['lines'].explore(
        m=m,
        column='SS', 
        cmap='Reds', 
        categories=[0, 1, 2, 3, 4, 5], 
        legend=True,
        legend_kwds = {'caption':'Category'},
        name='lines')
    
    # add a layer selector
    folium.LayerControl().add_to(m)
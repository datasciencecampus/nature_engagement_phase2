from model_config import *
from model_packages import *
from model_utils import *

import re

import add_counter_location_info 
import add_census_features_2021
import add_green_blue_infrastructure
import add_land_classification
import add_land_habitat_data
import add_dog_occupancy
import add_weather
import add_POIs
import add_strava_data
import add_counter_data

def counter_location_process_test_sites_data(config_file_path):
  file_dict=add_counter_location_info.get_config_file_paths(config_file_path)
  data= add_counter_location_info.load_counter_data_test_sites(file_dict)

  combined_df = []
  combined_anonymised_df=[]

  for provider, df in data.items():
      # Process each source data
      
      df = add_counter_location_info.assign_locations(df)  
      combined_df.append(df)
      anonymised_df= add_counter_location_info.anonymise_data(df, add_counter_location_info.rand_shift)
      combined_anonymised_df.append(anonymised_df)
      
    
  processed_df = pd.concat(combined_df, ignore_index=True)
  # keep only relevant columns
  processed_df= processed_df[['counter', 'lat', 'lon', 'geometry', 'provider', 'area','geom_type']]
  processed_df=processed_df.to_crs('EPSG:4326')
  processed_df.to_file(data_folder+'counter_locations/test_sites_counter_locations_processed.gpkg', crs= 'EPSG:4326')

  anonymised_df = pd.concat(combined_anonymised_df, ignore_index=True)
  # keep only relevant columns
  anonymised_df= anonymised_df[['counter', 'lat', 'lon', 'geometry', 'provider', 'area','geom_type']]
  anonymised_df=anonymised_df.to_crs('EPSG:4326')
  anonymised_df.to_file(data_folder+'counter_locations/test_sites_counter_locations_anonymised_processed.gpkg',crs= 'EPSG:4326' )

def census_process_test_sites_data():
    counter_info= gpd.read_file(data_folder+'counter_locations/counter_locations_processed.gpkg')

    household_occupancy_ftrs=['1-2 people in household','3+ people in household']
    age_ftrs=['Age group 0-25','Age group 25-65','Age group 65+']
    deprivation_ftrs=['Household is not deprived in any dimension','Household is deprived in at least 1 dimension']
    people_density_ftrs=['Population Density: Persons per square kilometre; measures: Value']
    econominc_activity_ftrs=['Economically active', 'Economic activity status: Economically inactive','Unemployed_population']
    health_ftrs=['Population in Good Health','Population in Bad Health']
    ethnic_ftrs=['White','Asian, Asian British or Asian Welsh','Mixed/Black/others']
    vehicle_ftrs=['Number of cars or vans: No cars or vans in household', 'Number of cars or vans: 1 car or van in household',\
                    '2 or more cars or vans in household']

    ftrs_sbset=[household_occupancy_ftrs,age_ftrs,deprivation_ftrs,econominc_activity_ftrs,health_ftrs,ethnic_ftrs,\
                    vehicle_ftrs]

    grouped_features= ['3+ people in household', '1-2 people in household', 'Age group 0-25', 'Age group 25-65', 'Age group 65+', 'Household is deprived in at least 1 dimension', 
        'Household is not deprived in any dimension','Economically active', 'Economic activity status: Economically inactive','Unemployed_population', 'Population in Good Health', 'Population in Bad Health', 
        'White','Asian, Asian British or Asian Welsh','Mixed/Black/others','Number of cars or vans: No cars or vans in household', 'Number of cars or vans: 1 car or van in household', '2 or more cars or vans in household',
        'Population Density: Persons per square kilometre; measures: Value']

    baseline_pop = ['1-2 people in household', 'Age group 65+', 'Household is not deprived in any dimension', 
                    'Economic activity status: Economically inactive','Population in Good Health', 'White', 'Number of cars or vans: 1 car or van in household']


    df_sites = gpd.read_file(data_folder+'counter_locations/test_sites_counter_locations_processed.gpkg')
    df_sites= df_sites[['counter', 'geometry', 'provider', 'geom_type']].reset_index(drop=True)

    df_census= pd.read_pickle(data_folder+'census_oa_shapefiles.pkl')

    # Intersect sites with Output Areas
    df_sites_oa = add_census_features_2021.intersect_sites_output_areas(df_sites, df_census)

    df_ur= pd.read_pickle(data_folder+'urban_rural_oa.pkl')

    # intersect updated census data with Census 2011 urban rural classification data
    df_sites_oa_ur= add_census_features_2021.intersect_sites_output_areas(df_sites_oa, df_ur)

    # Add area column
    df_sites_oa_ur['area_sq_km'] = add_census_features_2021.add_area_column(df_sites_oa_ur)

    # Save site info with raw census data
    df_sites_oa_ur.to_pickle(data_folder+'test_sites_raw_census_features_with_counter_info.pkl')

    df = df_sites_oa_ur
    
    
    # groups census features into larger and more relevant caetgories e.g. 3+ people in household
    grouped_census = add_census_features_2021.engineer_features(df)
    
    # # Get proportion of features in each subset (e.g. proportion of 'Age group 0-25' in ['Age group 0-25','Age group 25-65'])
    for cols in ftrs_sbset:   
        grouped_census[cols]=get_proportion(grouped_census, cols)

    grouped_census= grouped_census.groupby('counter').mean(numeric_only=True).reset_index()
    # merge with counter info to get provider column for subsetting
    grouped_census= grouped_census.merge(df_sites[['counter', 'provider', 'geometry', 'geom_type']], on='counter')
    # save features as static training data. Other input features will be added to this static data set.
    grouped_census.to_pickle(data_folder + 'test_sites_static_data.pkl')

def gree_blue_infrastructure_process_test_sites_data():
    sites_df= gpd.read_file(data_folder+'counter_locations/test_sites_counter_locations_processed.gpkg')
    sites_df= sites_df[['counter', 'geometry', 'provider', 'geom_type']].reset_index(drop=True)
    sites_df= sites_df.to_crs(crs_mtr)

    # Overlay data onto counter locations

    # green area
    green_overlay = add_green_blue_infrastructure.overlay_with_buffers(gpd.read_file(data_folder+'infrastructure_green.gpkg'), sites_df, False)
    # rename variable and adjust units
    green_overlay['accessible_green_space_area']=green_overlay['area']/(10**6)
    
    # PRoW- this has to be processed differently to the other variables
    prow_lengths= gpd.read_file(data_folder+'infrastructure_prow.gpkg') 
    prow_overlay = prow_lengths.to_crs(crs_mtr).overlay(sites_df,how='intersection')
    prow_overlay= prow_overlay.groupby('counter')['PROW_Total_length_m'].sum().reset_index()
    prow_overlay= prow_overlay[['counter', 'PROW_Total_length_m']]
    # rename variable and adjust units
    prow_overlay['PROW_Total_length_km']=prow_overlay['PROW_Total_length_m']/(10**3)

    # waterside
    waterside_overlay = add_green_blue_infrastructure.overlay_with_buffers(gpd.read_file(data_folder+'infrastructure_waterside.gpkg'), sites_df, True)
    # rename variable and adjust units
    waterside_overlay['waterside_length_km']=waterside_overlay['length']/(10**3)

    # Combine all features to a single data frame
    features = reduce(lambda df1,df2: pd.merge(df1,df2, on='counter'), [green_overlay, prow_overlay, waterside_overlay])
    features= features[['counter','accessible_green_space_area', 'PROW_Total_length_km', 'waterside_length_km']]
    
    # add new variables to static data set
    static= pd.read_pickle(data_folder + 'test_sites_static_data.pkl')
    static= pd.merge(features, static, on='counter', how='inner')
    static.to_pickle(data_folder+'test_sites_static_data.pkl')

def land_classification_process_test_sites_data():
  
    # constants

    # load rural/urban features from raw census data
    dataset = pd.read_pickle(data_folder+'raw_census_features_with_counter_info.pkl')
    dataset = dataset.groupby(['counter', 'urban_rural'])['area_sq_km'].sum().reset_index()

    # load counter locations _data
    locations_buffer = gpd.read_file(data_folder+'counter_locations/counter_locations_processed.gpkg').to_crs(crs_deg)

    # This mapping has to be determined manually and will need reviewing as more counter dat is input
    urbn_url_clstr_map = dict(zip([2,1,0,-1], ['rural_settings','major_urban_settings','minor_urban_settings','mixed_settings']))

    # load rural/urban features from raw census data
    dataset = pd.read_pickle(data_folder+'test_sites_raw_census_features_with_counter_info.pkl')
    dataset = dataset.groupby(['counter', 'urban_rural'])['area_sq_km'].sum().reset_index()

    locations_buffer = gpd.read_file(data_folder+'counter_locations/test_sites_counter_locations_processed.gpkg').to_crs(crs_deg)
    sites_profile = locations_buffer[['counter','geometry']].merge(dataset, on=['counter'], how='inner')
    sites_profile['geometry'] = sites_profile['geometry'].centroid
    sites_profile = sites_profile[['counter','geometry','urban_rural','area_sq_km']]

    # create coordinates for clustering and format df containing rural/urban features 
    sites_profile_pv = sites_profile.pivot_table('area_sq_km', ['counter'], 'urban_rural')
    sites_profile_pv.reset_index(drop=False, inplace=True)


    colm_nams = sites_profile_pv.columns
    sites_profile_pv = sites_profile_pv.reindex(colm_nams, axis=1).fillna(0)
    sites_profile_pv = sites_profile_pv.rename_axis(None, axis=1)


    sites_profile = sites_profile_pv.copy()
    sites_profile = locations_buffer[['counter','geometry']].merge(sites_profile, on=['counter'], how='inner')
    sites_profile['geometry'] = sites_profile['geometry'].centroid


    coordinates = sites_profile.select_dtypes(include=np.number).values

    # perform clustering to assign labels
    labels = add_land_classification.cluster(coordinates)

    # use label mapping to give meaning to clustering assigned lables
    sites_profile = add_land_classification.assign_labels(sites_profile, labels)

    # add new variables to static data set
    static= pd.read_pickle(data_folder + 'test_sites_static_data.pkl')
    static= pd.merge(sites_profile[['counter','land_type_labels']], static, on='counter', how='inner')
    static.to_pickle(data_folder+'test_sites_static_data.pkl')

def land_habitat_process_test_sites_data():
    
    habitat_df = add_land_habitat_data.process_habitat_data()

    #load counter locations _data
    locations_buffer_ts = gpd.read_file(data_folder+'counter_locations/test_sites_counter_locations_processed.gpkg').to_crs(crs_mtr)

    sites_df = add_land_habitat_data.get_site_buffers(locations_buffer_ts)

    sites_habitat_df = add_land_habitat_data.intersect_with_habitat(sites_df, habitat_df)

    sites_df_habitat_cover_pv = add_land_habitat_data.calculate_habitat_areas(sites_habitat_df, locations_buffer_ts)

    coordinates = sites_df_habitat_cover_pv.select_dtypes(include=np.number).values

    labels = add_land_habitat_data.get_cluster_labels(coordinates)

    sites_df_habitat_cover_pv= add_land_habitat_data.assign_labels(sites_df_habitat_cover_pv, labels)
    
    # add new variables to static data set
    static= pd.read_pickle(data_folder + 'test_sites_static_data.pkl')
    static= pd.merge(sites_df_habitat_cover_pv[['counter','land_habitat_labels']], static, on='counter', how='inner')
    static.to_pickle(data_folder+'test_sites_static_data.pkl')


def dog_process_test_sites_data():
  # load PNAS curvey data
  df = add_dog_occupancy.load_survey_data()

  world = gpd.read_file(world_boundaries)
  uk = world[world.name == 'U.K. of Great Britain and Northern Ireland']

  
  # load counter locations _data
  sites_df = gpd.read_file(data_folder+'counter_locations/test_sites_counter_locations_processed.gpkg').to_crs(crs_mtr)
  sites = sites_df.overlay(uk.to_crs(crs_mtr), how='intersection')

  gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Visit_Longitude, df.Visit_Latitude)).set_crs(crs_deg)
  gdf = gdf.to_crs(crs_mtr)

  intersect_df = gdf.sjoin(sites, how="left", op='intersects').dropna(subset=['counter'])
  intersect_df = intersect_df.to_crs(crs_deg)

  # get mean dog occupancy for each site
  
  intersect_df['Dog'] = intersect_df['Dog'].eq('Yes').mul(1)

  dog_occupancy = intersect_df.groupby('counter')[['No_Of_Visits', 'Dog']].mean().reset_index()
  dog_occupancy = sites_df[['counter','geometry']].merge(dog_occupancy, on=['counter'])
  dog_occupancy['geometry'] = dog_occupancy['geometry'].centroid

  # add new variables to static data set
  static= pd.read_pickle(data_folder + 'test_sites_static_data.pkl')
  static= pd.merge(dog_occupancy[['counter', 'Dog']], static, on='counter', how='inner')
  static.to_pickle(data_folder+'test_sites_static_data.pkl')

def weather_process_test_sites_data():
  # Constants
    START_DATE = datetime(2020, 1, 1)
    END_DATE = datetime(2023, 9, 30)

    site_locations=gpd.read_file(data_folder+'counter_locations/test_sites_counter_locations_processed.gpkg')
    
    # Get weather data
    weather_df = add_weather.get_weather_data(site_locations)  
    # Clean data
    weather_df = add_weather.clean_weather_data(weather_df)
    # Save cleaned data
    weather_df.to_pickle(data_folder+'test_sites_weather_data.pkl')

def pois_process_test_sites_data():

    # constants
    # # POIs to use in count_pois function
    # pois=["amenity","tourism","highway"]

    sel_colms = ["element_type", "osmid", "amenity", "geometry", "tourism", "highway"]
    desired_columns = ["element_type", "osmid", "amenity", "geometry", "tourism", "highway"]

    df_loc= gpd.read_file(data_folder+'counter_locations/test_sites_counter_locations_processed.gpkg')

    unique_providers = df_loc['provider'].unique()
    all_provider_pois = []

    for provider in unique_providers:
        provider_pois = add_POIs.process_single_provider(df_loc, provider)
        all_provider_pois.append(provider_pois)

    # Combine all provider POIs into a single DataFrame
    combined_pois = pd.concat(all_provider_pois).reset_index(drop=True)
    # combined_pois= combined_pois.drop(['amenity_count', 'tourism_count', 'highway_count'], axis=1)
    combined_pois= combined_pois.merge(df_loc[['area', 'counter']],on=['counter'],how='inner')
    
    num_cols=[x for x in combined_pois.columns if x not in ['area_sq_km','counter']]

    # # Density of pois
    combined_pois[num_cols]=combined_pois[num_cols].div(combined_pois['area'],axis=0)

    del combined_pois['area']

    # add new variables to static data set
    static= pd.read_pickle(data_folder + 'test_sites_static_data.pkl')
    static= pd.merge(combined_pois, static, on='counter', how='inner')
    static.to_pickle(data_folder+'test_sites_static_data.pkl')

def strava_process_test_sites_data(provider, strava_data_loc):

    remove_suffix = '_1_edge_daily_2020-01-01-2023-09-30_ped'

    # counter_info_loc= counter_info_loc.strip("'")
    counters= gpd.read_file(data_folder+'counter_locations/test_sites_counter_locations_processed.gpkg')
    loc_names= counters.counter
    add_strava_data.clean_folder_names(strava_data_loc, remove_suffix)
    # process strava data
    strava_count = prepare_strava(loc_names, strava_data_loc)
    strava_count.head()
    merged= strava_count[['total_trip_count', 'Date', 'site']].merge(counters, how='inner',left_on=['site'],\
                                            right_on=['counter'])
    merged.to_pickle(data_folder+f'test_sites/strava_data_{provider}.pkl')

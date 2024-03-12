from model_packages import *


data_folder='./data/'


data_folder_updated='./data/strava_and_counter_data_updated/'


data_folder_census='./data/census_2021/'

strava_data_loc_hourly='./data/strava_and_counter_data_updated/selected_area_hourly_2022-01-01-2023-01-01_ped/'

#strava_data_loc_monthly='./data/strava_and_counter_data_updated/selected_area_monthly_jan_2019-aug_2023_ped_leisure/'

#strava_data_loc_monthly='./data/strava_and_counter_data_updated/windermere/'

#strava_data_loc_monthly='./data/strava_and_counter_data_updated/monthly_data/'

#strava_data_loc_monthly='./data/strava_and_counter_data_updated/london/'

#strava_data_loc_monthly='./data/strava_and_counter_data_updated/london_2/'

#strava_data_loc_monthly='./data/strava_and_counter_data_updated/lake_district/'

#strava_data_loc_monthly='./data/strava_and_counter_data_updated/carlisle/'

strava_data_loc_nr='./data/strava_and_counter_data_updated/nature_reserves_data/'

strava_data_loc_np='./data/strava_and_counter_data_updated/national_park_data/'


cenus_ethnc_parish=data_folder_census+'ethnicity_2021_parish.csv'

cenus_table_parish=data_folder_census+'parish_lookup_in_england_and_wales.csv'


shapefile_parish=data_folder_census+'parish_shapefile/'


cenus_ethnc_ward=data_folder_census+'ethnicity_2021_ward.csv'


cenus_densty_ward=data_folder_census+'density_2021_ward.xlsx'


cenus_cars_ward=data_folder_census+'cars_hh.xlsx'

cenus_age_ward=data_folder_census+'age.xlsx'

cenus_hh_ward=data_folder_census+'hh.csv'


shapefile_ward=data_folder_census+'ward_shapefile/'


#strava_data_loc_monthly='./data/strava_and_counter_data_updated/selected_area_monthly_jan_2019-jan_2023_ped_leisure/'

#strava_data_loc_monthly='./data/strava_and_counter_data_updated/selected_area_daily_2019-08-01-2023-08-01_ped_leisure/'

#strava_data_loc_monthly='./data/strava_and_counter_data_updated/selected_area_monthly_aug_2019-aug_2023_ped_leisure/'

shp_data=data_folder+'NE_EnglandCoastPathRoute_SHP_Full/data/'

nature_reserve_data=data_folder+'NE_NationalNatureReservesEngland_SHP_Full/data/'

national_park_data=data_folder+'NE_NationalParksEngland_SHP_Full/data/'

rcrntl_data=data_folder+'recreational_datasets/'

countr_locn_file=data_folder+'counter_location_bng.gpkg'

val_countr_locn_file=data_folder+'north_downs_way_counter_location_bng.gpkg'


addtnl_countr_locn_file=data_folder+'canals_and_rivers_trust_counter_locations_bng.gpkg'

# This might not be a good option: cj 14-11-2022

census_locn_file_data=data_folder+'census/'


# Explore this  option: cj 14-11-2022

census_locn_file=data_folder+'census_oa_socio_economic_ftrs.pkl'


land_cluster_file=data_folder+'rural_urban_clusters.pkl'


habitat_cluster_file=data_folder+'land_habitat_clusters.pkl'


data_loc_ne_habitat=data_folder+'ne_living_habitat.pkl'

dog_ownership=data_folder+'dog_occupancy_sites.pkl'

nature_srvy_visits=data_folder+'nature_survey_time_series_data.pkl'

#green_infstrcr='dist_green_space.pkl'

green_infstrcr=data_folder+'green_infrastructure.pkl'


weathr_data=data_folder+'weather_df.pkl'

crs_deg="EPSG:4326"

crs_mtr="EPSG:27700"

#countr_dat_file=data_folder+'raw_counter_data_daily_27-07-22.csv'



#countr_dat_file=data_folder_updated+'counter_and_strava_data_01-20_to_09-22/'+'natural_england_national_trails_people_counters_daily.csv'

countr_dat_file=data_folder_updated+'data_01-2020_to_11-2022/'+'natural_england_national_trails_people_counters_daily.csv'



#val_countr_dat_file=data_folder_updated+'counter_and_strava_data_01-20_to_09-22/'+'north_downs_way_people_counters_daily.csv'


val_countr_dat_file=data_folder_updated+'data_01-2020_to_11-2022/'+'north_downs_way_people_counters_daily.csv'

#cut-off year for reading counter data
cnt_ct_off_yr=2020

cnt_ct_off_yr_ne=2020

cnt_ct_off_yr_nd=2021

# cut-off % to keep columns with missing values below null_prcntg(%) in the counter data set 

null_prcntg=50


null_prcntg_mnthly=25

# whether to apply smoothening flag

apply_smtheng_flg=True

# window length to pad the sequence while applying smoothening
# The following has been chosen with monthly aggregation in mind (freq ~M)
# For different sampling frequencies, different window_len might be optimal
window_len=4

#List of allowed smoothening functions
#lst_smthers=['exp','conv','sptrl','poly','splne','gaussn','binr','lwes','klmn']



whch_smther='exp'

#create subdirectories for storing STRAVA metro data for corresponding counter sites
#strava_data_loc=data_folder+'NE_people_counter/'

#strava_data_loc=data_folder_updated+'counter_and_strava_data_01-20_to_09-22/'+'natural_england_national_trails_strava_single_edge/'


strava_data_loc=data_folder_updated+'data_01-2020_to_11-2022/'+'natural_england_national_trails_strava_single_edge/'


#val_strava_data_loc=data_folder_updated+'counter_and_strava_data_01-20_to_09-22/'+'north_downs_way_strava_single_edge/'

val_strava_data_loc=data_folder_updated+'data_01-2020_to_11-2022/'+'north_downs_way_strava_single_edge/'


canal_trust_strava_data_loc=data_folder_updated+'data_01-2020_to_11-2022/'+'canals_and_rivers_trust_strava_single_edge/'

# Which STRAVA feature to be used in modelling while building a regression
# model for Natural england counter dataset as the target variable.
chsen_ftr_strava='total_trip_count'#'forward_trip_count'


#target feature
target='NE_counter'




# maximum distance to look for pois around a point
scng_dist_pois=5000 #(in metres)

# buffer zones to count the number of recreational sites
buffr_zone_dist_rcrtnl=0.1
# buffer zones in metres 1000m ~ 1km
bufr_zones_mrts=5000

bufr_zones_mrts_cnsus=5000


# buffer zones to get the socio-economic and demographic features around people counter locations
buffr_zone_dist_demogrphc=0.1

vif_threshld=5 # ideally <10

 
# start and end dates for retrieving weather data
start = datetime(2020, 1, 1)
end = datetime(2022, 12, 31)


# accesibility
accesb_area_file='accessibility.shp'


GI_Access_maps='/Users/cjoshi/Downloads/Green_and_Blue_Infrastructure_Opendata_NE_Geopackage/GI_Access_maps/GI_Access_maps.gpkg'




Blue_Infrastructure_Waterside='/Users/cjoshi/Downloads/Green_and_Blue_Infrastructure_Opendata_NE_Geopackage/Blue_Infrastructure_Waterside/Blue_Infrastructure_Waterside.gpkg'


world_boundaries=data_folder+'world-administrative-boundaries'

survey=data_folder+'survey/'

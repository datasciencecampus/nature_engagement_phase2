

from model_config import *
from model_packages import *
from model_utils import *

# Constants
census_locn_file_data
data_folder
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

# process raw census data downloads
def load_shapefiles_2021():
    """Loads Output Area shapefiles."""
    df = gpd.read_file(census_locn_file_data + '/England_oa_2021')
    df = df[['oa21cd', 'geometry']]
    df.rename(columns={'oa21cd': '2021 output area'}, inplace=True)
    return df

def load_shapefiles():
    """Loads Output Area shapefiles."""
    df = gpd.read_file(census_locn_file_data + '/infuse_oa_lyr_2011')
    df = df[df['geo_code'].str.lower().str.startswith('e')]
    df = df[['geo_code', 'geometry']]
    df.rename(columns={'geo_code': '2011 output area'}, inplace=True)
    return df

def load_urban_rural_data():
    """Loads urban/rural classification for Output Areas."""
    df = pd.read_csv(census_locn_file_data + 'RUC11_OA11_EW.csv', skiprows=0)
    df = df[df['OA11CD'].str.lower().str.startswith('e')]
    df = df[['OA11CD', 'RUC11']].reset_index(drop=True)
    df.rename(columns={'OA11CD': '2011 output area', 'RUC11': 'urban_rural'}, inplace=True)
    return df
    
def merge_urban_rural_shapefiles(df_shapefiles, df_urban_rural):
    """Merges urban/rural data with shapefiles."""
    return df_shapefiles.merge(df_urban_rural, on='2011 output area', how='inner').dropna().reset_index(drop=True)

def load_census_data():
    """Loads all census data."""
    dfs = []
    for filename in ['household_occupancy_2021', 'age_groups_2021', 'deprivation_dimension_2021', 
                     'population_density_2021', 'economic_activity_2021', 'population_health_2021',
                     'ethnicity_2021', 'cars_2021']:
        df = pd.read_csv(census_locn_file_data + filename + '.csv')
        df = df.set_index('2021 output area')
        dfs.append(df)
    return pd.concat(dfs, axis=1).reset_index()

def merge_census_ur(df_census, df_shapefiles):
    """Merges census data with shapefiles."""
    return df_census.merge(df_shapefiles, on='2021 output area', how='inner').dropna().reset_index(drop=True)

def save_data(df, filename):
    """Saves dataframe to pickle file."""
    df.to_pickle(data_folder + filename)






# functions to add census data to counter loctions.
def load_site_data():
    """Loads people monitoring site data."""
    df = gpd.read_file(data_folder + 'counter_locations/counter_locations_processed.gpkg')
    return df[['counter', 'geometry', 'provider', 'geom_type']].reset_index(drop=True)

def intersect_sites_output_areas(df_sites, df_census):
    """Intersects sites with Output Areas to get census data."""
    return df_sites.overlay(gpd.GeoDataFrame(df_census).to_crs(crs_deg), how='intersection')

def add_area_column(df):
    """Adds area column to dataframe."""
    return df.area / 10**6  








# census data processing from 8.data_augmentation

def get_area_sites(df):
    """Calculates area of buffer region around each site."""
    # Buffer zone is 5km radius around each site: pi*r^2 = 78.5 sq km
    return df.groupby('counter')['area'].sum().reset_index()

def engineer_features(df):
    """Engineers new features from existing columns."""

    # Define collective features
    df['3+ people in household'] = df[['3 people in household','4 people in household',\
                                           '5 people in household','6 people in household',\
                                           '7 people in household','8 or more people in household']].sum(axis=1) 

    # drop non-grouped features 
    df= df.drop(columns= ['3 people in household','4 people in household',\
                                           '5 people in household','6 people in household',\
                                           '7 people in household','8 or more people in household'], axis=1)


    df['1-2 people in household'] = df[['1 person in household','2 people in household']].sum(axis=1)
     # drop non-grouped features 
    df= df.drop(columns= ['1 person in household','2 people in household'], axis=1)

    household_occupancy_ftrs=['1-2 people in household','3+ people in household']

    # Age groups
    df['Age group 0-25'] = df[['Age: Aged 4 years and under','Age: Aged 5 to 9 years','Age: Aged 10 to 14 years','Age: Aged 15 to 19 years','Age: Aged 20 to 24 years']].sum(axis=1)
    df['Age group 25-65'] = df[['Age: Aged 25 to 29 years','Age: Aged 30 to 34 years','Age: Aged 35 to 39 years','Age: Aged 40 to 44 years','Age: Aged 45 to 49 years','Age: Aged 50 to 54 years','Age: Aged 55 to 59 years','Age: Aged 60 to 64 years']].sum(axis=1) 
    df['Age group 65+'] = df[['Age: Aged 65 to 69 years','Age: Aged 70 to 74 years','Age: Aged 75 to 79 years','Age: Aged 80 to 84 years','Age: Aged 85 years and over']].sum(axis=1)
    
    # drop non-grouped features 
    df= df.drop(columns= ['Age: Aged 4 years and under','Age: Aged 5 to 9 years','Age: Aged 10 to 14 years','Age: Aged 15 to 19 years','Age: Aged 20 to 24 years',\
                          'Age: Aged 25 to 29 years','Age: Aged 30 to 34 years','Age: Aged 35 to 39 years','Age: Aged 40 to 44 years','Age: Aged 45 to 49 years','Age: Aged 50 to 54 years','Age: Aged 55 to 59 years','Age: Aged 60 to 64 years',\
                            'Age: Aged 65 to 69 years','Age: Aged 70 to 74 years','Age: Aged 75 to 79 years','Age: Aged 80 to 84 years','Age: Aged 85 years and over'], axis=1)

    age_ftrs=['Age group 0-25','Age group 25-65','Age group 65+']

    # Deprivation
    df['Household is deprived in at least 1 dimension'] = df[['Household is deprived in one dimension',	'Household is deprived in two dimensions',	'Household is deprived in three dimensions','Household is deprived in four dimensions']].sum(axis=1)
    # drop non-grouped features 
    df= df.drop(columns= ['Household is deprived in one dimension',	'Household is deprived in two dimensions',	'Household is deprived in three dimensions','Household is deprived in four dimensions'], axis=1)
    deprivation_ftrs=['Household is not deprived in any dimension','Household is deprived in at least 1 dimension']
    # Economic activity				
    df['Unemployed_population'] = df[['Economic activity status: Economically active (excluding full-time students): Unemployed',\
                                          'Economic activity status: Economically active and a full-time student: Unemployed',]].sum(axis=1)
    
    df['Economically active'] = df[['Economic activity status: Economically active (excluding full-time students)',\
                                        'Economic activity status: Economically active and a full-time student']].sum(axis=1)
    
#   drop non-grouped features 
    df= df.drop(columns= ['Economic activity status: Economically active (excluding full-time students): Unemployed',\
                                          'Economic activity status: Economically active and a full-time student: Unemployed',\
                                            'Economic activity status: Economically active (excluding full-time students)',\
                                        'Economic activity status: Economically active and a full-time student'], axis=1)

    # Health 
    df['Population in Good Health'] = df[['Very good health','Good health','Fair health']].sum(axis=1)
    df['Population in Bad Health'] = df[['Bad health', 'Very bad health']].sum(axis=1)

    # drop non-grouped features 
    df= df.drop(columns= ['Very good health','Good health','Fair health', 'Very good health','Good health','Fair health', 'Bad health', 'Very bad health'], axis=1)
    

    # Ethnicity
    df['Mixed/Black/others'] = df[['Black, Black British, Black Welsh, Caribbean or African', 'Mixed or Multiple ethnic groups','Other ethnic group']].sum(axis=1)
    # drop non-grouped features 
    df= df.drop(columns= ['Black, Black British, Black Welsh, Caribbean or African', 'Mixed or Multiple ethnic groups','Other ethnic group'], axis=1)
    

    # Vehicles
    df['2 or more cars or vans in household'] = df[['Number of cars or vans: 2 cars or vans in household',	'Number of cars or vans: 3 or more cars or vans in household']].sum(axis=1)

    # drop non-grouped features 
    df= df.drop(columns= ['Number of cars or vans: 2 cars or vans in household',	'Number of cars or vans: 3 or more cars or vans in household'], axis=1)
    
    df['Population Density: Persons per square kilometre; measures: Value']= df['Population Density: Persons per square kilometre; measures: Value']
    return df

def get_prop(df, columns):
    """Gets proportion of features."""
    total = df[columns].sum(axis=1)
    print(total)
    df[columns]= df[columns].div(total, axis=0)
    print('done')
    return df[columns]

def save_static_data(df):
    """Saves dataframe to pickle file."""
    df.to_pickle(data_folder + 'static_data.pkl')

def merge_with_static(df):
    static= pd.read_pickle(data_folder + 'static_data.pkl')
    static= pd.merge(df, static, on='counter', how='inner')
    static.to_pickle(data_folder+'static_data.pkl')

def process_test_sites_data():
    df_sites = gpd.read_file(data_folder+'counter_locations/test_sites_counter_locations_processed.gpkg')
    df_sites= df_sites[['counter', 'geometry', 'provider', 'geom_type']].reset_index(drop=True)

    df_census= pd.read_pickle(data_folder+'census_oa_shapefiles.pkl')

    # Intersect sites with Output Areas
    df_sites_oa = intersect_sites_output_areas(df_sites, df_census)

    df_ur= pd.read_pickle(data_folder+'urban_rural_oa.pkl')

    # intersect updated census data with Census 2011 urban rural classification data
    df_sites_oa_ur= intersect_sites_output_areas(df_sites_oa, df_ur)

    # Add area column
    df_sites_oa_ur['area_sq_km'] = add_area_column(df_sites_oa_ur)

    # Save site info with raw census data
    df_sites_oa_ur.to_pickle(data_folder+'test_sites_raw_census_features_with_counter_info.pkl')

    df = df_sites_oa_ur
    
    
    # groups census features into larger and more relevant caetgories e.g. 3+ people in household
    grouped_census = engineer_features(df)
    
    # # Get proportion of features in each subset (e.g. proportion of 'Age group 0-25' in ['Age group 0-25','Age group 25-65'])
    for cols in ftrs_sbset:   
        grouped_census[cols]=get_proportion(grouped_census, cols)

    grouped_census= grouped_census.groupby('counter').mean(numeric_only=True).reset_index()
    # merge with counter info to get provider column for subsetting
    grouped_census= grouped_census.merge(df_sites[['counter', 'provider', 'geometry', 'geom_type']], on='counter')
    # save features as static training data. Other input features will be added to this static data set.
    grouped_census.to_pickle(data_folder + 'test_sites_static_data.pkl')




def main():

    # Load shapefiles
    df_shapefiles = load_shapefiles()  

    # Load urban/rural data
    df_urban_rural = load_urban_rural_data()

    # Merge urban/rural with shapefiles
    df_ur = merge_urban_rural_shapefiles(df_shapefiles, df_urban_rural)
    
    # Save urban/rural shapefiles
    save_data(df_ur, 'urban_rural_oa.pkl')

    # Load all census data
    df_census = load_census_data()

    # load 2021 shapefiles
    shape_2021= load_shapefiles_2021()

    # Merge census data with census 2021 shapefiles
    df_census = merge_census_ur(df_census, shape_2021)

    # Save census shapefiles and data
    save_data(df_census, 'census_oa_shapefiles.pkl')


    # merge census data with sites info
    # Load counter location data 
    df_sites = load_site_data()

    # Intersect sites with Output Areas Census 2021 data
    df_sites_oa = intersect_sites_output_areas(df_sites, df_census)

    # intersect updated census data with Census 2011 urban rural classification data
    df_sites_oa_ur= intersect_sites_output_areas(df_sites_oa, df_ur)
    
    # Add area column
    df_sites_oa_ur['area_sq_km'] = add_area_column(df_sites_oa_ur)

    # Save site info with raw census data
    df_sites_oa_ur.to_pickle(data_folder+'raw_census_features_with_counter_info.pkl')




    # process census data to features needed for model development
    df = df_sites_oa_ur
    
    
    # groups census features into larger and more relevant caetgories e.g. 3+ people in household
    grouped_census = engineer_features(df)
    
    # # Get proportion of features in each subset (e.g. proportion of 'Age group 0-25' in ['Age group 0-25','Age group 25-65'])
    for cols in ftrs_sbset:   
        grouped_census[cols]=get_proportion(grouped_census, cols)

    grouped_census= grouped_census.groupby('counter').mean(numeric_only=True).reset_index()
    # merge with counter info to get provider column for subsetting
    grouped_census= grouped_census.merge(df_sites[['counter', 'provider', 'geometry', 'geom_type']], on='counter')
    # save baseline features
    grouped_census.to_pickle(data_folder + 'census_features.pkl')
    # save features as static training data. Other input features will be added to this static data set.
    grouped_census.to_pickle(data_folder + 'static_data.pkl')


    # Get baseline features for regression 
    # baseline_features= [f for f in grouped_features if f in baseline_pop]
    # baseline_features.append('counter')
    baseline__features_df= grouped_census[baseline_pop]
    # merge with counter info to get provider column for subsetting
    # baseline__features_df= baseline__features_df.merge(df_sites[['counter', 'provider', 'geometry', 'geom_type']], on='counter')
    # save baseline features
    baseline__features_df.to_pickle(data_folder + 'baseline_features.pkl')

    # get features not included in baseline
    non_baseline_features = [f for f in grouped_features if f not in baseline_pop]
    non_baseline_features.append('counter')
    non_baseline_features_df= grouped_census[non_baseline_features]
    # merge with counter info to get provider column for subsetting
    non_baseline_features_df = non_baseline_features_df.merge(df_sites[['counter', 'provider', 'geometry', 'geom_type']], on='counter')
    # save features 
    non_baseline_features_df.to_pickle(data_folder + 'non_baseline_features.pkl')
    
if __name__ == "__main__":
    main()
  
  


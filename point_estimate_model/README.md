# Workflow 1 - Point estimate model of daily mean people count in each month of the year

This document explains how to execute the code in order to compile the input data set, train the model and generate predictions.
The data sets required and their structure will be outlined alongside step by step instructions on running the code. 

For detailed technical information relating the the modelling approach taken in this analysis please refer to our [technical report](https://datasciencecampus.ons.gov.uk/projects/a-data-science-approach-to-estimate-the-use-of-natural-spaces-a-feasibility-study/) 

# Input Data
## Census Data

All census features are downloaded fomr Census 2011 at the Output Area level from [Nomis](https://www.nomisweb.co.uk).

Features Required:

* Output Area shapefiles
* Urban-Rural classification
* Household occupancy
* Age by single year
* Households by deprivation dimensions
* Population density
* Working population
* General health
* Ethnic group
* Car or Van availability

## Accessible Green & Blue Infrastructure 

A series of geodatabases that contain a range of spatial datasets. These datasets describe the location and geographical extent of different types of Green and Blue Infrastructure across England. The datasets highlight accessibility levels, display greenspace provision and natural greenspace standards in a spatial context and present it alongside a wide range of social statistics. 
* [Green and Blue Infrastucture information](https://www.data.gov.uk/dataset/f335ab3a-f670-467f-bedd-80bdd8f1ace6/green-and-blue-infrastructure-england)
* [Green and Blue Infrstructure download link](https://s3.eu-west-1.amazonaws.com/data.defra.gov.uk/Natural_England/Access_Green_Infrastructure/Green_and_Blue_Infrastructure_NE/Green_and_Blue_Infrastructure_Opendata_NE_Geopackage.zip)

## Land Habitat Data

The habitat classification map  uses a machine learning approach to image classification, developed under the Defra Living Maps project (SD1705 – Kilcoyne et al., 2017). The method first clusters homogeneous areas of habitat into segments, then assigns each segment to a defined list of habitat classes using Random Forest (a machine learning algorithm). The habitat probability map displays modelled likely broad habitat classifications, trained on field surveys and earth observation data from 2021 as well as historic data layers. This map is an output from Phase IV of the Living England project, with future work in Phase V (2022-23) intending to standardise the methodology and Phase VI (2023-24) to implement the agreed standardised methods.
* [Landcover (Living England), Living England Habitat Map (Phase 4) | Natural England Open Data Geoportal](https://naturalengland-defra.opendata.arcgis.com/datasets/Defra::living-england-habitat-map-phase-4/about)

## People and Nature Survey Data
[The People and Nature Survey](https://www.gov.uk/government/collections/people-and-nature-survey-for-england) for England gathers evidence and trend data through an online survey relating to people’s enjoyment, access, understanding of and attitudes to the natural environment, and it’s contributions to wellbeing. Specifically, we will find mean dog ownership.
* [People and Nature Survey for England - Year 2 - Quarter 1 to Quarter 4 data](https://www.gov.uk/government/statistics/the-people-and-nature-survey-for-england-year-2-annual-report-data-and-publications-april-2021-march-2022-official-statistics-main-findings)

## Weather Data
Historical weather data for each individual people monitoring sites downlaoded using [Meteostat](https://meteostat.net/en/blog/obtain-weather-data-any-location-python) package.

## Counter Location Data 
A file containing the name, latitude and longitude of all people counters from each provider. Columns should be ‘counter’, ‘lat’, ‘lon’

## People Counter Data
A csv of people count data taken from automated sensors. Each column in the data set represents an individual people counter and each row represents a daily date. The values are the people counts for each day.

## Strava Data
Strava Metro data was access through the Strava Metro Dashboard. Applications to access Strava Metro can be completed [here](https://metro.strava.com). Strava Data is manually downloaded for the edge nearest to the location of each people counter.

# Data Folder Structure
The structure of the data folder is as follows. This folder structure is necessary to match the paths defined in modle_config.py. Any data sets required that do not have a specified folder should just be saved in the data folder

<pre>
data/
├── cenus/
├── counter_data/
├── counter_locations/
├── strava_data/<folder for each provider>
└── survey/
</pre>

# Compile Input Data Set

Firstly the data from each data souce needs to be collected for the area surrounding each people counter location.
The size of this area is called the buffer zone and is defined in model_config.py. The default size of the buffer zone is 5km.

In order to easily incoroporate new people counter locations into the code a config file is manually created, this config file 
contains infromation relating to people counters data from each people counter provider.
The information detailed is 
* provider name (this is used as the dictionary key e.g."ne" for Natural England)  
* "x-y-path" - the path to the location of the counter location data file (./data/counter_locations/\<counter location file>)  
* "pc_path" - the path to the location of the people counter data (./data/counter_data/\<people counter data file\>)  
* "strava_path" - the path to the location of strava data for each people counter (./data/strava_data/\<folder for each provider>/\<folder for each edge>/\<strava data files>)
* "cut_off_year" - the earliest year that we have people counter data for.

![Config file ](https://github.com/datasciencecampus/nature_engagement_phase2/blob/main/Screenshot%202024-03-15%20at%2015.09.34.png)

By opening and running the code chunks contained in "compile_input_data.ipynb" the information given in the config file 
ingested and then each of the "add_data source name.py" scripts are called to retrieve the data relevant to people counters
and create the input data set required for the model. The output of the "compile_input_data.ipynb" notebook is a pickle file called 
"static_and_dynamic_features_\<buffer zone size>.pkl" where the buffer zone size used when collecting data is input into the filename. 

# Model Training
By running each code chunk in  "model_training.ipynb"  the output data set from "compile_input_data.ipynb" is used to train the 
ensemble regression model developed in phase one of this project. The outputs from this notebook are saved in the data folder and are as follows:
* training_predictions.pkl - data set containing input data and predictions of daily mean for each month of the year  for each people counter location in the training data set 
* test_predictions.pkl - data set containing input data and predictions of daily mean for each month of the year  for each people counter location in the test data set
* voting_regressor_model.pkl - saved model after training.

The notebook uses the Pycaret Python package to train an ensemble regressor model that uses the predictions of five different regression models. 

### Train Test Split
The model training notebook also details the approach for splitting input data into training and test data sets in the training_test_split function. This is done first by carrying out K-Means clustering on the coordinates of each people counter to assign a cluster label to each counter location. This cluster label is then used to stratify the division of data when the data is split into training and testing data sets. This is done to ensure that the distribution of the locations of people counters is preserved in both training and test data sets. The function also provides an alternative option for the stratification of data splitting using the land_type lables assigned when compiling the input data, howevere during testing this had a negative impact on model performance.

### Feature Selection
Also included in the model_training notebook is a function to select the final features to include in the model, this is done using Variance Inflation Factor(VIF). VIF is used to remove features with signigicant collinearity from the model. If not removed this multicollinearity can have negative impacts on model performance and interpretation. The VIF function in the notebook carries out VIF and sequentially removes the feature with the highest VIF score untill all features have a VIF score of less than 10 (lowe VIF score indicates less multicollinearity).

# Generating predictions for locations without people counter data 
The model can also be used to create predictions for locations that we do not have people counter data for. A slight variation of the workflow must be used in this scenario due to the lack of people counter data. This process utilises the functions definied in the add_scripts and used to compile the input data set for the model along with a new config.json file relating to the new locations without people counter data.  

1. Create  new  location file containing x, y coordinates of points of interest. Retrieve  Strava Metro data from the edge closest to each point.
2. Create a new config.json file that contains the information outlined above but does not contain the "pc_path" variable.
3. Run the "compile_input_data_for_test_sites.ipynb". This will create the dataset to be used as the input for the model to make predictions.
4. Run the "generate_predictions_for_test_sites.ipynb" This uses the data set created and generates a dataframe containing model predictions.

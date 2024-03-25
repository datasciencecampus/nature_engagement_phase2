# Workflow 2- Area Predictions for Protected Landscapes
This worfklow details the steps needed to make predictions for larger geographic areas as opposed to the point 
estimates outlined in Workflow 1. The worfklow comprises of:

1. Identifying areas of overlap between the protected landscapes and the location of people counters
2. Clustering the protected landscapes based on socio-demographic features, 
3. Train a regression model using a multigroup approach i.e. one model for each cluster. The model relates the data from people counters to the strava activity count of edges closest to the people counters in that cluster. 
5. For each cluster we then identify the polygon containing a people counter location and all other conected polygons from the same cluster.
6. Collect Strava Data for edges within connected polygons.
7. Use Regression model created in step three to predict

# Input Data

## static_and_dynamic_features_<\buffer_zone>.pkl, the output from 'point_estimate_model/compile_input_data.ipynb'
This data set is used to select people counters that have passed data quality assessment during the process to compile the input data for the point estimate model. This provides the location of the people counters and  the people counter data.  

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

## Strava Data
Strava Metro data was access through the Strava Metro Dashboard. Applications to access Strava Metro can be completed [here](https://metro.strava.com). Strava Data is manually downloaded for the edge nearest to the location of each people counter and also all edges present in the polygons identified in step five.

## Protected Landscape Shapefiles
Shapefiles that provide the location of the protected landscapes. 

# Data Folder Structure
The structure of the data folder is as follows. This folder structure is necessary to match the paths defined in modle_config.py. Any data sets required that do not have a specified folder should just be saved in the data folder
<pre>
data/
├── AONB/
├── NE_NationalrksEngland_SHP-Full/
├── regions/
└──strava_data/<\data for each edge 
</pre>

# Workflow 2- Area Predictions for Protected Landscapes
This worfklow details the steps needed to make predictions for larger geographic areas as opposed to the point 
estimates outlined in Workflow 1. The worfklow comprises of:

1. Clustering the protected landscapes based on socio-demographic features, 
2. identifying areas of overlap between the protected landscapes and the location of people counters,
3. training a regression model using a multigroup approach for each cluster identified. The model relates the data
   from people counters to the strava activity count of edges within the cluster. 
5. For each cluster we then identify the polygon containing a people counter location and all other conected
   polygons from the same cluster and use the regression model created in step three to make predictions.

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

## People Counter Data
x,y locations of people counters 
## Strava Data
Strava Metro data was access through the Strava Metro Dashboard. Applications to access Strava Metro can be completed [here](https://metro.strava.com). Strava Data is manually downloaded for the edge nearest to the location of each people counter.

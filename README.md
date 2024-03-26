# Measuring Engagement with Nature

Estimating use of natural spaces based on People Counter data, Strava Metro data, Census data, weather data, Open Street Map data, Green Infrstructure data
________________________________________________________________
The goal of this project is to measure people's engagement with the natural environment. This information supports understanding of progress against Defra’s Environmental Improvement Plan 2023 which sets out key targets and commitments on access and engagement with nature, including a commitment that everyone should live within 15 minutes’ walk of a green or blue space.

Automated people counters are used frequently to monitor pedestrian and cycling activity with a good temporal resolution. However, people counters are expensive to install and maintain and for this reason are only installed in a few strategic locations. 

Introducing an inexpensive and widely applicable data science method for monitoring visitor numbers would considerably enhance Defra’s indicator for tracking nature engagement. This model combines aggregated and anonymised data from Strava Metro with carefully selected open or free-to-access spatial datasets such as automated people counters and indicators of local environmental and social conditions. These results are experimental, in order to produce more robust results to inform outcomes we need to incorporate a larger set of training data and datasets that cover the residential location of visitors. 

A brief introduction to the methodology used and interpretation of results can be found in [this blog post](https://datasciencecampus.ons.gov.uk/using-open-source-data-to-measure-our-engagement-with-the-natural-environment/) and for a more detailed look at this project please read our [technical report](https://datasciencecampus.ons.gov.uk/projects/a-data-science-approach-to-estimate-the-use-of-natural-spaces-a-feasibility-study/) 

This repository reflects work completed in the second phase of this project. In this phase of the project we have adapted the coding pipeline to be more efficient, more user-friendly and also accommodate new sources of people counter data more easily. This improved pipeline is documented in nature_engagement_phase2/point_estimate_model. We have also provided two new methods of analysis, the first focused on a clustering approach to provide larger area estimates to compliment the outputs of the point estimate model and the second focussed on optimising the placement of people counters using similarity analysis of Strava Metro data.


## Usage
_________________________________________________________________

Three analytical workflows are outlined in this repository:

1. Point Estimate Model- This outlines our approach to compiling relevant input data such as weather, points of interest and socio-demographic features from the areas around people counter locations and using this data in conjunction with activity counts taken from Strava Metro to train an ensemble regression model capable of estimating the daily mean people count for each month at each counter location. The data set created in 'compile_input_data.ipynb' is used also as an input data set for workflow two.
2. Area Predictions for Protected Landscapes- This analysis detail an approach to predicting daily mean people count for each month for larger areas. Using the people counter data and socio-demographic data complied in the point estimate model data set protected landscapes are decomposed into separate clusters. A regression model is then trained based on the people counter data and strava data present in each cluster. These models are then used to predict the daily mean people count for each month for larger areas surrounding each people counter location.
3. Optimised Counter Placement- Combining time series similarity analaysis with clustering to categorise streets based on the pattern of their Strava activity. Once clusters have been identified optimal placement of counters can be determined to best represent the distirbution of strava activity in the area.

More detailed documentation is provided in the relevant subfolder for each analysis.     


## Credits
_________________________________________________________________

This project was generated from a collaboration with [The Department for Environment, Food and Rural Affairs](https://www.gov.uk/government/organisations/department-for-environment-food-rural-affairs) and [The Data Science Campus](https://datasciencecampus.ons.gov.uk/) at [The Office for National Statistics](https://www.ons.gov.uk/), [Strava Metro](https://metro.strava.com), [Natural England](https://www.gov.uk/government/organisations/natural-england) and The North Downs Way 

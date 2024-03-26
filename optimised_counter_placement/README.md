# Workflow 3- Optimise Placement for People Counters 
In this worrkflow, we use clustering techniques to categorize street segments into classes of temporal 
patterns of Strava activities. We used continuous signal processing to group sample of street segments 
in National Parks across England into distinct classes of temporal activities that varied based on 
overall volume and daily patterns. Findings from this work can use this data to strategically place 
counters across these trails to efficiently capture visitation counts that better represent the 
visitation counts in protected landscapes.

1. Gather Strava Metro Data for trails in relevant areas
2. Separate Strava data into each season and take the mean number of acrivities per month for each edge. 
3. Use Dynamic Time Warping (DTW) to compare the data fro each edge and create a similarity matrix of all edges.
4. Use Agglomerative Clustering to assign each edge to a cluster based on the similarity matrix created in step four.
6. Based on this clustering a heatmap of activity for the selected Strava edges is produced. This can then
   be used to determine people counter placement that represents the distirubtion of activity in each area.
   The analysis is carried out in 'identify_busy_trails_national_park.ipynb'.

# Input Data
## Strava Data
[Strava Metro](https://metro.strava.com) Data for edges that are present in the areas of interest. 
## National Park Shapefiles
Shapefiles that provide the location of the National Parks. 

# Data Folder Structure
The structure of the data folder is as follows. This folder structure is necessary to match the paths defined in modle_config.py. Any data sets required that do not have a specified folder should just be saved in the data folder
<pre>
data/
├── NE_NationalNatureReservesEngland_SHP_Full/
├── NE_NationalrksEngland_SHP-Full/
└──strava_data/
  └── national_park_data/
    ├── national_park_1
    ├── national_park_2
    ├── national_park_3
    ├── national_park_4
    ├── national_park_5
    ├── national_park_6
    ├── national_park_7
    ├── national_park_8
    ├── national_park_9
    └──national_park_10
</pre>

# Requirements File
A requirements text file is provided to allow easy recreation of the environtment used for this analysis.

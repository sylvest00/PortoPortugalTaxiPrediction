# Final Project: Predicting Trip Times & Final Destinations of Taxi Trips in Porto, Portugal
## General Assembly Part-Time Data Science Course
## Completed November 5, 2016

### Overview
This project is based off of two Kaggle competitions ([I](https://www.kaggle.com/c/pkdd-15-predict-taxi-service-trajectory-i) and [II](https://www.kaggle.com/c/pkdd-15-taxi-trip-time-prediction-ii/data)) from 2015 that were posted by ECML PKDD* and completed by conference attendees.

The competition was a demonstration on how to make electronic dispatching systems more efficient by predicting the earliest time in which a driver can accept a new passenger based upon the location of the final destination and a prediction on how long the trip should take.

The Kaggle/ conference competitions had two immediate aims:
1. Predict the final destination of a taxi ride in Porto, Portugal based upon a partial trajectory of the beginning of the ride.
2. Predict the duration of the ride.

*ECML PKDD = European Conference on Machine Learning and Principles and Practice of Knowledge Discovery in Databases


### Final Project Objectives
For my final project, I chose to predict the final destination and trip time of a randomly selected partial trajectory (trip #40).

#### The Data
### Datasets
This Kaggle challenge came with 3 data sets- a test set (321 hypothetical observations), a training set (1710671 observations), and a CSV file that contains the name and latitude and longitude of taxi stands that are included in the data set.

The training and test sets include the following variables:

| Variable | Data Type | Description
---|---|---|
TRIP_ID | ID | Identifier for each trip
CALL_TYPE | Categorical | Mode of call A (dispatched), B (stand), C(street)
ORIGIN_CALL| ID | ID for each phone number used to demand service if CALL_TYPE==A
ORIGIN_STAND| ID | Taxi stand ID
TAXI_ID| ID | Taxi ID
TIMESTAMP| Continuous | Unix time stamp of trip's start
DAYTYPE| Categorical | Type of day B (holiday), C(day before B), A (all other days)
MISSING_DATA | Boolean | False when GPS data is complete, True otherwise
POLYLINE | Continuous | Coordinates of trip recorded every 15 seconds.

To simplify this project, I chose to predict the trip distance and time of one test trip. Also, I only worked with data from the same month and day of the week as the test trip. With more computing power, the entire data set will be used at a later date.

#### Procedure
I began by finding trajectories in the training set that had at least 1 point within a 0.1 radius of the last recorded point of partial test trajectory #40. To further select similar trajctories, I used dynamic time warping to identify trajectories that were the most similar to the partial trajectory. The difference between the point nearest the last point in the partial trajectory and the starting point of trips in the training set revealed additional clusters. I used kMeans clustering to further select clusters of trips that were the most similar to the test trip. I then used the distance traveled and total trip times of trajectories that shared the same cluster as the test data as inputs for decision tree and random forest regression.

#### Results
I found that, by comparing the mean squared error (MSE), regression analysis performed better when I used dynamic time warping alone instead of dynamic time warping and kMeans to better select inputs for my predictive models.

In summary, test trip #40 likely was around 2.23 miles (MSE = 0.41) and lasted around 5.5 minutes (MSE = 0.4).
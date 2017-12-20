# TrackAPI

# Features
1. REST APIs to be able to post the locations, get the data for a specific user, and get for the user to get his own data.
2. POST Request Object might be single location track.
3. Get API should be able to take date range (and particular user for admin) and give the route(as a list of locations), distance covered in that time frame.
4. If date range is not given API has to return the last known location, distance covered and route for that day.


## Setting up project
#### Run the setup shell script
```
    ./setup.sh
```

OR

* System Dependencies : geo django 
Uses django.contrib.gis.db.backends.spatialite as DB backend engine
* platform specific packages can be downloaded from https://docs.djangoproject.com/en/2.0/ref/contrib/gis/


```
    virtualenv env_tracker
    source env_tracker/bin/activate
    pip install -r reuqirements.txt
    ./manage.py migrate
    ./manage.py runserver 7001
    ./manage.py createsuperuser
```
 

## API endpoint for Tracks

```
http://localhost:7001/api/tracks/
```


## GET API
- Retruns track (list of locations) covered by users along with distance covered by user during that time span.
- If no date range is supplied we return data of today only


### Date range based filters

```

http://localhost:7001/api/tweets/?created_at__start=2017-12-19T07:10:00Z

http://localhost:7001/api/tweets/?created_at__end=2017-12-19T07:10:00Z

http://localhost:7001/api/tweets/?created_at__start=2017-12-19T07:10:00Z&created_at__end=2017-12-19T07:10:00Z
```

### User based filtering

* By default it returns all tracks data.
* if we supply user id as 'user' query param it returns data for that particular user only
    ```http://localhost:7001/api/tracks/?user=1```


## POST API 

params
    - user : Id of user
    - location : comma seperated lat long co ordinates of location (14.232, 15.233)

returns
201 : when successfully created


[![Maintainability](https://api.codeclimate.com/v1/badges/89fe2c715447b3929eab/maintainability)](https://codeclimate.com/github/Lambda-School-Labs/earth-dashboard-ds/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/89fe2c715447b3929eab/test_coverage)](https://codeclimate.com/github/Lambda-School-Labs/earth-dashboard-ds/test_coverage)

# PlanetData.World


<b><p align="left">A <a href="https://planetdata.world">website</a> that teaches middle school students about the Earth and data visualization via interactive lessons.</p></b>


## DS Contributors

|Charles Vanchieri|Serina Grill|Sean Hobin|      
| :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: |
|                      [<img src="https://github.com/CVanchieri/CVanchieri.github.io/blob/master/img/GeneralPortfolio/CVProfile2.jpg?raw=true" width = "200" />](https://github.com/CVanchieri)                       |                      [<img src="https://avatars1.githubusercontent.com/u/42048900?s=460&u=bc21df438fd5dad8ab1e15b57aaba82c6ff45856&v=4" width = "200" />](https://github.com/)                       |                      [<img src="https://abstractmonkey.github.io/img/avatar.jpg" width = "200" />](https://github.com/)                       |   
|                 [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/cvanchieri)                 |            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/serinamarie)             |           [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/AbstractMonkey)            |    
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/cvanchieri6/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/serinamarie) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/) |

![MIT](https://img.shields.io/packagist/l/doctrine/orm.svg)
![Python](https://img.shields.io/static/v1?label=Py&message=Python3.7&color=Blue)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

## Project Overview

- [Website](https://planetdata.world)

- [Product Vision Document](
https://www.notion.so/PlanetData-World-previously-Earth-Dashboard-f2164d30ed994ecab5894212efcc2000)

- [Product Release Canvas](https://www.notion.so/8bd1fb80a11447f9b3a2a4572bda7a33?v=bc7e5838ad224b978d81fc5946c29650)

- [Trello Board](https://trello.com/b/5gHETvxv/earth-dashboard)

## Project Repositories
- [Front-End](https://github.com/Lambda-School-Labs/earth-dashboard-fe)

- [Data Science](https://github.com/Lambda-School-Labs/earth-dashboard-ds)

##

## Tech Stack

Visualizations: **Plotly**, **D3**, **Mapbox**, **Seaborn**, **Matplotlib**

Services: **AWS**, **Docker**, **Jupyter Notebooks**, **Postman**

Languages: **Python**

Backend: **AWS API Gateway**, **AWS Lambda**, **AWS RDS PostgreSQL**, **Flask**, **SQLAlchemy**, **Heroku**, **AWS CloudWatch**

Predictive Modeling: **Facebook Prophet**, **Random Forest Regressor**

# Getting Started

## A note before you begin: 

This application is primarily serverless. [9 packaged functions](https://github.com/Lambda-School-Labs/earth-dashboard-ds/tree/master/AWSLambda) (AWS Lambda) are located on AWS:

* 7 functions are accessible via AWS API Gateway. These [endpoints](#aws-api-gateway-endpoints) return a json string — data that has been formatted, filtered, and wrangled by the DS team (and in cases of dynamic data, placed into the PostgreSQL database). 

* 2 functions, however, update existing tables in the database with new data from various [external API data sources](https://documenter.getpostman.com/view/10808728/SzS8rjbc?version=latest). Each day a CloudWatch rule triggers the 2 functions to parse the data from the external APIs, updating the [summary](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/AWSLambda/summary_db_add/lambda_function.py) and [covidall](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/AWSLambda/covidall_db_add/lambda_function.py) tables to get today’s data into the AWS RDS PostgreSQL. As the [heatmap](https://www.planetdata.world/Pandemic/racing) and [bubbles](https://www.planetdata.world/Pandemic/bubbles) visualizations rely on these tables, so too do the visualizations which update in order to show relevant data. This is all the result of these self-sufficient functions. Side note: You’ll notice a third table exists in the database (uscounties); this was originally meant to be a dynamic table but it proved too much for both Lambda functions and Heroku. 

Why is there a Flask app, then, you ask, if this is all serverless? Why am I necessary?

* There are [2 endpoints](#heroku-endpoints) which could not be made serverless (but go ahead and try with other cloud services such as Google Cloud functions, for example). These exist in the Flask app, deployed to Heroku. The first endpoint simply returns the data from the uscounties table in the database for web to visualize the [heatmap](planetdata.world/pandemic/heatmap). 

* The second endpoint exists only to be requested by a Lambda function, which in turn is each day triggered by a CloudWatch rule. Why can’t the Lambda function package just call directly to the external API so that we don’t need a Flask API endpoint? Well, Lambda functions are meant to be small and singly-tasked and the [external API](https://api.covid19api.com/country/us/status/confirmed/live) used for the [visualization](planetdata.world/pandemic/heatmap) returns too large a payload for the Lambda function to accept (and is difficult to filter by date). As all 380,000~ data points are necessary to display this visualization properly, things got tricky and ultimately we realized that static data would better capture the dramatic and exponential first 4 months of the COVID-19 pandemic.

## Prerequisites

    * Flask (preferred: Flask-SQLAlchemy, Flask-RestPlus, Flask-Marshmallow)
    * SQL, especially for PostgreSQL
    * Knowledge of how to run an application locally
    * Heroku or another web server (if part of the build-on for this project)

## Installing 

Go ahead and clone this repository into the directory of your choosing. You'll need to put the [Heroku Environment Variables](#heroku-environment-variables) into a .env file in your base directory. 

To start up the app locally, navigate to the FLASK directory via the CLI and type

    flask run

When viewing in your browser, it should result in this:

![Image of Swagger API](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/Images/swagger_API.png)

Otherwise you may not have the right environment variables.

## Running tests

As only 2 endpoints exist for the Flask API, only a few tests exist for this application. This area should be more robust in a later build.

To run, navigate to the application directory of the repository and type:

    pytest test.py
    
Or from the FLASK directory of the repository you may type:
    
    python -m application.test 

These tests simply check the [external APIs](https://documenter.getpostman.com/view/10808728/SzS8rjbc?version=latest) from which they request a response.

## Deployment to Heroku

Create a new app on [Heroku](https://dashboard.heroku.com/apps). Next, deployment of an application will require creating a special type of git remote called a Heroku remote (a Heroku-hosted remote). You can set this up in your remote repository on github by first logging in to heroku with 
    
    heroku login

Once you have logged in, type
    
    heroku git:remote -a whatever_you_named_your_app

As the app cannot be run from the root directory of the repository, one MUST use
    
    git subtree push --prefix FLASK heroku master
    
in order to let Heroku know where the application is, as it will be looking for the Pipfile. If you renamed your Heroku remote to something besides 'heroku,' replace 'heroku' in the command above with whatever you renamed it.

## Data Sources

### Landing Page Globe
- [Carbon Footprint](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/CarbonFootprint.ipynb)
- [Charles' Pollution Data](placeholder)

### COVID-19
- [COVID-19 Heatmap](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/COVID19API_DataVis2_CV.ipynb)
- [COVID-19 Race Chart](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/COVID19API_DataVis4_CV.ipynb)
- [COVID-19 Bubbles Plot](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/FLASK_RC1.2/application/templates/bubbles.html)
- [COVID-19 Air Pollution Line Graph](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/Air_Pollution_During_Quarantine.ipynb)

### Deforestation
- [Deforestation Data](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/DeforestationDataWrangle_RC2_CV.ipynb)
- [Deforestation Model](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/DeforestationPredictionModel_RC2_CV.ipynb)
- [Deforestation Line & Bar Graph](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/DeforestationDataVis_RC2_CV.ipynb)

### Wildlife
- [Migratory Bird Patterns Data](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/Static/birds.csv)
- [Migratory Bird Patterns Ridgeplot](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/Migratory_Bird_Patterns.ipynb)
- [Symbiosis Data](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/Static/symbiosis.csv)

### Global Warming
- [CO<sub>2</sub> in the Atmosphere](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/mol_fraction_co2.ipynb)
- [Aggregated Climate Data](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/aggregated_climate_data.ipynb)


##

# API Documentation

### Architecture
<img src="https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/Images/DSArchitecture.png" width = "600" />

#### Backend deployed serverlessly through AWS API Gateway and AWS Lambda, with two endpoints existing on a [Heroku](https://ds-backend-planetdata.herokuapp.com/) server.<br>

## AWS API Gateway Endpoints

### COVID-19 Global Cases Bubbles Visualization Data (AWS API Gateway and AWS Lambda)

#### URL

https://4eo1w5jvy0.execute-api.us-east-1.amazonaws.com/default/summary_db_query

#### Description

Returns the name and total confirmed cases for each country.

#### Schema

```typescript
{
	"country": string,
	"totalConfirmed": number
}
```
### COVID-19 Global Cases Bubbles Visualization - Refresh Data (AWS Lambda and AWS Cloudwatch)

#### URL

https://4eo1w5jvy0.execute-api.us-east-1.amazonaws.com/default/summary_db_add

#### Description

Pulls data from covid/summary API and inserts it into the AWS RDS PostgreSQL. Triggered once a day by a AWS CloudWatch rule.

### COVID-19 Global Fatalities Racing Chart Data (AWS API Gateway and AWS Lambda)

#### URL

https://4eo1w5jvy0.execute-api.us-east-1.amazonaws.com/default/covidall_db_query

#### Description

Returns the country, date, and cumulative number of deaths from COVID-19.

#### Schema

```typescript
{
	"country": string,
	"date": string ("yyyy/MM/dd"),
	"deaths": number
}
```

### Air Quality Line Graph Data (AWS API Gateway and AWS Lambda)

#### URL

https://4eo1w5jvy0.execute-api.us-east-1.amazonaws.com/default/airquality_query

#### Description

Returns a set of all dates, the date and daily dean PM2.5 concentration for each day, and the date and number of cases for each day. Data is only used for dates shared between both the cases and air quality data.

#### Schema

```typescript
{
	"dates": string ("M/d/yyyy")[],
	"airQuality": {
		"x": string ("M/d/yyyy"),
		"y": number
		}[],
	"cases": {
		"x": string ("M/d/yyyy"),
		"y": number
		}[]
}
```

### Deforestation Prediction Trends Line Graph Data (AWS API Gateway and AWS Lambda)

#### URL

 https://4eo1w5jvy0.execute-api.us-east-1.amazonaws.com/default/deforestation_function

#### Description

Returns the country code, year, agricultural land in sq. km, electrical power consumption, GDP per capita growth, livestock production index, number of ores and metals exports, urban population, crop production index, food production index and forest area percentage for each country.

#### Schema

```typescript
{
	"Country Name": string, 
  	"Country Code": string, 
  	"Year": number, 
  	"Agricultural land (sq. km)": number, 
  	"Electric power consumption (kWh per capita)": number, 
  	"GDP per capita growth (annual %)": number, 
 	"Livestock production index (2004-2006 = 100)": number, 
  	"Ores and metals exports (% of merchandise exports)": number, 
 	"Urban population": number, 
  	"Crop production index (2004-2006 = 100)": number, 
  	"Food production index (2004-2006 = 100)": number, 
  	"Forest area (% of land area)": number
}
```

### Globe - Carbon Footprint Data (AWS API Gateway and AWS Lambda)

#### URL

https://4eo1w5jvy0.execute-api.us-east-1.amazonaws.com/default/globe_footprint

#### Description

Returns the name, latitude, longitude, and carbon footprint of the city.

#### Schema

```typescript
[
	[city name, lat, lon, magnitude, city name, lat, lon, magnitude, city name, lat, lon, magnitude.. ]
]
```

### Bird Migration Ridgeplot Data (AWS API Gateway and AWS Lambda)

#### URL

https://4eo1w5jvy0.execute-api.us-east-1.amazonaws.com/default/migration_density

#### Description

Returns the number of bird sightings for that species in 1970, 1975, 1981, 1985, 1990, 1998, 2004, 2011, and 2015.

#### Schema

```typescript
{
	"1970": number, 
	"1975": number, 
	"1981": number, 
	"1985": number, 
	"1990": number, 
	"1998": number, 
	"2004": number, 
	"2011": number, 
	"2015": number
}
```

### AWS Environment Variables
In order to re-create the [AWS Lambda functions](https://github.com/Lambda-School-Labs/earth-dashboard-ds/tree/master/AWSLambda) correctly, the user must set up their own environment variables in each AWS Lambda function. 

```
RDS_HOST = database url 
RDS_USERNAME = username 
RDS_USER_PWD = password
```

In addition, create a Dockerfile based on the Amazon Linux image to create the correct Python environment (we used 3.7). Refer to [this article](https://medium.com/@niklongstone/how-to-build-an-aws-lambda-function-with-python-3-7-the-right-way-21888e2edbe8) for help if need be.

## Heroku Endpoints

### COVID-19 US Cases Heatmap Data

#### URL

https://ds-backend-planetdata.herokuapp.com/covid/uscounties/query

#### Description

Returns the latitude, longitude, number of confirmed cases, and date for each day and a set of all dates.

#### Schema

```typescript
{
	"cases": {
		"lat": number,
		"lon": number,
		"cases": number,
		"date": string ("MM/dd/yy")
		},
	"dates": string ("MM/dd/yy")
}
```
### COVID-19 Global Fatalities Racing Chart - Refresh Data (Heroku, AWS Lambda and AWS Cloudwatch)

#### URL

https://ds-backend-planetdata.herokuapp.com//covid/covidall/add

#### Description

Pulls data from covid/all API and inserts it into the AWS RDS PostgreSQL. Triggered once a day by a AWS CloudWatch rule. No endpoint provided so as to not to create duplicate records in the database. Can take up to 20 mins locally.


### Heroku Environment Variables
In order for the Flask app to function correctly, the user must set up their own environment variables.

create a .env file that includes the following:

```
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://username:password@databaseurl'
TESTING=True
DEBUG=True
SECRETKEY= secret key
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO=True
FLASK_APP=application.py
FLASK_ENV=development
```


## Initial Database Migration

You can quickly add a new table to the database and insert a large amount of data via Jupyter notebook in Colab.
[Data Migration Notebook](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/Web_API_to_DB_Migration.ipynb)

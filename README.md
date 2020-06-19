[![Maintainability](https://api.codeclimate.com/v1/badges/89fe2c715447b3929eab/maintainability)](https://codeclimate.com/github/Lambda-School-Labs/earth-dashboard-ds/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/89fe2c715447b3929eab/test_coverage)](https://codeclimate.com/github/Lambda-School-Labs/earth-dashboard-ds/test_coverage)

# PlanetData.World


<b><p align="left">A <a href="https://planetdata.world">website</a> that teaches middle school students about the Earth and data visualization via interactive lessons.</p></b>


## DS Contributors:

|Charles Vanchieri|Serina Grill|Sean Hobin|      
| :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: |
|                      [<img src="https://github.com/CVanchieri/CVanchieri.github.io/blob/master/img/GeneralPortfolio/CVProfile2.jpg?raw=true" width = "200" />](https://github.com/CVanchieri)                       |                      [<img src="https://avatars1.githubusercontent.com/u/42048900?s=460&u=bc21df438fd5dad8ab1e15b57aaba82c6ff45856&v=4" width = "200" />](https://github.com/)                       |                      [<img src="https://abstractmonkey.github.io/img/avatar.jpg" width = "200" />](https://github.com/)                       |   
|                 [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/cvanchieri)                 |            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/serinamarie)             |           [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/AbstractMonkey)            |    
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/cvanchieri6/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/serinamarie) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/) |

![MIT](https://img.shields.io/packagist/l/doctrine/orm.svg)
![Python](https://img.shields.io/static/v1?label=Py&message=Python3.7&color=Blue)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

## Project Overview:

- [Website](https://planetdata.world)

- [Product Vision Document](
https://www.notion.so/PlanetData-World-previously-Earth-Dashboard-f2164d30ed994ecab5894212efcc2000)

- [Product Release Canvas](https://www.notion.so/8bd1fb80a11447f9b3a2a4572bda7a33?v=bc7e5838ad224b978d81fc5946c29650)

- [Trello Board](https://trello.com/b/5gHETvxv/earth-dashboard)

## Project Repos:
- [Front-End](https://github.com/Lambda-School-Labs/earth-dashboard-fe)

- [Data Science](https://github.com/Lambda-School-Labs/earth-dashboard-ds)

##

## Tech Stack:

Visualizations: **Python**, **Plotly**, **D3**, **Mapbox**, **Seaborn**, **Matplotlib**

Backend: **AWS API Gateway**, **AWS Lambda**, **AWS RDS PostgreSQL**, **Flask**, **Heroku**, **AWS CloudWatch**

Predictive Modeling: **Facebook Prophet**, **Random Forest Regressor**

##

## Data Sources:

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

## Initial Database Migration
- [Data Migration](https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/Web_API_to_DB_Migration.ipynb)

##

# API Documentation

### Architecture
<img src="https://github.com/Lambda-School-Labs/earth-dashboard-ds/blob/master/Notebooks/Images/DSArchitecture.png" width = "600" />

#### Backend deployed serverlessly through AWS API Gateway and AWS Lambda, with a single endpoint existing on a [Heroku](https://ds-backend-planetdata.herokuapp.com/) server.<br>

## AWS API Gateway Endpoints

### COVID-19 Bubbles Visualization

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
### COVID-19 Bubbles - Refresh Data

#### URL

https://4eo1w5jvy0.execute-api.us-east-1.amazonaws.com/default/summary_db_add

#### Description

Pulls data from covid/summary API and inserts it into the AWS RDS PostgreSQL. Triggered once a day by a AWS CloudWatch rule.

### COVID-19 Racing Chart

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

### Air Quality Line Graph

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

### Deforestation Prediction Trends

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
  	"GDP per capita growth (annual %)": -3.8741031654, 
 	"Livestock production index (2004-2006 = 100)": number, 
  	"Ores and metals exports (% of merchandise exports)": number, 
 	"Urban population": number, 
  	"Crop production index (2004-2006 = 100)": number, 
  	"Food production index (2004-2006 = 100)": number, 
  	"Forest area (% of land area)": number
}
```

### Globe - Carbon Footprint

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

### Bird Migration - Ridgeplot (Density Plot)

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

### Environment Variables
In order to create AWS Lambda functions correctly, the user must set up their own environment variables in each AWS Lambda function.

```
RDS_HOST = database url 
RDS_USERNAME = username 
RDS_USER_PWD = password
```

## Heroku Endpoint

### COVID-19 Heatmap

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

### Environment Variables
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

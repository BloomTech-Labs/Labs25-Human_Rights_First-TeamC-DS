# Human Rights Considered - Data Science Backend
<p align="center">
<img src="https://raw.githubusercontent.com/Lambda-School-Labs/Labs25-Human_Rights_First-TeamC-FE/main/src/assets/HRC.png" width = "475">
</p>

## [Human Rights First](https://www.humanrightsfirst.org/)

> Human Rights First is a 501(c)(3) international independent advocacy and action organization that challenges America to live up to its ideals. We believe American leadership is essential in the global struggle for human rights, so we press the U.S. government and private companies to respect human rights and the rule of law. When they fail, we step in to demand reform, accountability and justice. Around the world, we work where we can best harness American influence to secure core freedoms.

Human Rights Considered is a project working to track incidents of police use of force on Americans for Human Rights First. Our initial goal was to develop a visualization that showcases instances of police use of force along with a data science model that helps classify possible instances of brutality. We quickly realized that our highest-priority data science task -in addition to creating a model to assess use of force- was to source and process the relevant data, create a database, and to host it in an accessible API. 

**Disclaimer: This application is currently in Alpha (as of Sep 20, 2020) and is not ready for production. Please use at your own risk.**


## DS Contributors

|Axel Corro|Michelle Hottinger|Miriam Ali|      
| :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: |
|                      [<img src="https://avatars3.githubusercontent.com/u/17439087?s=460&u=f9cdb3a55e942143c590bd572d27f935aa1d555b&v=4" width = "200" />](https://github.com/axefx)                       |                      [<img src="https://media-exp1.licdn.com/dms/image/C5603AQFZFcQ5fTtWHw/profile-displayphoto-shrink_800_800/0?e=1606348800&v=beta&t=9GNJecdRaFkpwpSY04k3eU-RCu1Jr_gGjTof_5LUUw4" width = "200" />](https://github.com/michhottinger)                       |                      [<img src="https://avatars1.githubusercontent.com/u/60833374?s=460&u=8cfd7af0db714de6413c97af92f030f41c468b1e&v=4" width = "200" />](https://https://github.com/maiali13/)                       |   
|                 [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/axefx)                 |            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/michhottinger)             |           [<img src="https://github.com/favicon.ico" width="15"> ](https://https://github.com/maiali13/)            |    
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/axel-corro/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/michellehottinger/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/miriam-ali/) |

This project's front end repository can be found [here](https://github.com/Lambda-School-Labs/Labs25-Human_Rights_First-TeamC-FE).


![MIT](https://img.shields.io/packagist/l/doctrine/orm.svg)
![Python](https://img.shields.io/badge/python-3.8-blue)
![Docker](https://img.shields.io/badge/Docker-19.03.6-blue)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)


### Tech Stack

#### Python Packages
- Pandas
- Snorkel
- GeoPy
- NLTK
- Scikit-learn
- Psycopg2

#### DevOps
- Docker
- PostgreSQL
- SQLAlchemy
- AWS CloudWatch
- AWS Lambda
- AWS Elastic Beanstalk
- FastAPI

## Overview

<p align="center">
<img src="https://raw.githubusercontent.com/Lambda-School-Labs/Labs25-Human_Rights_First-TeamC-DS/main/DS_Strcuture.png" width = "500">
</p>


### Data 

Currently we are using data from [Police Brutality 2020](https://github.com/2020PB/police-brutality), which primarily sources data from Reddit posts. This data as of August 2020 was used to train our model and seed our database. New incidents and evidence from PB2020 will be also added to the database via a cron job executed by AWS Lambda. One of our goals for future releases is to include more dynamic social media scraping, like Twitter.


### Processing and Model

Incident data was cleaned, and location metadata was added to each incident with a geocoder. 
In order to create a model which predicts which type of force was deployed, we first created a training dataset using a new method of weakly supervised learning with Snorkel. 

For more information on our data cleaning process, how we used Snorkel, and our model, see our [machine learning readme](./notebooks/README.md).

### Database Schema

<p align="center">
<img src="https://raw.githubusercontent.com/Lambda-School-Labs/Labs25-Human_Rights_First-TeamC-DS/main/dbssetup/DB_Schema.png" width = "350">
</p>

For information, see our [database readme](./dbsetup/README.md).

### API Endpoints

![**link**](http://human-rights-considered.eba-api7kmju.us-east-1.elasticbeanstalk.com/)

#### Route: `/incidents`
##### Method: `GET`
##### Description: 
Read all incidents of police use of force. Incidents can be identified by their unique id, eg: `ca-sanfrancisco-1`. 
##### Schema:
```
[
  {
    "id": "string",
    "place_id": 0,
    "descr": "string",
    "date": "string",
    "evidences": [
      {
        "incident_id": "string",
        "link": "string",
        "id": 0
      }
    ],
    "tags": [
      {
        "incident_id": "string",
        "tag": "string",
        "id": 0
      }
    ],
    "place": {
      "city": "string",
      "state_name": "string",
      "state_code": "string",
      "latitude": "string",
      "longitude": "string",
      "id": 0
    }
  }
]
```

#### Route: `/incidents/{tag}`
##### Method: `GET`
##### Description: 
Read incidents by tag. For example: `/incidents/projectiles`

Sortable Tags:
- Blunt Impact
- Chemical
- EHC Soft Technique
- EHC Hard Technique
- Projectiles
#### Schema:
```
see /incidents endpoint above
```

#### Route: `/cron_update`
##### Method: `POST`
##### Description: 
Endpoint for the cron job which updates the database with new incidents and evidence from PB2020. 
##### Schema:
```
WIP
```

See the [cron readme](./project/app/cron_pb2020/README.md). 
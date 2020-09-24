# Human Rights Considered - Data Science Backend

WIP - see raw for comments

<!--- are we going to change the name of this repo? will future teams get added to this or make a copy and work on that? how will it look going forward --->


## Overview

<!--- how to align center? --->
<img src="https://raw.githubusercontent.com/Lambda-School-Labs/Labs25-Human_Rights_First-TeamC-FE/main/src/assets/HRC.png" width = "500">

HRF schpeel
[Human Rights First](https://www.humanrightsfirst.org/)


## DS Contributors

<!--- add images? --->
|Axel Corro|Michelle Hottinger|Miriam Ali|      
| :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: |
|                      [<img src="" width = "200" />](https://github.com/axefx)                       |                      [<img src="" width = "200" />](https://github.com/michhottinger)                       |                      [<img src="" width = "200" />](https://https://github.com/maiali13/)                       |   
|                 [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/axefx)                 |            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/michhottinger)             |           [<img src="https://github.com/favicon.ico" width="15"> ](https://https://github.com/maiali13/)            |    
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/axel-corro/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/michellehottinger/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/miriam-ali/) |

<!--- what license, if any?--->
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

### Data Sources

Currently we are using data from [Police Brutality 2020](https://github.com/2020PB/police-brutality), which primarily sources data from Reddit posts. One of our goals for future releases is to include more dynamic social media scraping, like Twitter. 

For more information, see our [database readme](./dbsetup/README.md).
<!--- TODO update dbsetup repo readme with any additional details --->

<img src="https://raw.githubusercontent.com/Lambda-School-Labs/Labs25-Human_Rights_First-TeamC-DS/main/dbssetup/DB_Schema.png" width = "350">

cleaning, geoloc, snorkel weak supervision to train model to predict which type of excessive force was used. 

For more information on our data cleaning process and the NER model, see our [machine learning readme](./notebooks/README.md).
<!--- TODO write notebook repo readme with explanations of ML and data cleaning process --->

<img src="https://raw.githubusercontent.com/Lambda-School-Labs/Labs25-Human_Rights_First-TeamC-DS/main.DS_Strcuture.png" width = "600">


## API Endpoints
![link](http://human-rights-considered.eba-api7kmju.us-east-1.elasticbeanstalk.com/)

For more information, see our [app readme](./project/README.md).
<!--- TODO write data engineering repo readme, with link to cron job README  --->

### Route: `/incidents`
#### Method: `GET`
#### Description: 
Read incidents
#### Schema:
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

### Route: `/incidents/{tag}`
#### Method: `GET`
#### Description: 
Read incidents by tag
#### Schema:
```
see /incidents endpoint above
```

### Route: `/cron_update`
#### Method: `POST`
#### Description: 
Endpoint for the cron job which updates the database with new incidents and evidence from PB2020. 
#### Schema:
```
WIP
```
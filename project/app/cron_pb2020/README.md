# Cron pb2020

This is a lambda function handler to be deployed on AWS lambda

- visits [https://raw.githubusercontent.com/2020PB/police-brutality/data_build/all-locations.json](https://raw.githubusercontent.com/2020PB/police-brutality/data_build/all-locations.json) to fetch data of police brutality incidents

- Sends new incidents data to http://human-rights-considered.eba-api7kmju.us-east-1.elasticbeanstalk.com/cron_update endpoint to update the relational database

Plan:

Function is implemented to be deployed on aws lambda. It will be executed by aws cloudwatch daily to update database with new incidents.


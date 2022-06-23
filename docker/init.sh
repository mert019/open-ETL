#!/bin/sh

flask fab create-admin --username admin --firstname admin --lastname admin --email admin@admin.com --password password

flask fab create-db

# Import ETL_USER role.
flask fab import-roles -p ./docker/roles.json

python run.py
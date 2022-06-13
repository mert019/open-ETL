#!/bin/bash

flask fab create-admin --username admin --firstname admin --lastname admin --email admin@admin.com --password password

flask fab create-db

python run.py

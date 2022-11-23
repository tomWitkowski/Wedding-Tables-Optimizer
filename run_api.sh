#!/bin/bash

cd api
pip install -r requirements.txt # that should be moved to docker
echo 'visit route with /docs and see documentation of the api'
uvicorn main:app
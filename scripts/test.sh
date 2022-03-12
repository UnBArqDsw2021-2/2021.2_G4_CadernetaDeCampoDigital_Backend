#!/bin/bash

coverage run manage.py test 
coverage report -m 
coverage xml -o cov.xml
#!/bin/bash

pytest --cov --no-cov-on-fail
coverage report -m 
coverage xml -o coverage.xml
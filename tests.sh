#!/bin/bash
coverage erase
coverage run -a --branch main.py
coverage run -a --branch main.py -wdir tmp/allround1 config.failure
coverage run -a --branch main.py examples/ensys_allround1_config.json
coverage run -a --branch main.py -wdir tmp/allround1 examples/ensys_allround1_config.json
coverage run -a --branch main.py -wdir tmp/allround1 -olp examples/ensys_allround1_config.json 
coverage run -a --branch -m unittest discover
coverage report
coverage xml
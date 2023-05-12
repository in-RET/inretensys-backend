#!/bin/bash
coverage erase
coverage run -a --branch main.py
coverage run -a --branch main.py -wdir tmp/allround1 cbc.failure
coverage run -a --branch main.py examples/ensys_allround1_cbc.json
coverage run -a --branch main.py -wdir tmp/allround1_1 examples/ensys_allround1_cbc.json
coverage run -a --branch main.py -wdir tmp/allround1_2 -olp examples/ensys_allround1_cbc.json 
coverage run -a --branch -m unittest discover src
coverage report
coverage html
coverage xml

rm -r tmp
rm -r dumps
rm -r logs
coverage erase
coverage run -a main.py
coverage run -a main.py -wdir tmp/allround1 config.failure
coverage run -a main.py examples/ensys_allround1_config.json
coverage run -a main.py -wdir tmp/allround1 examples/ensys_allround1_config.json
coverage run -a main.py -wdir tmp/allround1 -olp examples/ensys_allround1_config.json 
coverage run -a -m unittest discover
coverage report
coverage html
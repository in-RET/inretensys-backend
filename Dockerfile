FROM gurobi/optimizer:latest

WORKDIR /app

ADD dist/InRetEnsys-0.2a1-py3-none-any.whl .

# Install InRetEnsys with all dependencies, wheels are nice!
RUN pip install InRetEnsys-0.2a1-py3-none-any.whl

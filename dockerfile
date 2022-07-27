FROM gurobi/optimizer:latest

# Install InRetEnsys with all dependencies, wheels are nice!
WORKDIR /app

ADD dist/InRetEnsys-0.2a1-py3-none-any.whl .
RUN pip install InRetEnsys-0.2a1-py3-none-any.whl

# Add Files
# ADD hsncommon .
ADD main.py .

# Old ENTRYPOINT from Gurobi-Solver Image
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]

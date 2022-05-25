FROM python:latest

# Set Workdir
WORKDIR /app

# Copy and Install Requirements
COPY requirements_code.txt .
RUN pip install -r requirements_code.txt

# Copy Source
COPY . /app
CMD [ "python", "/app/main.py" ]
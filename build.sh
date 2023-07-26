#!/bin/bash
docker build -t inretensys:0.2a6-gurobi -f production/gurobi/dockerfile .
docker build -t inretensys:0.2a6-cbc -f production/cbc/dockerfile .
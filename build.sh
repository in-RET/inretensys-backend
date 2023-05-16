#!/bin/bash
docker build -t inretensys:0.2a5-gurobi -f production/gurobi/dockerfile .
docker build -t inretensys:0.2a5-cbc -f production/cbc/dockerfile .
#!/bin/bash
docker build -t inretensys:0.2a7-gurobi -f production/gurobi/dockerfile .
docker build -t inretensys:0.2a7-cbc -f production/cbc/dockerfile .

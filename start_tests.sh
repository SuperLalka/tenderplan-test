#!/bin/bash

export PYTEST_PARAMS=$*
docker-compose -f test.yml up --build -V --abort-on-container-exit &&
docker-compose -f test.yml down

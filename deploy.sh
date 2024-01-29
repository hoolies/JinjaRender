#!/bin/bash

docker build -t TemplateTester .
docker run --rm -p 8080:8080 TemplateTester

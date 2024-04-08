#!/bin/bash

docker build -t JinjaRender .
docker run --rm -p 8080:8080 JinjaRender

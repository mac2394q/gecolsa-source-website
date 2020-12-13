#!/usr/bin/env bash
docker build -t registry.gitlab.com/axiacore/${PWD##*/} .
docker push registry.gitlab.com/axiacore/${PWD##*/}

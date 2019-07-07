#!/bin/bash
set -e
coverage run manage.py test tests --testrunner xmlrunner.extra.djangotestrunner.XMLTestRunner --no-input
coverage xml
if [[ ! -z "${DEFAULT_WORKING_DIRECTORY}" ]]; then
    python ./ci/rewrite_sources.py ./coverage.xml "${DEFAULT_WORKING_DIRECTORY}"
fi

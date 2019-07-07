#!/bin/bash
set -e
coverage run manage.py test tests --testrunner xmlrunner.extra.djangotestrunner.XMLTestRunner --no-input
coverage xml

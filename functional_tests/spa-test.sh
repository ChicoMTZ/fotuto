#!/bin/sh

# This script configure que requirements for spa e2e tests.
#
# Basically it create an SQLite database and instruct django to use it.
#
# **Caution:** This script assumes that fotuto has been installed following the steps in INSTALL.rst file
# **Caution:** you need to manually start the django server
#
# Available commands:
#   config : setup the requirements for tests
#   clear  : remove tests setup
#
# Additionally you can pass a second parameter specifying the path to the python executable, if ommitted it will use
# the path of the environment created during install.
#
# Usage:
#
# Config tests:
#   ./spa-test.sh config
#
# Then run protractor test
#   protractor static/spa/protractor.conf.js
#
# And finally clean setup test
#   ./spa-test.sh clean
#
# Using with other python executable:
#
#   ./spa-test.sh config python
#   ./spa-test.sh config /home/fotuto/virtualenv/python2.7

# Save fotuto project location
DIR="$( dirname $( dirname "$0" ) )";

PYTHON=${2:-"$DIR/../env/bin/python"}

if [ "$1" = config ]; then
    echo "Init config..."
    # Use spa test settings
    cp --backup $DIR/fotuto/settings_local.py.spa_test $DIR/fotuto/settings_local.py
    # Generate the database
    $PYTHON $DIR/manage.py migrate
    # Load fixtures
    $PYTHON $DIR/manage.py loaddata $DIR/functional_tests/spa_fixtures.json
    # Start django development server
    # screen -d -m $PYTHON $DIR/manage.py runserver
    echo "SPA test has been configures successfully"

elif [ "$1" = clean ]; then
    echo "Init clean..."
    # Restore saved settings
    mv $DIR/fotuto/settings_local.py~ $DIR/fotuto/settings_local.py
    # Remove database
    rm $DIR/db_spa_tests.sqlite3
    echo "SPA test has been configures successfully"

else
    echo Missing command
fi

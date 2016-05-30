====================
Fotuto Install Guide
====================

Quick Install Development Environment
=====================================

1. Install SO dependences::

     sudo apt-get install python-pip python-virtualenv libjpeg-dev zlib1g-dev python-dev

2. Create environment and install packages::

     cd PROJECT_ROOT
     virtualenv env
     source env/bin/activate
     pip install -r requirments.txt

   .. note:: If use PostgreSQL, maybe is required to install::

        sudo apt-get install libpq-dev
        sudo apt-get install postgresql postgresql-contrib
        pip install psycopg2

      Then create the database::

         sudo -u postgres createdb shrimps

      And change database settings by rename `fotuto/settings_local.py.example` to
      `fotuto/settings_local.py` and change the values.

3. Generate tables in database::

     python manage.py migrate

4. Create superuser::

     python manage.py createsuperuser

5. Add static resources::

     sudo apt-get install npm
     sudo npm install -g bower
     sudo ln -s /usr/bin/nodejs /usr/bin/node
     cd PROJECT_ROOT
     bower install

6. Start development server::

     python manage.py runserver

Run Tests
=========

.. note:: Before continue, be sure to activate the virtual environment created on step 2.

Back-end Tests
--------------

.. code::

   pip install -r requirments_test.txt
   python manage.py test

Front-end Tests
---------------
Execute the following commands to configure and run SPA tests::

   npm install karma karma-cli protractor screen
   npm install karma-ng-html2js-preprocessor --save-dev
   webdriver-manager update
   python manage.py runserver
   karma fotuto/static/spa/karma.conf.js
   ./functional_tests/spa-test.sh config
   protractor fotuto/static/spa/protractor.conf.js
   ./functional_tests/spa-test.sh clean


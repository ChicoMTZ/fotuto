============================
Guide for Add-ons developers
============================

You can add new functions to Fotuto. We called it **add-ons** and its are regular Django_ apps.

To integrate your add-on to Fotuto, you need to add the name of your app to the setting ``ADDITIONAL_APPS`` in the
``settings_local.py`` file. Then Fotuto will detects and use automatically ``urls`` module in your add-on.

.. note:: The filesystem path to your add-on need to be in system var :envvar:`PYTHON_PATH` or your add-on need to
   be installed on the same python `virtual environment`_ used by Fotuto.

Menus items
===========
To add menu items, add fixtures to add/overwrite fotuto default :ref:`menu items <developers-fotuto-menu-items>`.

Filters
=======
Fotuto provide some AngularJS_ filters to use in the SPA. All shared filters can be found in :file:`static/spa/shared/fotuto.filters.js`.

Filter getItem
--------------
Used to get an item from a list given a property with a value. If the parameter is just a string it will search by the
``slug`` property. Also, the parameter could be an object in the format
``{'<PROPERTY_NAME>[__startswith]' : '<VALUE>'}``. By adding ``__startswith`` tail to the property name it will search the
value of the property that starts with the *<VALUE>*.

Here are some usage examples:

Given a list of :class:`vars.models.Vars`, to obtain the var with:

1. ``slug`` = *door-sensor*, it will need to pass just the string::

   {{ var_list | getItem:'door-sensor' }}


2. ``id`` = *1*, will be needed to pass an object::

   {{ var_list | getItem:{'id': 1} }}


3. ``name`` starting by *"Door Sen"*, will be needed to pass an object with property tail::

   {{ var_list | getItem:{'name__startswith': "Door Sen"} }}

.. _Django: http://djangoproject.com
.. _virtual environment: http://pypi.python.org/pypi/virtualenv
.. _AngularJS: http://angularjs.org
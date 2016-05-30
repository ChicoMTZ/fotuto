===========================
Guide for fotuto developers
===========================

Backend
=======
The Fotuto backend has been created using Django_ and several Django apps.

API
---
To generate an API from the models has been used `Django REST framework`_ for the :doc:`API </api>`.

Admin
-----

Testing
-------
.. todo::

.. _developers-fotuto-menu-items:

Menus items
-----------
Some menus items are customizable, it resides in :doc:`/ref/fmenus`. There are three positions
where menu will be displayed:

* **Main:** The main top bar, at right side of the site logo.
* **View:** In the top of the content area.
* **User:** In the submenu behind user menu at right side of the top bar.

The :doc:`/ref/fmenus` provides the AngularJS_ directive ``<f-menu>`` to use in SPA HTML files it display the menu items
specified in it ``position`` attribute i.e. ``<f-menu position="view"></f-menu>``.

.. todo:: add link to attribute reference in ``position`` on previous paragraph

Also, :doc:`/ref/fmenus` provide and include for *View* menu, you can place it in the view by adding the following tag::

  <ng-include src="'/static/spa/components/fmenus/_menu_view.html'"></ng-include>

Front-end
=========
The Fotuto front-end is build as an SPA_ using AngularJS_ and other JavaScript libraries like `D3.js`_.

Testing
-------

E2E Test
~~~~~~~~
.. todo:: Protractor

Unittest
~~~~~~~~
.. todo:: Karma

Documentation
=============
This documentation is done using reStructureText_ and can be built to generate in HTML or other formats with Sphinx_.

.. todo:: Define which to install for generate docs

Be sure to install required packages if you want to generate documentation.

To generate HTML files, from the :file:`docs` directory execute the following::

  make html

To generate reference files from Fotuto modules, move to :file:`docs` directory and execute the following command::

  sphinx-apidoc -d 1 -f -o ref ../ ../**/migrations/*


.. _Django: http://djangoproject.com
.. _Django REST framework: http://http://www.django-rest-framework.org
.. _SPA: https://en.wikipedia.org/wiki/Single-page_application
.. _AngularJS: http://www.angularjs.org
.. _D3.js: https://d3js.org/
.. _reStructureText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://www.sphinx-doc.org
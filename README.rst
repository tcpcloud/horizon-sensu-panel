|License badge|

============================
Horizon Monitoring Dashboard
============================

Sensu dashboard as Horizon plugin.

**Allows list events from multi Sensu APIs aka Uchiwa datacenters.**

Known Error Database as optional service provide store for your errors and workarounds.

**Monitoring, issues and solutions in one dashboard.**

|Animation|

.. contents::
   :local:

Overview
========

This plugin provide ``Monitoring`` dashboard with these panels

* Current Events
* Event Stahes
* Service Checks
* Aggregations
* Monitored Clients
* Monitoring Status

optionaly with configured KEDB is there two additional panels

* Known Errors
* Workarounds

Installation notes
==================

Requirements
------------

* Openstack Horizon
* Sensu API >= 0.16.0
* KEDB is optional

.. code-block:: bash

    pip install horizon-sensu-dashboard

Configuration Sensu
-------------------

* add 'horizon_monitoring' to ``INSTALLED_APPS`` tuple
* add 'monitoring' to 'dashboards' key in ``HORIZON_CONFIG``
* and config for your Sensu API
 
.. code-block:: python

    SENSU_HOST='localhost'
    SENSU_PORT=4567


for more Sensu APIs write this

.. code-block:: python

    SENSU_API = {
        'DC1': {'host': '10.10.10.10'},
        'DC2': {'host': '10.10.10.11', 'port': 9999, 'icon': 'fa fa-cloud'},
    }

for custom check filter you could write this

.. code-block:: python

    def check_filter(check):
        return ":".join(check['name'].split("_")[1:-1])

    SENSU_CHECK_FILTER = check_filter

this filter is applied on check in event view, default returns check name.

Configuration KEDB
------------------

if you are using service `KEDB`_ put this into your ``settings.py``:

.. code-block:: python

    KEDB_HOST='localhost'
    KEDB_PORT=6754

.. _`KEDB`: https://github.com/tcpcloud/kedb.git

Read more
=========

* http://docs.openstack.org/developer/horizon/topics/tutorial.html
* http://sensuapp.org/docs/0.16/api
* http://docs.openstack.org/developer/horizon/_modules/horizon/tables/base.html
* http://docs.openstack.org/developer/horizon/ref/tables.html
* http://nagios.sourceforge.net/docs/3_0/flapping.html
* https://github.com/ehazlett/sensu-py/
* https://github.com/tcpcloud/kedb.git

.. |License badge| image:: http://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat
.. |Animation| image:: https://github.com/tcpcloud/horizon-sensu-panel/raw/master/docs/images/animation.gif
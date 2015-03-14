|License badge|

============================
Horizon Monitoring Dashboard
============================

Sensu panels in the Horizon interface. With configured KEDB provide Known Error with workarounds over Sensu checks.

Dashboards
----------

* Monitoring

Panels
------

* Current Events
* Event Stahes
* Service Checks
* Aggregations
* Monitored Clients
* Monitoring Status

Panels with configured KEDB
---------------------------

* Known Errors
* Workarounds

Requirements
------------

* Python 2.6 / 2.7
* Openstack Horizon
* Sensu API >= 0.16.0
* KEDB is optional

Installation notes
------------------

* add 'horizon_monitoring' to INSTALLED_APPS tuple
* add 'monitoring' to 'dashboards' key in HORIZON_CONFIG
* add to horizon settings file
 
.. code-block:: pyton

    SENSU_HOST='localhost'
    SENSU_PORT=4567


if you using service KEDB

.. code-block:: python

    KEDB_HOST='localhost'
    KEDB_PORT=6754


Read more
-----

* http://docs.openstack.org/developer/horizon/topics/tutorial.html
* http://sensuapp.org/docs/0.16/api
* http://docs.openstack.org/developer/horizon/_modules/horizon/tables/base.html
* http://docs.openstack.org/developer/horizon/ref/tables.html
* http://nagios.sourceforge.net/docs/3_0/flapping.html
* https://packages.debian.org/wheezy/nagios-plugins-openstack
* https://github.com/ehazlett/sensu-py/
* https://github.com/tcpcloud/kedb.git

`Documentation`_

.. |License badge| image:: http://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat
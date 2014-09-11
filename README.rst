|License badge|

==========
Horizon Monitoring Dashboard
==========

This is a simple Horizon based interface for Sensu Monitoring Framework with Known Error Database.


Requirements
-----

* Python 2.6 / 2.7
* Openstack Horizon
* Sensu API
* KEDB is opetional

Installation notes
------------

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


Screenshots
-----

.. image:: /docs/source/_static/imgs/show_me.gif

Read more
-----

* http://docs.openstack.org/developer/horizon/topics/tutorial.html
* http://sensuapp.org/docs/0.12/api
* http://docs.openstack.org/developer/horizon/_modules/horizon/tables/base.html
* http://docs.openstack.org/developer/horizon/ref/tables.html
* http://nagios.sourceforge.net/docs/3_0/flapping.html
* https://packages.debian.org/wheezy/nagios-plugins-openstack
* https://github.com/ehazlett/sensu-py/


`Documentation`_

.. |License badge| image:: http://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat
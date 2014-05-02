
# Horizon Monitoring Panels

This is a simple Horizon based interface for Sensu.

## Installation notes

* add 'horizon_monitoring' to INSTALLED_APPS tuple
* add 'monitoring' to 'dashboards' key in HORIZON_CONFIG
* add to horizon settings file
 
    SENSU_HOST='localhost'
    SENSU_PORT=4567

## Read more

* http://docs.openstack.org/developer/horizon/topics/tutorial.html
* http://sensuapp.org/docs/0.12/api
* http://docs.openstack.org/developer/horizon/_modules/horizon/tables/base.html
* http://nagios.sourceforge.net/docs/3_0/flapping.html
* https://packages.debian.org/wheezy/nagios-plugins-openstack
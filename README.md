
# Horizon Billing Panel

This is a simple Horizon-based interface for billometer.

To enable it in dashboard, install the horizon_billing package and turn it on in openstack-dashboard's local_settings.py:

* add 'horizon_billing' to INSTALLED_APPS tuple;
* add 'billing' to 'dashboards' key in HORIZON_CONFIG.


Prometheus
===========

Federation
-----------

.. code-block:: yaml

  scrape_configs:
    - job_name: 'fed'
      scheme: https
      honor_labels: true
      metrics_path: '/federate'
      params:
        'match[]':
        - '{job="kube-state-metrics"}'
      static_configs:
      - targets:
        - '10.0.0.10'

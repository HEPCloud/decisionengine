First command ``cd`` is just to make sure that you end up in a directory that will contain two subdirectory ``decisionengine`` and ``decisionengine_modules``. Of course this can be done in any directory, not necessarily home directory.

Decisionengine framework
========================

Prerequisites:
^^^^^^^^^^^^^^

.. code-block::

   yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
   yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
   yum install -y python3 python3-pip python36-devel postgresql11 postgresql11-server
   pip3 install pandas DBUtils psycopg2-binary tabulate mock pytest toposort

Build & test
^^^^^^^^^^^^

.. code-block::

   cd
   git clone https://github.com/HEPCloud/decisionengine

   export PYTHONPATH=`pwd`

   python3 -m pytest

   ==================================== test session starts ====================================
   platform linux -- Python 3.6.8, pytest-6.0.1, py-1.9.0, pluggy-0.13.1
   rootdir: /cloud/login/knoepfel/de-devel/decisionengine
   plugins: timeout-1.4.2, postgresql-2.5.1, profiling-1.7.0
   collected 89 items

   framework/config/tests/test_config.py .............                                   [ 14%]
   framework/config/tests/test_policies.py ....                                          [ 19%]
   framework/dataspace/datasources/tests/test_postgresql.py ......                       [ 25%]
   framework/dataspace/tests/test_Reaper.py .......                                      [ 33%]
   framework/dataspace/tests/test_datablock.py ..............                            [ 49%]
   framework/engine/tests/test_client_only.py ..                                         [ 51%]
   framework/engine/tests/test_startup.py ..                                             [ 53%]
   framework/logicengine/tests/test_cascaded_rules.py ..                                 [ 56%]
   framework/logicengine/tests/test_construction.py .....                                [ 61%]
   framework/logicengine/tests/test_facts.py .....                                       [ 67%]
   framework/logicengine/tests/test_pandas_fact.py ..                                    [ 69%]
   framework/logicengine/tests/test_rule_with_negated_fact.py ..                         [ 71%]
   framework/logicengine/tests/test_simple_configuration.py ..                           [ 74%]
   framework/taskmanager/tests/test_processing_state.py .....                            [ 79%]
   framework/taskmanager/tests/test_task_manager.py ...                                  [ 83%]
   framework/tests/test_defaults.py ...                                                  [ 86%]
   framework/tests/test_reaper.py ...                                                    [ 89%]
   framework/tests/test_restart_channel.py .                                             [ 91%]
   framework/tests/test_sample_config.py ...                                             [ 94%]
   framework/tests/test_start_with_no_channels.py .                                      [ 95%]
   framework/util/tests/test_fs.py ...                                                   [ 98%]
   framework/util/tests/test_tsort.py .                                                  [100%]

   =============================== 89 passed in 90.01s (0:01:30) ===============================

Decisionengine_modules
======================

Prerequisites:
^^^^^^^^^^^^^^

In Addition to above installed packages

.. code-block::

   yum install condor
   pip3 install htcondor boto boto3 google_auth google-api-python-client gcs-oauth2-boto-plugin

Test
^^^^

.. code-block::

   cd

   git clone https://github.com/HEPCloud/decisionengine_modules
   python3 -m pytest decisionengine_modules

Current status:

.. code-block::

   [root@fermicloud371 tmp]# python3 -m pytest decisionengine_modules
   ==================================== test session starts =====================================
   platform linux -- Python 3.6.8, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
   rootdir: /root/junjk
   collected 85 items

   decisionengine_modules/AWS/tests/test_AWSInstancePerformance.py ..                     [  2%]
   decisionengine_modules/AWS/tests/test_AWSJobLimits.py ..                               [  4%]
   decisionengine_modules/AWS/tests/test_AWSOccupancyWithSourceProxy.py ..                [  7%]
   decisionengine_modules/AWS/tests/test_AWSSpotPriceWithSourceProxy.py ..                [  9%]
   decisionengine_modules/AWS/tests/test_AWS_figure_of_merit_publisher.py ..              [ 11%]
   decisionengine_modules/AWS/tests/test_AWS_price_performance_publisher.py ..            [ 14%]
   decisionengine_modules/AWS/tests/test_FigureOfMerit.py ...                             [ 17%]
   decisionengine_modules/tests/test_AwsBurnRate.py ..                                    [ 20%]
   decisionengine_modules/tests/test_GCEBillingInfo.py ..                                 [ 22%]
   decisionengine_modules/tests/test_GCEFigureOfMerit_publisher.py ..                     [ 24%]
   decisionengine_modules/tests/test_GCEInstancePerformanceInfo.py ..                     [ 27%]
   decisionengine_modules/tests/test_GCEPricePerformance_publisher.py ..                  [ 29%]
   decisionengine_modules/tests/test_GCEResourceLimits.py ..                              [ 31%]
   decisionengine_modules/tests/test_GceBurnRate.py ..                                    [ 34%]
   decisionengine_modules/tests/test_GceFigureOfMerit.py ..                               [ 36%]
   decisionengine_modules/tests/test_GceOccupancy.py ..                                   [ 38%]
   decisionengine_modules/tests/test_NerscAllocationInfo.py ..                            [ 41%]
   decisionengine_modules/tests/test_NerscFigureOfMerit.py ..                             [ 43%]
   decisionengine_modules/tests/test_NerscFigureOfMerit_publisher.py ..                   [ 45%]
   decisionengine_modules/tests/test_NerscInstancePerformance.py ..                       [ 48%]
   decisionengine_modules/tests/test_NerscJobInfo.py ..                                   [ 50%]
   decisionengine_modules/tests/test_factory_client.py ....                               [ 55%]
   decisionengine_modules/tests/test_factory_entries.py ....                              [ 60%]
   decisionengine_modules/tests/test_factory_global.py ....                               [ 64%]
   decisionengine_modules/tests/test_fomorderplugin.py ....                               [ 69%]
   decisionengine_modules/tests/test_grid_figure_of_merit.py .                            [ 70%]
   decisionengine_modules/tests/test_htcondor_query.py ....                               [ 75%]
   decisionengine_modules/tests/test_job_clustering.py .....                              [ 81%]
   decisionengine_modules/tests/test_job_clustering_publisher.py ..                       [ 83%]
   decisionengine_modules/tests/test_job_q.py ...                                         [ 87%]
   decisionengine_modules/tests/test_slots.py ..                                          [ 89%]
   decisionengine_modules/tests/glideinwms/publishers/test_decisionenginemonitor.py ...   [ 92%]
   decisionengine_modules/tests/glideinwms/publishers/test_fe_group_classads.py ...       [ 96%]
   decisionengine_modules/tests/glideinwms/publishers/test_glideclientglobal.py ...       [100%]

   ====================================== warnings summary ======================================
   /usr/local/lib/python3.6/site-packages/boto/plugin.py:40
     /usr/local/lib/python3.6/site-packages/boto/plugin.py:40: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
       import imp

   -- Docs: https://docs.pytest.org/en/latest/warnings.html
   =============================== 85 passed, 1 warning in 9.73s ================================

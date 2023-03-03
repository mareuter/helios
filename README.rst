Helios
######

This package provides information for the sun as a web service.

Development
-----------

This package uses a submodule (`pre-commit-config`) to assist with the configuration of the pre-commit hook. After cloning the repo and initializing and updating the submodule and setting up the required dependencies for development, first install the pre-commit hook:

.. code-block:: bash

    $ pre-commit install

Next run the command to install the pre-commit configuation and associated individual configuration files:

.. code-block:: bash

    $ ./pre-commit-config/setup_pre_commit_config.py

During the first commit, the hook environment will initialize and then run all of the require steps.

The web service uses the `skyfield <https://rhodesmill.org/skyfield>`_ package for sun information.
The package requires an ephemeris file.
To grab the file, run the following from the top-level of the repository.

.. code-block:: bash

    $ python bin/setup_skyfield.py

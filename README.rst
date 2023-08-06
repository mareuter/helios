Helios
######

This package provides information for the sun as a web service.

Development
-----------

This package uses a submodule (`pre-commit-config`) to assist with the configuration of the pre-commit hook.
The web service uses the `skyfield <https://rhodesmill.org/skyfield>`_ package for sun information.
The package requires an ephemeris file.
After cloning the repo, run the following:

.. code-block:: bash

    $ make init-clone

msdss-base-dotenv
=================

Environmental file management for the Modular Spatial Decision Support Systems (MSDSS) framework.

* `PyPi <https://pypi.org/project/msdss-base-dotenv>`_
* `Github <https://www.github.com/rrwen/msdss-base-dotenv>`_
* `License <https://github.com/rrwen/msdss-base-dotenv/blob/main/LICENSE>`_

Install
=======

1. Install `Anaconda 3 <https://www.anaconda.com/>`_ for Python
2. Install ``msdss-base-dotenv`` via pip or through a conda environment

.. code::

   conda create -n msdss-base-dotenv python=3.8
   conda activate msdss-base-dotenv
   pip install msdss-base-dotenv

Quick Start
===========

After installing the package, use in Python via functions:

.. jupyter-execute::

   from msdss_base_dotenv import save_env_file, load_env_file, clear_env_file, env_exists

   # Clear existing env files
   clear_env_file()

   # Check if environment exists
   exists_before = env_exists()

   # Create key-value environmental variables to save
   env = dict(user='msdss', password='msdss123')

   # Save the environmental variables as an encrypted file
   save_env_file(env, file_path='./.env')

   # Load the encrypted environmental variables
   loaded_env = load_env_file(file_path='./.env')

   # Load with defaults
   defaults = dict(database='postgres', port='5432')
   loaded_env_defaults = load_env_file('./.env', defaults=defaults)

   # Check if environment exists after creation
   exists_after = env_exists()

   # Display the results
   print('exists_before: ' + str(exists_before))
   print('env: ' + str(env))
   print('loaded_env: ' + str(loaded_env))
   print('loaded_env_defaults: ' + str(loaded_env_defaults))
   print('exists_after: ' + str(exists_after))

API Reference
=============

.. automodule:: msdss_base_dotenv.core
    :members:

Contact
=======

Richard Wen <rrwen.dev@gmail.com>

.. toctree:: 
   :maxdepth: 2
   :hidden:

   index
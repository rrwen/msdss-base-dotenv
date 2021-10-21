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

Initialize your env file and key in a command line terminal:

>>> msdss-dotenv init

Set env variables:

>>> msdss-dotenv set USER msdss
>>> msdss-dotenv set PASSWORD msdss123

Remove env variables:

>>> msdss-dotenv set TYPO randomtypo
>>> msdss-dotenv del TYPO

Clear env file and key:

>>> msdss-dotenv clear

Get help:

>>> msdss-dotenv --help
>>> msdss-dotenv set --help
>>> msdss-dotenv del --help

Usage
=====

This package can also be used programmatically in Python via functions.

Saving and Loading Environment Variables
----------------------------------------

Create and load encrypted environment variables:

.. jupyter-execute::

   from msdss_base_dotenv import *

   # Clear existing env files
   clear_env_file()

   # Check if env exists
   exists_before = env_exists()

   # Save encrypted env vars
   env = dict(USER='msdss', PASSWORD='msdss123')
   save_env_file(env, file_path='./.env')

   # Load encrypted env vars
   loaded_env = load_env_file(file_path='./.env')

   # Load env vars with defaults
   defaults = dict(DATABASE='postgres', PORT='5432')
   loaded_env_defaults = load_env_file('./.env', defaults=defaults)

   # Check if env exists after saving vars
   exists_after = env_exists()

   # Display the results
   print('exists_before: ' + str(exists_before))
   print('env: ' + str(env))
   print('loaded_env: ' + str(loaded_env))
   print('loaded_env_defaults: ' + str(loaded_env_defaults))
   print('exists_after: ' + str(exists_after))

Editing Environment Variables
-----------------------------

Edit saved encrypted environment variable files:

.. jupyter-execute::

   from msdss_base_dotenv import *

   # Clear existing env files
   clear_env_file()

   # Save env vars
   env = dict(USER='msdss', PASSWORD='msdss123')
   save_env_file(env, file_path='./.env')

   # Remove the password variable
   del_env_var('PASSWORD')

   # Set a secret variable
   set_env_var('SECRET', 'some-secret')

   # Update with a dict
   updated_env = dict(HOST='localhost', PORT='5432')
   update_env_file(updated_env)

   # Load the env vars with edits
   edited_env = load_env_file(file_path='./.env')

   # Display the results
   print('env: ' + str(env))
   print('edited_env: ' + str(edited_env))

API Reference
=============

Core Functions
--------------

.. automodule:: msdss_base_dotenv.core
   :members:

Command Line Interface
----------------------

.. automodule:: msdss_base_dotenv.cli
   :members:

Contact
=======

Richard Wen <rrwen.dev@gmail.com>

.. toctree:: 
   :maxdepth: 2
   :hidden:

   index
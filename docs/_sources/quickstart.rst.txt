Quick Start
===========

This package can be used in either the command line terminal or via Python.

Command Line Interface (CLI)
----------------------------

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

Python
------

Create and load encrypted environment variables:

.. jupyter-execute::

   import os

   from msdss_base_dotenv import *

   # Clear existing env files
   clear_env_file()

   # Check if env exists
   exists_before = env_exists()

   # Save encrypted env vars
   env = dict(USER='msdss', PASSWORD='msdss123')
   save_env_file(env, file_path='./.env')

   # Load encrypted env vars
   load_env_file(file_path='./.env')
   loaded_env = dict(
      USER=os.environ['USER'],
      PASSWORD=os.environ['PASSWORD']
   )

   # Load env vars with defaults
   defaults = dict(DATABASE='postgres', PASSWORD='already-set')
   load_env_file('./.env', defaults=defaults)
   loaded_env_defaults = dict(
      USER=os.environ['USER'],
      PASSWORD=os.environ['PASSWORD'],
      DATABASE=os.environ['DATABASE']
   )

   # Check if env exists after saving vars
   exists_after = env_exists()

   # Display the results
   print('exists_before: ' + str(exists_before))
   print('\nenv: ' + str(env))
   print('loaded_env: ' + str(loaded_env))
   print('loaded_env_defaults: ' + str(loaded_env_defaults))
   print('\nexists_after: ' + str(exists_after))

Edit saved encrypted environment variable files:

.. jupyter-execute::

   import os

   from msdss_base_dotenv import *

   # Clear existing env files
   clear_env_file()

   # Save env vars
   env = dict(USER='msdss', PASSWORD='msdss123')
   save_env_file(env, file_path='./.env')

   # Load env vars
   load_env_file(file_path='./.env')

   # Remove the password variable
   del_env_var('PASSWORD')

   # Set a secret variable
   set_env_var('SECRET', 'some-secret')

   # Load the env vars with edits
   load_env_file(file_path='./.env')
   edited_env = dict(
      USER=os.environ['USER'],
      SECRET=os.environ['SECRET']
   )

   # Display the results
   print('env: ' + str(env))
   print('edited_env: ' + str(edited_env))
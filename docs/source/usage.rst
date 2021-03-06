Usage
=====

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
>>> msdss-dotenv init --help
>>> msdss-dotenv set --help
>>> msdss-dotenv del --help
>>> msdss-dotenv clear --help

For more information, see :class:`msdss_base_dotenv.cli.run`.

Python Class
------------

Use a :class:`msdss_base_dotenv.core.DotEnv` class to manage variables in an existing env file:

.. jupyter-execute::

   from msdss_base_dotenv import DotEnv

   # Create env
   env = DotEnv(
      secret='MSDSS_SECRET',
      password='PASSWORD',
      env_file='./.env',
      key_path=None)
   env.save()

   # Set an env var
   env.set('password', 'msdss123')

   # Get an existing env var
   password = env.get('password')
   print('password: ' + password)

   # Get a non-existent env var
   # Will print the default value 'secret-default'
   secret = env.get('secret', 'secret-default')
   print('secret: ' + secret)

   # Del the password
   env.delete('password')
   password = env.get('password')
   print('password_after_del: ' + str(password))

   # Set the password
   env.set('password', 'new-password')
   password = env.get('password')
   print('password_after_set: ' + str(password))

   # Save the current specified env vars
   env.save()

   # Load the env vars from the env_file
   env.load()

   # Remove the env files
   env.clear()

For more information, see :class:`msdss_base_dotenv.core.DotEnv`.

Python Tools
------------

Create and load encrypted environment variables:

.. jupyter-execute::

   import os

   from msdss_base_dotenv.tools import *

   # Clear existing env files
   clear_env_file()

   # Check if env exists
   exists_before = env_exists()

   # Save encrypted env vars
   env = dict(USER='msdss', PASSWORD='msdss123')
   save_env_file(env, env_file='./.env')

   # Load encrypted env vars
   load_env_file(env_file='./.env')
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

   # Clear env files
   clear_env_file()

Edit saved encrypted environment variable files:

.. jupyter-execute::

   import os

   from msdss_base_dotenv.tools import *

   # Clear existing env files
   clear_env_file()

   # Save env vars
   env = dict(USER='msdss', PASSWORD='msdss123')
   save_env_file(env, env_file='./.env')

   # Load env vars
   load_env_file(env_file='./.env')

   # Remove the password variable
   del_env_var('PASSWORD')

   # Set a secret variable
   set_env_var('SECRET', 'some-secret')

   # Load the env vars with edits
   load_env_file(env_file='./.env')
   edited_env = dict(
      USER=os.environ['USER'],
      SECRET=os.environ['SECRET']
   )

   # Display the results
   print('env: ' + str(env))
   print('edited_env: ' + str(edited_env))

   # Clear env files
   clear_env_file()

For more information see:

* :func:`msdss_base_dotenv.tools.clear_env_file`
* :func:`msdss_base_dotenv.tools.del_env_var`
* :func:`msdss_base_dotenv.tools.env_exists`
* :func:`msdss_base_dotenv.tools.load_env_file`
* :func:`msdss_base_dotenv.tools.save_env_file`
* :func:`msdss_base_dotenv.tools.set_env_var`
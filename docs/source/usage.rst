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

Use a :class:`msdss_base_dotenv.core.EnvironmentVariables` class to manage variables in an existing env file:

.. jupyter-execute::

    from msdss_base_dotenv import EnvironmentVariables
    from msdss_base_dotenv.tools import *

    # Clear existing env files
    clear_env_file()

    # Create env file
    env = dict(USER='msdss', PASSWORD='msdss123') # notice no NONEXIST var
    save_env_file(env, file_path='./.env')

    # Create object to represent env vars and load it
    env = EnvironmentVariables(nonexist='NONEXIST', user='USER', password='PASSWORD')
    env.load()

    # Get an existing env var
    password = env.get_password()
    print('password: ' + password)

    # Get a non-existent env var
    # Will print the default value 'nonexist-default'
    nonexist = env.get_nonexist('nonexist-default')
    print('nonexist: ' + nonexist)

    # Del the password
    env.del_password()
    password = env.get_password()
    print('password_after_del: ' + str(password))

    # Set the password
    env.set_password('new-password')
    password = env.get_password()
    print('password_after_set: ' + str(password))

For more information, see :class:`msdss_base_dotenv.core.EnvironmentVariables`.

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

   from msdss_base_dotenv.tools import *

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

For more information see:

* :func:`msdss_base_dotenv.tools.clear_env_file`
* :func:`msdss_base_dotenv.tools.del_env_var`
* :func:`msdss_base_dotenv.tools.env_exists`
* :func:`msdss_base_dotenv.tools.load_env_file`
* :func:`msdss_base_dotenv.tools.save_env_file`
* :func:`msdss_base_dotenv.tools.set_env_var`
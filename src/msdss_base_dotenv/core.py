import os

from functools import partial

from .tools import *

class DotEnv:
    """
    Class to manage environmental variables.

    Parameters
    ----------
    env_file : str
        The path of the file with environmental variables.
    key_path : str
        The path of the key file for the ``env_file``.
    defaults : dict
        Key and value pairs representing default environment values to be loaded. These will be loaded if ones in the ``env_file`` do not exist or are unset.
    **kwargs
        Keyword arguments defining the environmental variable name mappings for this object:

        * Each key represents an alias name referring to an environmental variable
        * Each value represents the environmental variable name
        * This allows changing env vars to refer to the same keys

    Attributes
    ----------
    env_file : str
        Same as parameter ``env_file``.
    key_path : str
        Same as parameter ``key_path``.
    defaults : dict
        Same as parameter ``defaults``.
    mappings : dict
        Dictionary of key and values relative to ``kwargs``.

    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>

    Example
    -------
    .. jupyter-execute::

        from msdss_base_dotenv import DotEnv
        from msdss_base_dotenv.tools import *

        # Clear any existing env files
        clear_env_file()

        # Create env
        env = DotEnv(secret='MSDSS_SECRET', password='PASSWORD')

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

        # Remove the env files
        env.clear()
    """
    def __init__(
        self,
        env_file='./.env',
        key_path=None,
        defaults={},
        **kwargs):

        # (DotEnv_create) Create .env file if it does not exist
        if env_exists(env_file, key_path):
            load_env_file(env_file=env_file, key_path=key_path, defaults=defaults)
        else:
            save_env_file(defaults, env_file, key_path)
        
        # (Environment_attrs) Set attrs
        self.env_file = env_file
        self.key_path = key_path
        self.mappings = kwargs

    def clear(self):
        """
        Delete env and key files.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_dotenv import *
            from msdss_base_dotenv.tools import *

            # Clear any existing env files
            clear_env_file()

            # Create default key value env
            env = dict(USER='msdss', PASSWORD='msdss123')

            # Save the key value env to an encrypted file
            save_env_file(env)
            
            # Create env and clear it
            env = DotEnv()
            env.clear()
        """
        clear_env_file(env_file=self.env_file, key_path=self.key_path)

    def delete(self, key):
        """
        Delete an environment variable.

        Parameters
        ----------
        key : str
            The key to delete a reference env var.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_dotenv import *
            from msdss_base_dotenv.tools import *

            # Clear any existing env files
            clear_env_file()

            # Create default key value env
            env = DotEnv(user='USER', password='PASSWORD')

            # Set env var values
            env.set('user', 'msdss')
            env.set('password', 'msdss123')
            
            # Delete an env var based on key alias
            env.delete('password')
        """
        name = self.mappings[key]
        del_env_var(name)

    def exists(self):
        """
        Check if a set of env vars exist based on the env and key files.

        Return
        ------
        bool
            Whether the env exists or not.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_dotenv import *
            from msdss_base_dotenv.tools import *

            # Clear any existing env files
            clear_env_file()

            # Create default key value env
            env = DotEnv(user='USER', password='PASSWORD')

            # Set env var values
            env.set('user', 'msdss')
            env.set('password', 'msdss123')

            # Check that env exists
            before_clear = env.exists()

            # Clear and check again
            env.clear()
            after_clear = env.exists()

            # Print results
            print('before_clear: ' + str(before_clear))
            print('after_clear: ' + str(after_clear))
        """
        out = env_exists(env_file=self.env_file, key_path=self.key_path)
        return out

    def get(self, key, default=None):
        """
        Obtain the value of an env var.

        Parameters
        ----------
        key : str
            The key to get a reference env var.
        default : str or None
            A default value if there is no value set for the env var.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_dotenv import *
            from msdss_base_dotenv.tools import *

            # Clear any existing env files
            clear_env_file()

            # Create default key value env
            env = DotEnv(user='USER', password='PASSWORD')

            # Set env var values
            env.set('user', 'msdss')
            env.set('password', 'msdss123')

            # Get the PASSWORD var
            password = env.get('password')
            print(password)
        """
        name = self.mappings[key]
        out = os.getenv(name, default)
        return out

    def set(self, key, value):
        """
        Sets an env var.

        Parameters
        ----------
        key : str
            The key to get a reference env var.
        value : str
            A value to set for the env var.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_dotenv import *
            from msdss_base_dotenv.tools import *

            # Clear any existing env files
            clear_env_file()

            # Create default key value env
            env = DotEnv(user='USER', password='PASSWORD')

            # Set env var values
            env.set('user', 'msdss')
            env.set('password', 'msdss123')
        """
        name = self.mappings[key]
        set_env_var(name, value)
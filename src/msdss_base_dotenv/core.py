import os

from functools import partial

from .tools import *

class EnvironmentVariables:
    """
    Class to manage environmental variables.

    Parameters
    ----------
    env_file : str
        The path of the file with environmental variables.
    key_path : str
        The path of the key file for the ``env_file``.
    **kwargs
        Keyword arguments defining the environmental attributes and variable names for this object:

        * Each key represents the attribute name
        * Each value represents the environmental variable name

    Attributes
    ----------
    env_file : str
        Same as parameter ``env_file``.
    key_path : str
        Same as parameter ``key_path``.
    \*\*kwargs
        Copies the keys and values from ``**kwargs`` to the attributes.

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

        # Create env and load
        env = EnvironmentVariables(secret='MSDSS_SECRET', password='PASSWORD')
        env.load()

        # Get an existing env var
        password = env.get_password()
        print('password: ' + password)

        # Get a non-existent env var
        # Will print the default value 'secret-default'
        secret = env.get_secret('secret-default')
        print('secret: ' + secret)

        # Del the password
        env.del_password()
        password = env.get_password()
        print('password_after_del: ' + str(password))

        # Set the password
        env.set_password('new-password')
        password = env.get_password()
        print('password_after_set: ' + str(password))
    """
    def __init__(
        self,
        env_file='./.env',
        key_path=None,
        **kwargs):

        # (Environment_kwargs) Set attrs for key value args
        for k, v in kwargs.items():
            setattr(self, k, v)
        
        # (Environment_attrs) Set standard attrs
        self.env_file = env_file
        self.key_path = key_path

    def clear(self):
        """
        Delete env and key files.

        Parameters
        ----------
        throw_error : bool
            Whether to throw an error if either the env or key file does not exist.

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
            env = EnvironmentVariables()
            env.clear()
        """
        clear_env_file(file_path=self.file_path, key_path=self.key_path)

    def delete(self, name):
        del_env_var(getattr(self, name))

    def exists(self):
        """
        Checks whether an env and key file pair exists.

        Return
        ------
        bool
            Whether or not the env and key file pair exists.

        Example
        -------
        .. jupyter-execute::

            from msdss_base_dotenv import *
            from msdss_base_dotenv.tools import *

            # Clear any existing env files
            clear_env_file()
            
            # Create env and check if it exists
            env = EnvironmentVariables()
            print(env.exists())
        """
        out = env_exists(file_path=self.env_file, key_path=self.key_path)
        return out

    def get(self, name, default=None):
        out = os.getenv(getattr(self, name), default)
        return out

    def load(self, throw_error=False):
        """
        Class to manage environmental variables.

        Parameters
        ----------
        throw_error : bool
            Whether to throw an error if either the env or key file does not exist.

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
            
            # Create env and load
            env = EnvironmentVariables(secret='MSDSS_SECRET', password='PASSWORD')
            env.load()
        """
        if self.exists():
            load_env_file(file_path=self.env_file, key_path=self.key_path)
        elif throw_error:
            raise FileNotFoundError(f'Env or key file does not exist')

    def set(self, name, value):
        set_env_var(getattr(self, name), value)
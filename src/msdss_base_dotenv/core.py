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

        # Create env
        env = DotEnv(secret='MSDSS_SECRET', password='PASSWORD')
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

        # Remove the env files
        env.clear()
    """
    def __init__(
        self,
        env_file='./.env',
        key_path=None,
        defaults={},
        **kwargs):
        self.env_file = env_file
        self.key_path = key_path
        self.defaults = defaults
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

            # Create env
            env = DotEnv(secret='MSDSS_SECRET', password='PASSWORD')
            env.save()

            # Set an env var
            env.set('password', 'msdss123')

            # Save the current specified env vars to an encrypted file
            env.save()
            
            # Create files
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

            # Create default key value env
            env = DotEnv(user='USER', password='PASSWORD')
            env.save()

            # Set env var values
            env.set('user', 'msdss')
            env.set('password', 'msdss123')
            
            # Delete an env var based on key alias
            env.delete('password')

            # Clear env files
            env.clear()
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

            # Create default key value env
            env = DotEnv(user='USER', password='PASSWORD')
            env.save()

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

            # Create default key value env
            env = DotEnv(user='USER', password='PASSWORD')
            env.save()

            # Set env var values
            env.set('user', 'msdss')
            env.set('password', 'msdss123')

            # Get the PASSWORD var
            password = env.get('password')
            print(password)

            # Clear env files
            env.clear()
        """
        name = self.mappings[key]
        out = os.getenv(name, default)
        return out

    def load(self):
        """
        Load env vars from the saved env file.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_dotenv import *

            # Create default key value env
            env = DotEnv(user='USER', password='PASSWORD')
            env.save()
            env.set('user', 'new-user')

            # Save the env vars
            env.save()
            
            # Load and see env vars
            env.load()
            user = env.get('user')
            print('user: ' + user)
            
            # Clear env files
            env.clear()
        """
        load_env_file(env_file=self.env_file, key_path=self.key_path, defaults=self.defaults)

    def save(self):
        """
        Save env vars to a file.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_dotenv import *

            # Create default key value env
            env = DotEnv(user='USER', password='PASSWORD')
            env.save()
            env.set('user', 'new-user')

            # Save the env vars
            env.save()
            
            # Load and see env vars
            env.load()
            user = env.get('user')
            print('user: ' + user)
            
            # Clear env files
            env.clear()
        """

        # (DotEnv_save_current) Gather current env vars
        current_vars = {}
        for k in self.mappings:
            name = self.mappings[k]
            if name in os.environ:
                current_vars[name] = os.environ[name]
        
        # (DotEnv_save_file) Save current env vars to a file
        save_env_file(current_vars, self.env_file, self.key_path)
        current_vars.clear()

    def set(self, key, value):
        """
        Sets an env var and saves it in the file.

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

            # Create default key value env
            env = DotEnv(user='USER', password='PASSWORD')
            env.save()

            # Set env var values
            env.set('user', 'msdss')
            env.set('password', 'msdss123')

            # Get env var values to check
            user = env.get('user')
            password = env.get('password')
            print('user: ' + user)
            print('password: ' + password)

            # Clear env files
            env.clear()
        """
        name = self.mappings[key]
        set_env_var(name, value)
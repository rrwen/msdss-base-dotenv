import copy
import dotenv
import json
import os
import pickle

from cryptography.fernet import Fernet
from io import StringIO

__PATH__ = os.path.dirname(os.path.abspath(__file__))

def _dict_to_dotenv(env_dict):
    """
    Converts a ``dict`` to a .env formatted str.
    
    Parameters
    ----------
    env_dict : dict
        Key value dictionary representing env variables.

    Returns
    -------
    str
        Str representing a .env formatted file structure.

    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>

    Example
    -------
    .. jupyter-execute::

        from msdss_base_dotenv.core import _dict_to_dotenv

        # Create default key value env
        env = dict(USER='msdss', PASSWORD='msdss123')

        # Convert to dotenv file str
        env_str = _dict_to_dotenv(env)

        # Display results
        print('env: ' + str(env))
        print('env_str: ' + env_str)
    """
    out = '\n'.join([k + '=' + str(v) for k, v in env_dict.items()])
    return out

def clear_env_file(file_path='./.env', key_path=None):
    """
    Deletes the encrypted environment file and its key if they exist.
    
    Parameters
    ----------
    file_path : str
        Path of the encrypted environment file.
    key_path : str
        Path of the key file used to unlock the encrypted file. If None, this defaults to the package's directory.

    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>

    Example
    -------
    .. jupyter-execute::

        from msdss_base_dotenv.core import save_env_file, load_env_file, clear_env_file

        # Create default key value env
        env = dict(USER='msdss', PASSWORD='msdss123')

        # Save the key value env to an encrypted file
        save_env_file(env)

        # Remove the env file and its associated key
        clear_env_file()
    """
    
    # (clear_env_file_path) Get path of encrypted env files
    env_path = os.path.abspath(file_path)
    key_path = key_path if key_path is not None else os.path.join(__PATH__, '.env.key')

    # (clear_env_file_remove) Remove the encrypted env files
    for path in [env_path, key_path]:
        if os.path.exists(path):
            os.remove(path)

def del_env_var(name, file_path='./.env', key_path=None):
    """
    Deletes an environmental variable using a file from :func:`msdss_base_dotenv.core.save_env_file`.
    
    Parameters
    ----------
    name : str
        The name of the environmental variable to be deleted.
    file_path : str
        Path of the environment save file.
    key_path : str
        Path of the key file used to unlock the save file. If None, this defaults to the package's directory.
    
    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>
    
    Example
    -------
    .. jupyter-execute::

        import os

        from msdss_base_dotenv.core import save_env_file, load_env_file, clear_env_file, del_env_var
        
        # Clear any existing env files
        clear_env_file()

        # Create key value env and save it
        env = dict(USER='msdss', PASSWORD='msdss123')
        save_env_file(env)

        # Load the saved env
        load_env_file()

        # Remove the password var from the saved env
        del_env_var('PASSWORD')

        # Load the saved env after the removal
        load_env_file()
        loaded_env = dict(
            USER=os.environ['USER'],
            PASSWORD=os.getenv('PASSWORD', None)
        )

        # Display the results
        print('env: ' + str(env))
        print('loaded_env: ' + str(loaded_env))
    """
    env = load_env_file(file_path=file_path, key_path=key_path, set_env=False, return_dict=True)
    del os.environ[name]
    del env[name]
    save_env_file(env, file_path=file_path, key_path=key_path)

def env_exists(file_path='./.env', key_path=None):
    """
    Checks if an environment exists using a saved environment file from :func:`msdss_base_dotenv.core.save_env_file`.
    
    Parameters
    ----------
    file_path : str
        Path of the environment save file.
    key_path : str
        Path of the key file used to unlock the save file. If None, this defaults to the package's directory.
    
    Returns
    -------
    bool
        Whether or not ``file_path`` and ``key_path`` exist, which define whether the env exists.
    
    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>
    
    Example
    -------
    .. jupyter-execute::

        from msdss_base_dotenv.core import save_env_file, load_env_file, clear_env_file, env_exists
        
        # Clear any existing env files
        clear_env_file()

        # Check if env exists
        exists_before = env_exists()

        # Create key value env and save it
        env = dict(USER='msdss', PASSWORD='msdss123')
        save_env_file(env)

        # Check if env exists
        exists_after = env_exists()

        # Display the results
        print('exists_before: ' + str(exists_before))
        print('exists_after: ' + str(exists_after))
    """

    # (env_exists_file_path) Get path of encrypted env file
    env_path = os.path.abspath(file_path)
    key_path = key_path if key_path is not None else os.path.join(__PATH__, '.env.key')

    # (env_exists_return) Check if env file and key exists
    out = os.path.isfile(env_path) and os.path.isfile(key_path)
    return out

def load_env_file(file_path='./.env', key_path=None, defaults={}, set_env=True, return_dict=False):
    """
    Loads a saved environment file from :func:`msdss_base_dotenv.core.save_env_file`.
    
    Parameters
    ----------
    file_path : str
        Path of the environment save file.
    key_path : str
        Path of the key file used to unlock the save file. If None, this defaults to the package's directory.
    defaults : dict
        Key and value pairs representing default environment values to be loaded. These will replace ones in ``env`` if they do not exist or are unset.
    set_env : bool
        Whether to set the ``os.environ`` with the variables in the ``file_path`` or not.
    return_dict : bool
        Whether to return a dictionary of the env variables or not.

    Returns
    -------
    dict
        Dictionary of the decrypted key value environment from ``file_path`` if ``return_dict`` is ``True``.
    
    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>
    
    Example
    -------
    .. jupyter-execute::

        import os

        from msdss_base_dotenv.core import save_env_file, load_env_file, clear_env_file
        
        # Clear any existing env files
        clear_env_file()

        # Create key value env and save it with defaults
        env = dict(USER='msdss', PASSWORD='msdss123')
        defaults = dict(DATABASE='postgres', PASSWORD='already-set')
        save_env_file(env, defaults=defaults)

        # Load the saved env file 
        load_env_file()
        loaded_env = dict(
            USER=os.environ['USER'],
            PASSWORD=os.environ['PASSWORD'],
            DATABASE=os.environ['DATABASE']
        )

        # Display the results
        print('env: ' + str(env))
        print('defaults: ' + str(defaults))
        print('loaded_env: ' + str(loaded_env))
    """
    
    # (load_env_file_path) Get path of encrypted env file
    env_path = os.path.abspath(file_path)
    key_path = key_path if key_path is not None else os.path.join(__PATH__, '.env.key')

    # (load_env_file_load) Load env details file
    with open(key_path, 'rb') as key_file, open(env_path, 'rb') as env_file:

        # (load_env_file_key) Load key store object
        key = pickle.load(key_file)
        decrypter = Fernet(key)

        # (load_env_file_encrypted) Get encrypted env details
        encrypted = pickle.load(env_file)
    
    # (load_env_file_decrypt) Decrypt env
    decrypted = decrypter.decrypt(encrypted).decode('utf-8')
    env = json.loads(decrypted)

    # (load_env_file_set) Set env variables in environ
    if set_env:

        # (load_env_file_set_defaults) Set defaults first
        defaults_str = _dict_to_dotenv(defaults)
        dotenv.load_dotenv(stream=StringIO(defaults_str), override=True)

        # (load_env_file_set_os) Set env vars in os and override defaults
        env_str = _dict_to_dotenv(env)
        dotenv.load_dotenv(stream=StringIO(env_str), override=True)

    # (load_env_file_return) Returns a dict
    if return_dict:
        out = env
        return out

def save_env_file(env, file_path='./.env', key_path=None, defaults={}):
    """
    Saves a login file with the connection details.
    
    Parameters
    ----------
    env : dict
        Key and value pairs representing environment values to be saved.
    file_path : str
        Path of the encrypted environment save file. Read/write/execute permissions will be set only for the owner of this file.
    key_path : str
        Path of the key file used to unlock the save file. If ``None``, this defaults to the package's directory.
    defaults : dict
        Key and value pairs representing default environment values to be saved. These will replace ones in ``env`` if they do not exist or are unset.

    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>

    Example
    -------
    .. jupyter-execute::

        from msdss_base_dotenv.core import save_env_file, load_env_file, clear_env_file
        
        # Clear any existing env files
        clear_env_file()

        # Create default key value env
        env = dict(USER='msdss', PASSWORD='msdss123')

        # Save the key value env to an encrypted file
        save_env_file(env)
    """

    # (save_env_file_defaults) Set default env values
    defaults = copy.deepcopy(defaults)
    defaults.update(env)
    env = copy.deepcopy(defaults)

    # (save_env_file_path) Get path of encrypted env file
    env_path = os.path.abspath(file_path)
    key_path = key_path if key_path is not None else os.path.join(__PATH__, '.env.key')

    # (save_env_file_key) Obtain key if exists or create one if not
    key_exists = os.path.isfile(key_path)
    if key_exists: # read key
        with open(key_path, 'rb') as key_file:
            key = pickle.load(key_file)
    else: # create key
        with open(key_path, 'wb') as key_file:
            key = Fernet.generate_key()
            pickle.dump(key, key_file)
        os.chmod(key_path, 0o700) # set read/write/execute only for owner
    encrypter = Fernet(key)

    # (save_env_file_encrypt) Encrypt env file
    out = encrypter.encrypt(bytes(json.dumps(env), encoding = 'utf-8'))
    with open(env_path, 'wb') as env_file:
        pickle.dump(out, env_file)

def set_env_var(name, value, file_path='./.env', key_path=None):
    """
    Sets an environmental variable using a file from :func:`msdss_base_dotenv.core.save_env_file`.
    
    Parameters
    ----------
    name : str
        The name of the environmental variable to be set.
    value : str
        The value of the environmental variable to be set.
    file_path : str
        Path of the environment save file.
    key_path : str
        Path of the key file used to unlock the save file. If None, this defaults to the package's directory.
    
    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>
    
    Example
    -------
    .. jupyter-execute::

        import os

        from msdss_base_dotenv.core import save_env_file, load_env_file, clear_env_file, set_env_var
        
        # Clear any existing env files
        clear_env_file()

        # Create key value env and save it
        env = dict(USER='msdss')
        save_env_file(env)

        # Add/set a password var to the saved env
        set_env_var('USER', 'msdssnew')
        set_env_var('PASSWORD', 'msdss123')

        # Load the saved env after the addition
        load_env_file()
        loaded_env = dict(
            USER=os.environ['USER'],
            PASSWORD=os.environ['PASSWORD']
        )

        # Display the results
        print('env: ' + str(env))
        print('loaded_env: ' + str(loaded_env))
    """
    env = load_env_file(file_path=file_path, key_path=key_path, set_env=False, return_dict=True)
    os.environ[name] = str(value)
    env[name] = os.environ[name]
    save_env_file(env, file_path=file_path, key_path=key_path)

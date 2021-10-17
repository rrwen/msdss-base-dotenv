import json
import os
import pickle

from cryptography.fernet import Fernet

__PATH__ = os.path.dirname(os.path.abspath(__file__))

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
        env = dict(user='msdss', password='msdss123')

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

def save_env_file(env, file_path='./.env', key_path=None):
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
        env = dict(user='msdss', password='msdss123')

        # Save the key value env to an encrypted file
        save_env_file(env)
    """

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
    encrypted = encrypter.encrypt(bytes(json.dumps(env), encoding = 'utf-8'))
    with open(env_path, 'wb') as env_file:
        pickle.dump(encrypted, env_file)

def load_env_file(file_path='./.env', key_path=None):
    """
    Loads a saved environment file from :func:`msdss_base_dotenv.core.save_env_file`.
    
    Parameters
    ----------
    file_path : str
        Path of the environment save file.
    key_path : str
        Path of the key file used to unlock the save file. If None, this defaults to the package's directory.
    
    Returns
    -------
    dict
        Dictionary of the decrypted key value environment from ``file_path``.
    
    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>
    
    Example
    -------
    .. jupyter-execute::

        from msdss_base_dotenv.core import save_env_file, load_env_file, clear_env_file
        
        # Clear any existing env files
        clear_env_file()

        # Create default key value env and save it
        env = dict(user='msdss', password='msdss123')
        save_env_file(env)

        # Load the saved env file 
        env = load_env_file()
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
    
    # (load_env_file_decrypt) Decrypt env details
    login = decrypter.decrypt(encrypted).decode('utf-8')
    out = json.loads(login)
    return out

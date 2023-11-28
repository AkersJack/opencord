import hashlib
import uuid
from datetime import datetime


def generate_profile_hash(user_uuid) -> str:
    """
    using uuid4() to generate a unique user id we can then simply hash the uuid to generate a profile hash for everyone
    we just need to grab the uuid on account creation:
        - use uuid4() instead of uuid1() because uuid1() uses the MAC address of the computer and the current time
        - uuid4() is random and is not guaranteed to be unique, although 5.3 undecillion versions can be generated

    https://docs.python.org/3/library/uuid.html

    :param user_uuid: UUID of the user
    :return: hashed user
    """
    return hashlib.sha256(user_uuid.encode()).hexdigest()


def generate_server_hash(owner_uuid, server_uuid) -> str:
    """
    unsure if i understand the communications correctly for opencord, but i think this would work for a hashing
    method assuming that a server owner cannot be changed

    :param owner_uuid: UUID of the server owner
    :param server_uuid: UUID of the server
    :return: hashed server
    """
    return hashlib.sha256(f"{server_uuid}{owner_uuid}".encode()).hexdigest()


def message_hash(message: str, profile_hash: str) -> str:
    """
    this is the hash that is sent with the message to the server, it is a sha256 hash of
     the message,
     the profile hash,
     and the timestamp

     ex. message["hash"] = message_hash(message_content, self.profile_hash)

    :param message: string containing message content
    :param profile_hash: string containing user profile hash
    :return: hashed message
    """
    timestamp = datetime.now()
    raw_message = f"{message}{profile_hash}{timestamp}"
    return hashlib.sha256(raw_message.encode()).hexdigest()

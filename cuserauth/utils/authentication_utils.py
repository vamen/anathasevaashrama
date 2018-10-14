import random
import hashlib
import string
from .logger_utils import init_logger
logger=init_logger()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    # use following for uncrakable random string 
    # return ''.join(random.SystemRandom.choice(chars) for _ in range(size))
    return ''.join(random.choice(chars) for _ in range(size))

def make_password(password):
    salt=id_generator()
    password=password+salt
    # replace this with argon2 or sha3 etc
    hash=hashlib.md5(password.encode('utf-8'))
    return hash.hexdigest(),salt

def check_password(hash_password,salt,password_candidate):
    password_candidate=password_candidate+salt
    logger.info(hash_password)
    logger.info(hashlib.md5(password_candidate.encode('utf-8')).hexdigest())
    if hash_password == str(hashlib.md5(password_candidate.encode('utf-8')).hexdigest()):
        return True
    return False    

def generate_token(hash_password,salt):
    token=str(hashlib.md5((hash_password+salt).encode('utf-8')).hexdigest())+salt
    return hashlib.md5(token.encode('utf-8')).hexdigest()


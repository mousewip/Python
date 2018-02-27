import math
from hashids import Hashids
ALPHABET = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
LEN = 12
salt = 'c6c482b268b0a985f9b19c03419e246a'
hashids = Hashids(salt=salt, min_length=LEN, alphabet=ALPHABET)

def hash_id_encode(n):
    return hashids.encode(int(n))
def has_id_decode(s):
    return hashids.decode(s)[0]
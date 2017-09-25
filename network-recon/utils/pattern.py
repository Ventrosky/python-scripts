from itertools import islice, product, chain
import string

def generate( n ):
    if n > 20280:
        return "Max lenght 20280"
    return ''.join(tuple(islice(chain.from_iterable(product(string.ascii_uppercase, string.ascii_lowercase, string.digits)), n)))

def convert(string):
    return string.decode("hex") 

def to_hex(string):
    return string.encode("hex")
    
def find_match(string):
    segment = convert(string)
    pattern = generate(2080)
    return pattern.find(segment)

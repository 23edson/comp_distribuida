from hashlib import md5

def hashFunction(key,mod):
    out = md5(key.encode('utf-8')).hexdigest()
    out_1 = '\0'
    for character in out:
        out_1 = str(out_1) + str(ord(character)%mod)
    return out_1

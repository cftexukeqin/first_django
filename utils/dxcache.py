from django.core .cache import cache

def set(key,value,timeout=60*5):
    return cache.set(key=key,value=value,timeout=timeout)

def get(key):
    return cache.get(key)
def delete(key):
    return cache.delete(key)
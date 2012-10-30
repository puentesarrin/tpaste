# -*- coding: utf-8 *-*
import string
import random
import hashlib


def generate_random(size=20,
    chars=string.digits + string.ascii_lowercase + string.ascii_uppercase):
    return ''.join(random.choice(chars) for x in range(size))


def generate_randomnumber(size=20):
    return int(generate_random(size, string.digits))


def generate_md5(input_text=generate_random()):
    return hashlib.md5(input_text).hexdigest()


def base62_encode(number,
    chars=string.digits + string.ascii_lowercase + string.ascii_uppercase):
    if (number == 0):
        return chars[0]
    arr = []
    base = len(chars)
    while number:
        rem = number % base
        number = number // base
        arr.append(chars[rem])
    arr.reverse()
    return ''.join(arr)


def random_base62(size=10):
    return base62_encode(generate_randomnumber(size))

#!/usr/bin/env python
from __future__ import print_function
import sys


def xor(data, key):
    result = ''
    index_max = len(key) - 1
    i = 0
    for character in data:
        output = ord(key[i]) ^ ord(character)
        result += chr(output)
        i += 1
        if i > index_max:
            i = 0
    return result


def encode(data, key, mode):
    if mode == 'decode':
        data = data.decode('base64', 'strict')
    data = xor(data, key)
    if mode == 'encode':
        data = data.encode('base64', 'strict')
    return data


def main():
    key = s_input("Key?: ")
    data = s_input("Data block?: ")
    mode = ''
    while mode not in ['encode', 'decode']:
        mode = s_input("(e)ncode or (d)ecode?: ")[0].lower()
        if mode == 'e':
            mode = 'encode'
        elif mode == 'd':
            mode = 'decode'
        else:
            mode = ''

    output = encode(data, key, mode)

    print("Key: {}".format(key))
    print ("Input data: {}".format(data))
    print("{}d data: {}".format(mode.title(), output))


if __name__ == '__main__':
    s_input = input
    if sys.version_info[:2] <= (2, 7):  # If this is Python 2, use raw_input()
        s_input = raw_input
    main()

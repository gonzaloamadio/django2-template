""" Concise UUID generation. """

import binascii
import math
import os
import uuid as _uu

INTAB = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
OUTTAB = "3A297LNjkTnpDvUuxFBP5QW8wKHJRMZaibS4mGCdeXoYVhry6Efqcgstz"
# create translation table to salt string
salttab = str.maketrans(INTAB, OUTTAB)
# revert translation to unsalt string
unsalttab = str.maketrans(OUTTAB, INTAB)

def salt_string(string):
    """
      Translate encoded UUID to another string, converting letters following
      INOUT and OUTTAB translation.
      We want to add an extra layer of security because we are going to expose
      this UUID translations in slugs
    """
    return string.translate(salttab)

def unsalt_string(string):
    """
      Revert translation to unstal string
    """
    return string.translate(unsalttab)

def int_to_string(number, alphabet, padding=None):
    """
    Convert a number to a string, using the given alphabet.
    The output has the most significant digit first.
    """
    output = ""
    alpha_len = len(alphabet)
    while number:
        number, digit = divmod(number, alpha_len)
        output += alphabet[digit]
    if padding:
        remainder = max(padding - len(output), 0)
        output = output + alphabet[0] * remainder
    return output[::-1]


def string_to_int(string, alphabet):
    """
    Convert a string to a number, using the given alphabet.
    The input is assumed to have the most significant digit first.
    """
    number = 0
    alpha_len = len(alphabet)
    for char in string:
        number = number * alpha_len + alphabet.index(char)
    return number


class ShortUUID(object):
    def __init__(self, alphabet=None):
        if alphabet is None:
            alphabet = list("23456789ABCDEFGHJKLMNPQRSTUVWXYZ" "abcdefghijkmnopqrstuvwxyz")

        self.set_alphabet(alphabet)

    @property
    def _length(self):
        """
        Return the necessary length to fit the entire UUID given
        the current alphabet.
        """
        return int(math.ceil(math.log(2 ** 128, self._alpha_len)))

    def _encode(self, uuid, pad_length=None):
        """
        Encode a UUID into a string (LSB first) according to the alphabet

        If leftmost (MSB) bits are 0, the string might be shorter.
        """
        if pad_length is None:
            pad_length = self._length
        #return int_to_string(uuid.int, self._alphabet, padding=pad_length)
        return int_to_string(uuid.int, self._alphabet, padding=pad_length)

    def encode(self, uuid, pad_length=None):
        """
            Encode and Salt string
        """
        if pad_length is None:
            pad_length = self._length
        #return int_to_string(uuid.int, self._alphabet, padding=pad_length)
        return salt_string(self._encode(uuid))

    def _decode(self, string, legacy=False):
        """
        Decode a string according to the current alphabet into a UUID
        Raises ValueError when encountering illegal characters
        or a too-long string.

        If string too short, fills leftmost (MSB) bits with 0.

        Pass `legacy=True` if your UUID was encoded with a ShortUUID version
        prior to 0.6.0.
        """
        if legacy:
            string = string[::-1]
        return _uu.UUID(int=string_to_int(string, self._alphabet))

    def decode(self, string, legacy=False):
        if legacy:
            string = string[::-1]
        string = unsalt_string(string)
        return self._decode(string)

    def uuid(self, name=None, pad_length=None):
        """
        Generate and return an encoded(and salted) UUID.

        If the name parameter is provided, set the namespace to the provided
        name and generate a UUID.
        """
        if pad_length is None:
            pad_length = self._length

        # If no name is given, generate a random UUID.
        if name is None:
            uuid = _uu.uuid4()
        elif name.lower().startswith(("http://", "https://")):
            # NAMESPACE_URL is a constant predefined in library
            uuid = _uu.uuid5(_uu.NAMESPACE_URL, name)
        else:
            # NAMESPACE_DNS is a constant predefined in library
            uuid = _uu.uuid5(_uu.NAMESPACE_DNS, name)
        return self.encode(uuid, pad_length)

    def random(self, length=None):
        """
        Generate and return a cryptographically-secure short random string
        of the specified length.
        """
        if length is None:
            length = self._length

        random_num = int(binascii.b2a_hex(os.urandom(length)), 16)
        return int_to_string(random_num, self._alphabet, padding=length)[:length]

    def get_alphabet(self):
        """Return the current alphabet used for new UUIDs."""
        return "".join(self._alphabet)

    def set_alphabet(self, alphabet):
        """Set the alphabet to be used for new UUIDs."""

        # Turn the alphabet into a set and sort it to prevent duplicates
        # and ensure reproducibility.
        new_alphabet = list(sorted(set(alphabet)))
        if len(new_alphabet) > 1:
            self._alphabet = new_alphabet
            self._alpha_len = len(self._alphabet)
        else:
            raise ValueError("Alphabet with more than " "one unique symbols required.")

    def encoded_length(self, num_bytes=16):
        """
        Returns the string length of the shortened UUID.
        """
        factor = math.log(256) / math.log(self._alpha_len)
        return int(math.ceil(factor * num_bytes))


# For backwards compatibility
_global_instance = ShortUUID()
encode = _global_instance.encode
decode = _global_instance.decode
uuid = _global_instance.uuid
random = _global_instance.random
get_alphabet = _global_instance.get_alphabet
set_alphabet = _global_instance.set_alphabet

#s = ShortUUID()
#u = _uu.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}')
#print('U:{}'.format(u))
#e = s._encode(u)
#d = s._decode(e)
#es = s.encode(u)
#ds = s.decode(es)
#print('e:{}'.format(e))
#print('es:{}'.format(es))
#print('d:{}'.format(d))
#print('ds:{}'.format(ds))
#print(ds==u)
#print(d==u)
#
#U:00010203-0405-0607-0809-0a0b0c0d0e0f
#e:339nX8gnDYeGc8jU4dpCfE
#es:339nX8gnDYeGc8jU4dpCfE
#d:05bb8749-3edc-ace0-36ad-efd7b33cdeae
#ds:00010203-0405-0607-0809-0a0b0c0d0e0f
#True

#s = ShortUUID()
#u = _uu.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}')
#print(s.encode(u))
#u = _uu.UUID('{00010203-0405-0607-0000-0a0b0c0d0e0f}')
#print(s.encode(u))
#332uXNfuFYCm4NndbGxiVD
#332uXNfuFYC43sNZmnNTUc


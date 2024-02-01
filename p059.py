"""
XOR Decryption

Each character on a computer is assigned a unique code and the preferred standard is ASCII (American Standard Code for Information Interchange). For example, uppercase A = 65, asterisk (*) = 42, and lowercase k = 107.

A modern encryption method is to take a text file, convert the bytes to ASCII, then XOR each byte with a given value, taken from a secret key. The advantage with the XOR function is that using the same encryption key on the cipher text, restores the plain text; for example, 65 XOR 42 = 107, then 107 XOR 42 = 65.

For unbreakable encryption, the key is the same length as the plain text message, and the key is made up of random bytes. The user would keep the encrypted message and the encryption key in different locations, and without both "halves", it is impossible to decrypt the message.

Unfortunately, this method is impractical for most users, so the modified method is to use a password as a key. If the password is shorter than the message, which is likely, the key is repeated cyclically throughout the message. The balance for this method is using a sufficiently long password key for security, but short enough to be memorable.

Your task has been made easy, as the encryption key consists of three lower case characters. Using data/p59_cipher.txt, a file containing the encrypted ASCII codes, and the knowledge that the plain text must contain common English words, decrypt the message and find the sum of the ASCII values in the original text.
"""
from collections import Counter
from functools import lru_cache
from itertools import cycle, product, starmap
from string import ascii_lowercase

from lib.common import data, elapsed


# Highest frequency English-language characters, with space and punctuation included
eng_freq_chars = set(' etaoinsr,.')

# A glossary of common English words for testing decryption quality
glossary = set((
    'a', 'an', 'the', 'is', 'was', 'has', 'have', 'and', 'of', 'from',
    'i', 'me', 'you', 'he', 'she', 'them', 'it', 'this', 'that', 'these', 'those',
    'my', 'mine', 'your', 'yours', 'his', 'him', 'hers', 'her', 'their', 'they',
    'who', 'what', 'when', 'where', 'why', 'how',
))

# Retrieve encrypted message
fpath = data("p59_cipher.txt")
encrypted = None

with open(fpath) as fh:
    encrypted = fh.read().split(',')


# Encryption functions for testing
def encrypt_char(ecrypted_ord, key):
    return str(ord(ecrypted_ord) ^ ord(key))


def encrypt(msg, pw):
    return list(starmap(encrypt_char, zip(msg, cycle(pw))))


# Decryption functions for solution
@lru_cache(maxsize=None)
def decrypt_char(ecrypted_ord, key):
    decrypted_ord = int(ecrypted_ord) ^ key
    return chr(decrypted_ord)


def decrypt(msg, pw):
    if isinstance(pw, str):
        pw = map(ord, pw)

    return ''.join(starmap(decrypt_char, zip(msg, cycle(pw))))


# Crack by generating all possible passwords and comparing frequency of common words
def passwords(length=3, valid_chars=ascii_lowercase):
    """Generate passwords of the given length from characters in valid_chars."""
    ord_chars = map(ord, valid_chars)
    for pw in product(ord_chars, repeat=length):
        yield pw


def crack_by_word_freq(msg, glossary=glossary):
    """Return best candidate decrypted msg based on frequency of glossary terms."""
    best_pw = None
    best_msg = None
    rating = 0

    found = 0

    i = 0
    for pw in passwords():
        i += 1
        res = decrypt(msg, pw)
        words = res.split()

        counts = Counter(word.lower() for word in words if word in glossary)

        if len(counts) < 2:
            # Only found 1 word in this test
            continue
        else:
            this_rating = sum(counts.values())
            if this_rating > rating:
                rating = this_rating
                best_msg = res
                best_pw = list(map(chr, pw))
                found += 1

    print(f"Tested {i} passwords and found {found} possible matches")
    print(f"\nBest match (pw: {''.join(best_pw)}): {best_msg}")

    return best_msg


# Crack by comparing character frequency with most common English characters
# This is significantly faster than the above method using random passowrds and word frequency
def partition_msg(msg, size):
    """Return n lists partitioning msg into every nth element, for n=:size:."""
    partitions = list()
    actual_count = min(size, len(msg))

    for i in range(actual_count):
        partitions.append(msg[i::size])

    if actual_count < size:
        # Pad the list of partitions, since the msg was smaller than the requested size
        partitions.extend([[]] * size - actual_count)

    return partitions


def crack_partition_key(msg_partition, valid_chars=ascii_lowercase):
    """Return 3-tuple of ASCII characters that can be used to decrypt this partition, sorted by confidence."""
    # Dict for tracking score of each possible decryption key
    key_score = dict()

    # Set score based on how many times frequent characters appear in the decrypted string
    for a in valid_chars:
        msg_char_by_freq = Counter(decrypt(msg_partition, a).lower())
        key_score[a] = sum(v for k, v in msg_char_by_freq.items() if k in eng_freq_chars)

    # Get top 3
    best = sorted(key_score, key=key_score.__getitem__, reverse=True)[:3]

    padding = 3 - len(best)
    if padding:
        best.extend([None] * padding)

    return tuple(best)


def crack_by_char_freq(msg, pw_len=3):
    """Return best candidate decrypted msg based on frequency of English characters."""
    pw = ''
    all_keys = []
    for part in partition_msg(msg, pw_len):
        if part:
            part_keys = crack_partition_key(part)
            all_keys.append(part_keys[:2])
            pw += part_keys[0]

    decrypted_msg = decrypt(msg, pw)

    print(f"Highest confidence password: '{pw}'")
    print(f"Possible alternates: {list(map(lambda x: ''.join(x), list(product(*all_keys))[1:]))}")
    print("\nMessage:")
    print('\t', decrypted_msg)

    return decrypted_msg


print(f"\nAscii ord total: {sum(map(ord, crack_by_char_freq(encrypted)))}")
elapsed()

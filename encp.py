# import rsa
# def generateKeys():
#     (publicKey, privateKey) = rsa.newkeys(512)
#     with open('keys/publcKey.pem', 'wb') as p:
#         p.write(publicKey.save_pkcs1('PEM'))
#     with open('keys/privateKey.pem', 'wb') as p:
#         p.write(privateKey.save_pkcs1('PEM'))
#
# def loadKeys():
#     with open('keys/publcKey.pem', 'rb') as p:
#         publicKey = rsa.PublicKey.load_pkcs1(p.read())
#     with open('keys/privateKey.pem', 'rb') as p:
#         privateKey = rsa.PrivateKey.load_pkcs1(p.read())
#     return privateKey, publicKey
#
# def encrypt(message, key):
#     return rsa.encrypt(message.encode('ascii'), key)
#
# def decrypt(ciphertext, key):
#     try:
#         return rsa.decrypt(ciphertext, key).decode('ascii')
#     except:
#         return False
#
# def sign(message, key):
#     return rsa.sign(message.encode('ascii'), key, 'SHA-1')
#
# def verify(message, signature, key):
#     try:
#         return rsa.verify(message.encode('ascii'), signature, key,) == 'SHA-1'
#     except:
#         return False
#
# generateKeys()
# publicKey, privateKey =loadKeys()
# message = input('Write your message here:')
# ciphertext = encrypt(message, publicKey)
# signature = sign(message, privateKey)
# text = decrypt(ciphertext, privateKey)
# print(f'Cipher text: {ciphertext}')
# # print(f'Signature: {signature}')
# # if text:
# #     print(f'Message text: {text}')
# # else:
# #     print(f'Unable to decrypt the message.')
# # if verify(text, signature, publicKey):
# #     print('Successfully verified signature')
# # else:
# #     print('The message signature could not be verified')
from math import sqrt
#required for the sqrt() function, if you want to avoid doing **0.5
import random
#required for randrange
from random import randint as rand

#just to use the well known keyword rand() from C++


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return -1


def isprime(n):
    if n < 2:
        return False
    elif n == 2:
        return True
    else:
        for i in range(2, int(sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
    return True


#initial two random numbers p,q
p = rand(1, 1000)
q = rand(1, 1000)


def generate_keypair(p, q, keysize):
    # keysize is the bit length of n so it must be in range(nMin,nMax+1).
    # << is bitwise operator
    # x << y is same as multiplying x by 2**y
    # i am doing this so that p and q values have similar bit-length.
    # this will generate an n value that's hard to factorize into p and q.

    nMin = 1 << (keysize - 1)
    nMax = (1 << keysize) - 1
    primes = [2]
    # we choose two prime numbers in range(start, stop) so that the difference of bit lengths is at most 2.
    start = 1 << (keysize // 2 - 1)
    stop = 1 << (keysize // 2 + 1)

    if start >= stop:
        return []

    for i in range(3, stop + 1, 2):
        for p in primes:
            if i % p == 0:
                break
        else:
            primes.append(i)

    while (primes and primes[0] < start):
        del primes[0]

    #choosing p and q from the generated prime numbers.
    while primes:
        p = random.choice(primes)
        primes.remove(p)
        q_values = [q for q in primes if nMin <= p * q <= nMax]
        if q_values:
            q = random.choice(q_values)
            break
    print(p, q)
    n = p * q
    phi = (p - 1) * (q - 1)

    #generate public key 1<e<phi(n)
    e = random.randrange(1, phi)
    g = gcd(e, phi)

    while True:
        #as long as gcd(1,phi(n)) is not 1, keep generating e
        e = random.randrange(1, phi)
        g = gcd(e, phi)
        #generate private key
        d = mod_inverse(e, phi)
        if g == 1 and e != d:
            break

    #public key (e,n)
    #private key (d,n)

    return ((e, n), (d, n))


def encrypt(msg_plaintext, package):
    e, n = package
    msg_ciphertext = [pow(ord(c), e, n) for c in msg_plaintext]
    return msg_ciphertext


def decrypt(msg_ciphertext, package):
    d, n = package
    msg_plaintext = [chr(pow(c, d, n)) for c in msg_ciphertext]
    return (''.join(msg_plaintext))


#-------------------------------------------------------------
#driver program
if __name__ == "__main__":
    bit_length = int(input("Enter bit_length: "))
    print("Running RSA...")
    print("Generating public/private keypair...")
    public, private = generate_keypair(
        p, q, 2**bit_length)  # 8 is the keysize (bit-length) value.
    print("Public Key: ", public)
    print("Private Key: ", private)
    msg = input("Write msg: ")
    print([ord(c) for c in msg])
    encrypted_msg = encrypt(msg, public)
    print("Encrypted msg: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypted msg: ")
    print(decrypt(encrypted_msg, private))


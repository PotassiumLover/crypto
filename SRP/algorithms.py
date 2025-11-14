from secrets import randbelow

def egcd(a, b):
    if a < 0 or b < 0:
        a0, b0 = abs(a), abs(b)
    else:
        a0, b0 = a, b

    old_r, r = a0, b0
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    x = old_s if a >= 0 else -old_s
    y = old_t if b >= 0 else -old_t
    return old_r, x, y

def mod_pow(base, exponent, modulus):
    base = base % modulus
    result = 1 % modulus
    e = exponent

    while e > 0:
        if e & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        e >>= 1

    return result

def try_composite(a, s, d, n):
    x = mod_pow(a, d, n)
    if x == 1 or x == n - 1:
        return False
    for muda in range(s - 1):
        x = (x * x) % n
        if x == n - 1:
            return False
    return True 

def is_probable_prime(n, rounds = 40):
    if n < 2:
        return False

    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if n == p:
            return True
        if n % p == 0:
            return False
        
    d = n - 1
    s = 0
    while (d & 1) == 0:
        d >>= 1
        s += 1

    for muda in range(rounds):
        a = 2 + randbelow(n - 3)
        if try_composite(a, s, d, n):
            return False

    return True

import secrets
import hashlib
from algorithms import mod_pow  

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, "big")


def bytes_to_int(b):
    return int.from_bytes(b, "big")


def H(data):
    return hashlib.sha256(data).digest()

if __name__ == "__main__":

    password    = "sexagenaries" 
    salt    = "1afd3889" 
    b   = 210338911319114893987312568536431345694612602486711856748908179851921775565770751564259107620620447672474324857277380437984263916514710728346474029318083491758579875686516530361983795552548666442825539264905019369189657938066504664613524802883657136015759485413359985154720693171712272306608646322399218744517
    username    = "tnitzsch"

    p = 233000556327543348946447470779219175150430130236907257523476085501968599658761371268535640963004707302492862642690597042148035540759198167263992070601617519279204228564031769469422146187139698860509698350226540759311033166697559129871348428777658832731699421786638279199926610332604408923157248859637890960407
    g = 5
    a = 9883325405337806983858802322888532651133652057857442599968375665104905230690326597991782102288968556438351243806531918829793367496074666051607472586942565
    if a is None:
        a = secrets.randbits(512)
        print("A: ", a)

    # Step 2

    A = mod_pow(g, a, p)
    print("DH Key: ", A)
    
    A_bytes = int_to_bytes(A)

    salt = int(salt, 16)
    salt_bytes = int_to_bytes(salt)

    # Step 3

    password_bytes = password.encode("ascii")

    x_bytes = salt_bytes + password_bytes
    for _ in range(1000):
        x_bytes = H(x_bytes)
    x = bytes_to_int(x_bytes)

    print("Hashed password:", x)

    p_bytes = int_to_bytes(p)
    g_bytes = int_to_bytes(g)
    k = bytes_to_int(H(p_bytes + g_bytes))

    gx = mod_pow(g, x, p)

    public_b = (b - k * gx) % p
    B_bytes = int_to_bytes(public_b)

    u = bytes_to_int(H(A_bytes + B_bytes))

    print("k:", k)
    print("g^b:", public_b)
    print("u:", u)

    exponent = a + u * x
    shared_key = mod_pow(public_b, exponent, p)
    shared_key_bytes = int_to_bytes(shared_key)

    print("Shared key:", shared_key)
    # Step 4

    Hp = H(int_to_bytes(p))
    Hg = H(int_to_bytes(g))
    Huser = H(username.encode("ascii"))

    p1 = bytes(a ^ b for a, b in zip(Hp, Hg))
    p2 = Huser
    p3 = salt_bytes
    p4 = A_bytes
    p5 = B_bytes
    p6 = shared_key_bytes

    m1 = H(p1 + p2 + p3 + p4 + p5 + p6)

    # Step 5

    m2 = H(p4 + m1 + p6)

    print("M1:", m1.hex())
    print("M2:", m2.hex())
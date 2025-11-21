import hashlib
import random

prev_hash = "000000664779bc3c77fe23ab28d9660d3995b2717adc1d37209b9ea359043364"

difficulty_bits = 24
quote = "You can have premature generalization as well as premature optimization. -- Bjarne Stroustrup"
prev_hash = bytes.fromhex(prev_hash)
quote_bytes = quote.encode("ascii")

#nonce = random.getrandbits(64)
nonce = 8114609493251522667

while True:
    
    length = (nonce.bit_length() + 7) // 8
    nonce_bytes = nonce.to_bytes(length, byteorder="big")

    data = prev_hash + nonce_bytes + quote_bytes
    block_hash_bytes = hashlib.sha256(data).digest()

    hash_int = int.from_bytes(block_hash_bytes, byteorder="big")

    if difficulty_bits <= 0:
        meets_difficulty = True
    else:
        if hash_int == 0:
            leading_zero_bits = 256
        else:
            leading_zero_bits = 256 - hash_int.bit_length()
        meets_difficulty = (leading_zero_bits >= difficulty_bits)

    if meets_difficulty:
        print("Nonce:", nonce)
        print("Hash: ", block_hash_bytes.hex())
        break

    nonce += 1



"""
SHA-256 (Secure Hash Algorithm 256-bit) Implementation
This implementation follows the NIST specification for SHA-256.
SHA-256 is a cryptographic hash function that produces a 256-bit (32-byte) hash value.
It's part of the SHA-2 family of hash functions.
"""

# Step 1: Define constants (K)
# These constants represent the first 32 bits of the fractional parts of the cube roots
# of the first 64 prime numbers (2 to 311). They are used in the compression function
# to add non-linearity to the algorithm.
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

# Step 2: Define initial hash values (H)
# These values are the first 32 bits of the fractional parts of the square roots
# of the first 8 prime numbers (2 to 19). They serve as the initial hash state.
H = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

# Step 3: Define helper functions for bitwise operations
def right_rotate(value, bits):
    """
    Perform a circular right rotation on a 32-bit integer.
    This is a key operation in SHA-256 that helps create the avalanche effect,
    where a small change in input causes a large change in the output.
    
    Args:
        value: The 32-bit integer to rotate
        bits: Number of positions to rotate right
    Returns:
        The rotated value as a 32-bit integer
    """
    return ((value >> bits) | (value << (32 - bits))) & 0xFFFFFFFF

def sha256(message):
    """
    Compute the SHA-256 hash of a given message.
    
    Args:
        message: Input message (string or bytes)
    Returns:
        64-character hexadecimal string representing the hash
    """
    # Step 4: Preprocessing (Padding)
    # The message must be padded to ensure its length is a multiple of 512 bits
    # This is crucial for the block-based nature of the algorithm
    if isinstance(message, str):
        message = message.encode()
    
    # Store the original message length for later use
    original_bit_length = len(message) * 8
    
    # Append the '1' bit (as a byte 0x80) to mark the end of the message
    message += b'\x80'
    
    # Add zero padding until the message length is 448 mod 512 bits
    # This leaves room for the 64-bit length at the end
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    
    # Append the original message length as a 64-bit big-endian integer
    message += original_bit_length.to_bytes(8, byteorder='big')
    
    # Step 5: Process the message in 512-bit chunks
    # Break the padded message into 512-bit (64-byte) chunks
    chunks = [message[i:i + 64] for i in range(0, len(message), 64)]
    
    for chunk in chunks:
        # Convert chunk into 16 32-bit big-endian words
        w = [int.from_bytes(chunk[i:i + 4], byteorder='big') for i in range(0, 64, 4)]
        
        # Extend 16 words into 64 words through message scheduling
        # This creates additional words through a deterministic process
        for i in range(16, 64):
            # Create new words using bitwise operations for diffusion
            s0 = right_rotate(w[i - 15], 7) ^ right_rotate(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = right_rotate(w[i - 2], 17) ^ right_rotate(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w.append((w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFF)
        
        # Initialize working variables with current hash state
        a, b, c, d, e, f, g, h = H
        
        # Main compression function - Process each word
        # This is the heart of SHA-256 where the mixing of bits occurs
        for i in range(64):
            # Two temporary words are computed in each round
            # S1 calculation: mix of rotations of variable 'e'
            S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
            # Choice function: choose bits from f or g based on e
            ch = (e & f) ^ (~e & g)
            temp1 = (h + S1 + ch + K[i] + w[i]) & 0xFFFFFFFF
            
            # S0 calculation: mix of rotations of variable 'a'
            S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
            # Majority function: take majority of bits from a, b, and c
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xFFFFFFFF
            
            # Update working variables
            # This rotation ensures each variable influences multiple others
            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF
        
        # Update hash state with compressed chunk
        # Add the compressed chunk to the current hash value (modulo 2^32)
        H[0] = (H[0] + a) & 0xFFFFFFFF
        H[1] = (H[1] + b) & 0xFFFFFFFF
        H[2] = (H[2] + c) & 0xFFFFFFFF
        H[3] = (H[3] + d) & 0xFFFFFFFF
        H[4] = (H[4] + e) & 0xFFFFFFFF
        H[5] = (H[5] + f) & 0xFFFFFFFF
        H[6] = (H[6] + g) & 0xFFFFFFFF
        H[7] = (H[7] + h) & 0xFFFFFFFF
    
    # Step 6: Produce the final hash
    # Concatenate the final hash values into a 64-character hexadecimal string
    return ''.join(f'{value:08x}' for value in H)

# Example usage showing how to hash a simple message
message = "hello world"
hash_result = sha256(message)
print(f"SHA-256 hash of '{message}': {hash_result}")

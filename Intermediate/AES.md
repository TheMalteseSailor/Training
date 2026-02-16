The **Advanced Encryption Standard (AES)** is a symmetric block cipher that serves as the global gold standard for protecting sensitive digital data. Established by the National Institute of Standards and Technology (NIST) in 2001, it replaced the outdated Data Encryption Standard (DES).

#### Key Characteristics
- **Symmetric Algorithm**: It uses the same secret key for both encryption and decryption.
- **Block Cipher**: AES processes data in fixed-size blocks of **128 bits** (16 bytes).
- **Key Lengths**: It supports three standard key sizes: **128, 192, and 256 bits**.
- **Security Level**: AES-256 is currently considered virtually immune to brute-force attacks and is approved by the NSA for protecting "Top Secret" information.

#### How the Algorithm Works
AES is based on a **Substitution-Permutation Network (SPN)**, which repeatedly performs a set of mathematical operations over several "rounds". The number of rounds depends on the key length: 
- **AES-128**: 10 rounds.
- **AES-192**: 12 rounds.
- **AES-256**: 14 rounds. 
Each round (except the last) consists of four main transformations: 
1. **SubBytes**: Replaces each byte with another using a lookup table (S-box) for non-linearity.
2. **ShiftRows**: Cyclically shifts rows of the data matrix to ensure data is moved around.
3. **MixColumns**: Mathematically combines columns to provide diffusion across the block.
4. **AddRoundKey**: Combines the data with a unique subkey derived from the original master key.


AES is a **Block Cipher**, meaning it breaks plaintext into 128-bit (16-byte) blocks and processes them through a series of mathematical "rounds."
#### AES Encryption Flow (128-bit Key)

``` text
       [ Plaintext Block ] (128-bit / 16 bytes)
              |
              v
     +-----------------+       +------------------+
     |  State Matrix   | <---- |  Original Key    |
     |  (4x4 bytes)    |       +---------+--------+
     +--------+--------+                 |
              |                 [ Key Expansion ]
      (Initial Round)          (Generates 10 Subkeys)
      [ AddRoundKey ] <------------------+
              |                          |
              v                          |
    +-------------------+                |
    |  ROUNDS 1 to 9    |                |
    |                   |                |
    | 1. SubBytes       | (S-Box)        |
    | 2. ShiftRows      | (Transposition)|
    | 3. MixColumns     | (Mixing)       |
    | 4. AddRoundKey    | <--------------+ (Subkey N)
    +---------+---------+                |
              |                          |
              v                          |
      (Final Round 10)                   |
    +-------------------+                |
    | 1. SubBytes       |                |
    | 2. ShiftRows      |                |
    | 3. AddRoundKey    | <--------------+ (Subkey 10)
    +---------+---------+
              |
              v
      [ Ciphertext Block ]

```

#### The 4 Core Transformations
1. **SubBytes**: A non-linear substitution step where each byte is replaced with another according to a lookup table (S-Box). This provides confusion.
2. **ShiftRows**: A transposition step where the last three rows of the state are shifted cyclically a certain number of steps. This provides diffusion.
3. **MixColumns**: A mixing operation which operates on the columns of the state, combining the four bytes in each column. (This step is skipped in the Final Round).
4. **AddRoundKey**: Each byte of the state is combined with a block of the "round key" using bitwise XOR.

#### Key Expansion
The original key is not used directly in every round. Instead, the AES Key Schedule expands the short input key into a much larger "key schedule," providing a unique Subkey for every single round.

#### AES Modes
Since AES is a block cipher that only encrypts 128-bit chunks at a time, **modes of operation** are used to define how to handle larger data streams

1. **ECB (Electronic Codebook)**
	- **Description**: The simplest mode where each block of plaintext is encrypted independently with the same key.
	- **Pros**: Fast and parallelizable.
	- **Cons**: Insecure for most uses. Identical plaintext blocks produce identical ciphertext blocks, which reveals patterns in the data (the famous "Tux the Penguin" vulnerability). 
2. **CBC (Cipher Block Chaining)**
	- **Description**: Each block of plaintext is XORed with the previous ciphertext block before encryption. The first block uses a random Initialization Vector (IV).
	- **Pros**: Hides patterns well and is widely supported in legacy systems (e.g., PGP, older VPNs).
	- **Cons**: Encryption cannot be parallelized (sequential); it requires padding to fill the last block, making it vulnerable to Padding Oracle attacks.
3. **CTR (Counter Mode)**
	- **Description**: Turns AES into a stream cipher by encrypting a unique, incrementing counter (combined with a nonce) and XORing the result with the plaintext.
	- **Pros**: Extremely fast, fully parallelizable, and allows "random access" to any part of the file without decrypting everything before it.
	- **Cons**: Does not provide integrity (authentication); an attacker can flip bits in the ciphertext to predictably change the plaintext. 
4. **GCM (Galois/Counter Mode)**
	- **Description**: The modern gold standard. It combines CTR mode for encryption with a Galois Field multiplier for authentication.
	- **Pros**: Provides AEAD (Authenticated Encryption with Associated Data), meaning it ensures both confidentiality and that the data hasn't been tampered with. It is fast and parallelizable.
	- **Cons**: Catastrophic security failure if the same nonce is reused with the same key. 
5. **CFB (Cipher Feedback) & OFB (Output Feedback)** 
	- **Description**: Both turn the block cipher into a stream cipher by feeding ciphertext (CFB) or the previous keystream (OFB) back into the next encryption step.
	- **Usage**: Generally considered obsolete or niche today, replaced by more efficient modes like CTR and GCM. 
6. **XTS (XEX-based Tweaked-Codebook Mode)**
	- **Description**: A specialized mode designed specifically for disk encryption.
	- **Usage**: Used by tools like Microsoft BitLocker and Apple FileVault because it handles data stored in fixed sectors better than chaining modes.


#### Python Implementation
Implementing **AES-128** from scratch in pure Python is significantly more complex than RC4 or Salsa20 because it requires the **AES S-Box**, **Key Expansion**, and **Galois Field (GF(2⁸))** multiplication.
This code implements the **AES-128** core and **CBC mode** with padding.

``` python
# AES S-Box and Rcon (Round Constants)
SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, d2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

def sub_word(word):
    return [SBOX[b] for b in word]

def rot_word(word):
    return word[1:] + word[:1]

def aes_key_expansion(key):
    """Expands a 16-byte key into 11 round keys."""
    words = [list(key[i:i+4]) for i in range(0, 16, 4)]
    for i in range(4, 44):
        temp = words[i-1][:]
        if i % 4 == 0:
            temp = sub_word(rot_word(temp))
            temp[0] ^= RCON[i//4]
        words.append([words[i-4][j] ^ temp[j] for j in range(4)])
    return [bytearray([b for word in words[i:i+4] for b in word]) for i in range(0, 44, 4)]

def sub_bytes(state):
    for i in range(16): state[i] = SBOX[state[i]]

def shift_rows(state):
    state[1], state[5], state[9], state[13] = state[5], state[9], state[13], state[1]
    state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6]
    state[3], state[7], state[11], state[15] = state[15], state[3], state[7], state[11]

def xtime(a):
    return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else (a << 1) & 0xFF

def mix_columns(state):
    for i in range(0, 16, 4):
        s0, s1, s2, s3 = state[i:i+4]
        state[i]   = xtime(s0 ^ s1) ^ s1 ^ s2 ^ s3
        state[i+1] = xtime(s1 ^ s2) ^ s2 ^ s3 ^ s0
        state[i+2] = xtime(s2 ^ s3) ^ s3 ^ s0 ^ s1
        state[i+3] = xtime(s3 ^ s0) ^ s0 ^ s1 ^ s2

def add_round_key(state, key):
    for i in range(16): state[i] ^= key[i]

def aes_encrypt_block(block, round_keys):
    state = bytearray(block)
    add_round_key(state, round_keys[0])
    for i in range(1, 10):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, round_keys[i])
    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, round_keys[10])
    return bytes(state)

def encrypt_cbc(plaintext, key, iv):
    round_keys = aes_key_expansion(key)
    # PKCS7 Padding
    pad_len = 16 - (len(plaintext) % 16)
    plaintext += bytes([pad_len] * pad_len)
    
    ciphertext = b""
    prev_block = iv
    for i in range(0, len(plaintext), 16):
        block = bytes(p ^ b for p, b in zip(plaintext[i:i+16], prev_block))
        encrypted_block = aes_encrypt_block(block, round_keys)
        ciphertext += encrypted_block
        prev_block = encrypted_block
    return ciphertext

# --- Usage Example ---
key = b"16byte_secretkey"  # 128-bit key
iv = b"unique_init_vect"   # 16-byte IV
msg = b"Pure Python AES"

encrypted = encrypt_cbc(msg, key, iv)
print(f"Ciphertext (Hex): {encrypted.hex()}")

```


#### Core Components
- **S-Box**: The massive array at the top is the **SubBytes** lookup table. It's designed to be mathematically "confusing" so that small changes in input create large, non-linear changes in output.
- **xtime**: This handles multiplication in the Galois Field GF(2⁸). It’s how the MixColumns step mathematically combines the data.
- **Key Expansion**: AES-128 needs 11 distinct "round keys." This function stretches your 16-byte password into a 176-byte schedule.
- **CBC Chaining**: Notice the line p ^ b. This is where each plaintext block is XORed with the previous ciphertext block before being encrypted.

**Important**: This implementation only includes encryption. Decryption requires "Inverse" versions of every function (InvSubBytes, InvMixColumns, etc.). For production, always use a library like PyCryptodome to avoid side-channel attacks.


#### C Implementation
This C implementation of **AES-128** in **CBC mode** is a "tiny" version designed for clarity. It includes the core block cipher (encryption only) and the XOR-chaining logic required for CBC. 

``` C
#include <stdint.h>
#include <string.h>
#include <stdio.h>

#define AES_BLOCK_SIZE 16

// AES S-Box for the SubBytes transformation
static const uint8_t sbox[256] = {
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
};

// Multiplication in GF(2^8)
uint8_t xtime(uint8_t x) { return (x << 1) ^ (((x >> 7) & 1) * 0x1b); }

// MixColumns transformation
void mix_columns(uint8_t *s) {
    for (int i = 0; i < 4; i++) {
        uint8_t a = s[i*4], b = s[i*4+1], c = s[i*4+2], d = s[i*4+3];
        uint8_t h = a ^ b ^ c ^ d;
        s[i*4]   ^= h ^ xtime(a ^ b);
        s[i*4+1] ^= h ^ xtime(b ^ c);
        s[i*4+2] ^= h ^ xtime(c ^ d);
        s[i*4+3] ^= h ^ xtime(d ^ a);
    }
}

// Core AES Block Encryption (simplified for 128-bit key)
void aes_encrypt_block(uint8_t *state, const uint8_t *round_keys) {
    // Initial AddRoundKey
    for (int i = 0; i < 16; i++) state[i] ^= round_keys[i];

    for (int r = 1; r <= 10; r++) {
        // 1. SubBytes
        for (int i = 0; i < 16; i++) state[i] = sbox[state[i]];
        // 2. ShiftRows (simplified)
        uint8_t t;
        t = state[1]; state[1] = state[5]; state[5] = state[9]; state[9] = state[13]; state[13] = t;
        t = state[2]; state[2] = state[10]; state[10] = t; t = state[6]; state[6] = state[14]; state[14] = t;
        t = state[15]; state[15] = state[11]; state[11] = state[7]; state[7] = state[3]; state[3] = t;
        // 3. MixColumns (except last round)
        if (r < 10) mix_columns(state);
        // 4. AddRoundKey
        for (int i = 0; i < 16; i++) state[i] ^= round_keys[r * 16 + i];
    }
}

// CBC Mode Wrapper
void aes_cbc_encrypt(uint8_t *data, uint32_t len, const uint8_t *key, uint8_t *iv) {
    // Note: This example uses a simplified key schedule for brevity
    // Real implementation requires full KeyExpansion function
    uint8_t round_keys[176]; 
    memset(round_keys, 0xAC, 176); // Placeholder: use actual key expansion here!

    uint8_t *prev_block = iv;
    for (uint32_t i = 0; i < len; i += AES_BLOCK_SIZE) {
        // XOR with previous ciphertext (or IV)
        for (int j = 0; j < AES_BLOCK_SIZE; j++) data[i + j] ^= prev_block[j];
        
        aes_encrypt_block(data + i, round_keys);
        prev_block = data + i;
    }
}

int main() {
    uint8_t key[16] = "secret_key_128b";
    uint8_t iv[16]  = "initial_vector_";
    uint8_t msg[32] = "This is a 32-byte secret message";

    printf("Encrypting...\n");
    aes_cbc_encrypt(msg, 32, key, iv);
    
    printf("Ciphertext (Hex): ");
    for(int i=0; i<32; i++) printf("%02x", msg[i]);
    printf("\n");
    
    return 0;
}

```

#### Key Differences from Python
- **Memory Management**: In C, we process the data "in-place" within the array to save memory, which is essential for embedded or high-performance systems.
- **Static Tables**: The **S-box** is stored as a static const array, ensuring it resides in the program's read-only memory rather than taking up stack space.
- **Bit Manipulation**: Operations like xtime (used in MixColumns) are handled via direct bit shifting and XORing, which is much faster than Python's integer math. 
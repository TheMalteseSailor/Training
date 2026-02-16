# Salsa20
**Salsa20** is a high-speed symmetric stream cipher designed by Daniel J. Bernstein in 2005. It was a finalist in the European eSTREAM project, a competition created to find modern, efficient alternatives to older ciphers like RC4. 

### How Salsa20 Works
Unlike RC4, which uses a shifting state, Salsa20 is built on a **pseudorandom function** that maps a key, a nonce, and a counter to a block of the keystream. 
- **ARX Design**: It relies on three simple operations: 32-bit **A**ddition, bitwise **R**otation, and bitwise **X**OR. This avoids the use of "S-boxes" or lookup tables, making it resistant to timing attacks.
- **Internal State**: The cipher organizes a 256-bit key, a 64-bit nonce, a 64-bit counter, and constant strings into a **4x4 matrix** (16 32-bit words).
- **Keystream Generation**: It repeatedly applies a "quarter-round" function to the matrix to scramble the data. The default version, Salsa20/20, performs 20 rounds of this scrambling.
- **Encryption**: The resulting 64-byte block of "random" data is then XORed with 64 bytes of your message to produce the ciphertext.

#### Key Characteristics
- **Random Access**: A major advantage over RC4 is that you can jump to any part of a large file (e.g., at the 1GB mark) and begin decrypting instantly by setting the counter to the correct block number.
- **Security**: Salsa20 provides high confidentiality and has no known practical attacks that break its full 20 rounds. However, it does not provide data integrity; if an attacker flips a bit in the ciphertext, it will predictably change the decrypted message.
- **Successor**: Bernstein later released ChaCha20 in 2008, which is a variant of Salsa20 designed to increase security (diffusion) and performance. 

#### Common Applications
- **Messaging**: Used in apps like **Viber** and **Discord** for fast communication.
- **Protocols**: Implemented in modern versions of **TLS/SSL** and **VPN** services.
- **Storage**: Often found in disk encryption and ransomware (such as Petya) due to its speed. 

**Critical Warning**: Never reuse the same nonce with the same key. Doing so allows an attacker to easily recover the original message.

``` text
      [ Input Parameters ]
     /        |         \
 [Key]     [Nonce]    [Counter]    [Constants]
 (256b)     (64b)       (64b)        (128b)
    |         |           |            |
    +---------+-----------+------------+
              |
      1. [ MATRIX INITIALIZATION ]
      +-----------------------+
      | C0  | K0  | K1  | K2  |  (C = Constants)
      | K3  | C1  | N0  | N1  |  (K = Key)
      | T0  | T1  | C2  | K4  |  (N = Nonce)
      | K5  | K6  | K7  | C3  |  (T = Counter)
      +-----------+-----------+
                  |
      2. [ THE 20 ROUNDS (Double-Rounds) ]
      +-----------v-----------+
      |  Column Round (Odd)   |  <-- "Quarter-Round" on
      |  Row Round    (Even)  |      Matrix columns/rows
      +-----------+-----------+      using ARX operations
                  |
      3. [ FINAL ADDITION ]
      |  (Scrambled Matrix)   |
      |          +            |
      |  (Original Matrix)    |
      +-----------+-----------+
                  |
                  v
       4. [ 64-BYTE KEYSTREAM ]
                  |
          +-------v-------+
          | XOR Operation | <--- [ Plaintext ]
          +-------+-------+
                  |
                  v
           [ Ciphertext ]

```

#### Key Differences from the RC4 Flow
- **State-Based vs. Counter-Based**: Unlike RC4, which relies on a mutating S-box, Salsa20 is a **functional cipher**. It uses a fixed input matrix and a Counter to generate blocks. To decrypt the 10th block, you simply set the counter to 10.
- **ARX Operations**: The core "shuffling" happens via Addition, Rotation, and XOR on 32-bit words rather than swapping bytes in an array.
- **Input Constants**: Salsa20 uses the string "expand 32-byte k" (the constants C0-C3) to ensure that the key and nonce are properly distributed across the matrix, preventing internal patterns that attackers could exploit.


#### Python Implementation

This implementation follows the Salsa20 specification and includes the core **Quarter-Round** function and the **20-round matrix** transformation.

``` python
import struct

def rotate_left(v, c):
    """32-bit bitwise rotation."""
    return ((v << c) & 0xffffffff) | (v >> (32 - c))

def quarter_round(y, a, b, c, d):
    """The core ARX (Add, Rotate, XOR) operation."""
    y[b] ^= rotate_left((y[a] + y[d]) & 0xffffffff, 7)
    y[c] ^= rotate_left((y[b] + y[a]) & 0xffffffff, 9)
    y[d] ^= rotate_left((y[c] + y[b]) & 0xffffffff, 13)
    y[a] ^= rotate_left((y[d] + y[c]) & 0xffffffff, 18)

def salsa20_block(key, nonce, counter):
    """Transforms a 64-byte block using 20 rounds of scrambling."""
    # Constants for "expand 32-byte k"
    constants = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
    
    # 1. Matrix Initialization (16 32-bit words)
    # Mapping: Constants, Key (8 words), Nonce (2 words), Counter (2 words)
    state = [0] * 16
    state[0], state[5], state[10], state[15] = constants
    state[1:5] = struct.unpack('<4I', key[:16])
    state[11:15] = struct.unpack('<4I', key[16:])
    state[6:8] = struct.unpack('<2I', nonce)
    state[8:10] = struct.unpack('<2I', counter)
    
    working_state = list(state)
    
    # 2. Perform 20 Rounds (10 double-rounds)
    for _ in range(10):
        # Column rounds
        quarter_round(working_state, 0, 4, 8, 12)
        quarter_round(working_state, 5, 9, 13, 1)
        quarter_round(working_state, 10, 14, 2, 6)
        quarter_round(working_state, 15, 3, 7, 11)
        # Row rounds
        quarter_round(working_state, 0, 1, 2, 3)
        quarter_round(working_state, 5, 6, 7, 4)
        quarter_round(working_state, 10, 11, 8, 9)
        quarter_round(working_state, 15, 12, 13, 14)
        
    # 3. Final Addition & Serialization
    for i in range(16):
        working_state[i] = (working_state[i] + state[i]) & 0xffffffff
        
    return struct.pack('<16I', *working_state)

def salsa20_encrypt(key, nonce, plaintext):
    """Encrypts/Decrypts variable length plaintext."""
    res = bytearray()
    for i in range(0, len(plaintext), 64):
        # Generate a 64-byte keystream block for each counter increment
        counter = struct.pack('<Q', i // 64)
        keystream = salsa20_block(key, nonce, counter)
        
        # XOR plaintext with keystream
        block = plaintext[i:i+64]
        for p_byte, k_byte in zip(block, keystream):
            res.append(p_byte ^ k_byte)
    return bytes(res)

# --- Usage ---
my_key = b"this is a very secret 32-byte k" # 32 bytes
my_nonce = b"8byte-no"                    # 8 bytes
msg = b"Hello, this is a pure Python Salsa20 implementation!"

encrypted = salsa20_encrypt(my_key, my_nonce, msg)
print(f"Ciphertext (Hex): {encrypted.hex()}")

decrypted = salsa20_encrypt(my_key, my_nonce, encrypted)
print(f"Decrypted: {decrypted.decode()}")

```

#### Why this is different from RC4
- **Struct Packing**: Since Salsa20 operates on 32-bit integers, we use Python's struct module to convert bytes into integers (Little-Endian) and back again.
- **The Counter**: Note that salsa20_block takes a counter. This allows the cipher to encrypt each 64-byte block independently, whereas RC4 must process all previous bytes to reach a specific point.
- **Fixed Matrix**: The internal state is always a 16-word matrix. The "security" comes from the complex **quarter_round** shuffles that make it impossible to reverse-engineer the key from the output.
- **Critical Note**: This is roughly 100x slower than a C-based library like PyCryptodome. It is perfect for learning the logic, but for production apps, use a compiled library to avoid performance bottlenecks and potential side-channel leaks.


### C Implementation
Implementing **Salsa20** in C requires manual handling of 32-bit word rotations and little-endian byte ordering. The following implementation is a standalone version that follows the standard 20-round specification.

``` C
#include <stdint.h>
#include <string.h>
#include <stdio.h>

#define ROTL32(v, n) (((v) << (n)) | ((v) >> (32 - (n))))

// 1. The Quarter-Round function: The core ARX building block
void s20_quarterround(uint32_t *a, uint32_t *b, uint32_t *c, uint32_t *d) {
    *b ^= ROTL32(*a + *d, 7);
    *c ^= ROTL32(*b + *a, 9);
    *d ^= ROTL32(*c + *b, 13);
    *a ^= ROTL32(*d + *c, 18);
}

// 2. The Core Hash function: Scrambles the 64-byte state matrix
void s20_core(uint32_t *out, const uint32_t *in) {
    uint32_t x[16];
    memcpy(x, in, sizeof(x));

    for (int i = 0; i < 10; i++) {
        // Column rounds
        s20_quarterround(&x[0], &x[4], &x[8], &x[12]);
        s20_quarterround(&x[5], &x[9], &x[13], &x[1]);
        s20_quarterround(&x[10], &x[14], &x[2], &x[6]);
        s20_quarterround(&x[15], &x[3], &x[7], &x[11]);
        // Row rounds
        s20_quarterround(&x[0], &x[1], &x[2], &x[3]);
        s20_quarterround(&x[5], &x[6], &x[7], &x[4]);
        s20_quarterround(&x[10], &x[11], &x[8], &x[9]);
        s20_quarterround(&x[15], &x[12], &x[13], &x[14]);
    }

    for (int i = 0; i < 16; i++) out[i] = x[i] + in[i];
}

// 3. Salsa20 Encryption/Decryption
// Works for any length; key must be 32 bytes, nonce must be 8 bytes.
void salsa20_crypt(const uint8_t *key, const uint8_t *nonce, uint8_t *data, uint32_t len) {
    uint32_t state[16];
    uint32_t keystream[16];
    uint8_t *key8 = (uint8_t*)keystream;
    uint32_t counter[2] = {0, 0};

    // Constants: "expand 32-byte k"
    state[0] = 0x61707865; state[5] = 0x3320646e;
    state[10] = 0x79622d32; state[15] = 0x6b206574;

    // Load Key (32 bytes)
    memcpy(&state[1], key, 16);
    memcpy(&state[11], key + 16, 16);

    // Load Nonce (8 bytes)
    memcpy(&state[6], nonce, 8);

    for (uint32_t i = 0; i < len; i += 64) {
        // Set Counter (64-bit)
        state[8] = counter[0];
        state[9] = counter[1];

        s20_core(keystream, state);

        // XOR the data with the keystream block
        uint32_t block_len = (len - i < 64) ? (len - i) : 64;
        for (uint32_t j = 0; j < block_len; j++) {
            data[i + j] ^= key8[j];
        }

        // Increment 64-bit counter
        if (++counter[0] == 0) counter[1]++;
    }
}

int main() {
    uint8_t key[32] = "this-is-a-32-byte-secret-key!!!";
    uint8_t nonce[8] = "8-bytes!";
    uint8_t message[] = "Salsa20 is fast and secure in C.";
    uint32_t len = strlen((char*)message);

    printf("Original: %s\n", message);
    salsa20_crypt(key, nonce, message, len);
    printf("Encrypted (Hex): ");
    for(int i=0; i<len; i++) printf("%02X", message[i]);
    
    salsa20_crypt(key, nonce, message, len); // Decrypt
    printf("\nDecrypted: %s\n", message);

    return 0;
}

```

#### Implementation Highlights
- **The Matrix Layout**: The state matrix is initialized with a specific pattern of constants, the key, the nonce, and the block counter.
- **Modulo 2³² Addition**: C's uint32_t naturally handles the required overflow behavior, simplifying the **Add-Rotate-XOR** operations.
- **64-Byte Blocks**: Salsa20 generates keystream in 64-byte chunks. The counter allows you to encrypt huge amounts of data (up to 2⁷⁰ bytes) without reusing the keystream.
- **Symmetry**: Like RC4, Salsa20 is its own inverse; calling the function on ciphertext with the same key and nonce returns the plaintext. 

**Security Note**: For real-world use, ensure your nonces are unique for every message to prevent keystream reuse attacks.


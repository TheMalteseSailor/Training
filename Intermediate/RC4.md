**RC4** (Rivest Cipher 4) is a **symmetric stream cipher** designed by Ron Rivest in 1987. Once the most widely used stream cipher in the world, it is renowned for its remarkable **simplicity and speed**. 

### How RC4 Works
The algorithm operates by generating a **pseudorandom keystream**—a sequence of random-looking bits—which it then combines with the original data (plaintext) using a bitwise **XOR operation**. It consists of two main phases:
- **Key Scheduling Algorithm (KSA)**: It uses a variable-length key (typically 40 to 2048 bits) to initialize and scramble a 256-byte state array.
- **Pseudo-Random Generation Algorithm (PRGA)**: It continuously permutes the state array to produce a stream of bytes. Each byte of the plaintext is XORed with a byte from this stream to create the ciphertext.

#### Key Characteristics
- **Symmetric**: The same secret key is used for both encryption and decryption.
- **Stream Cipher**: Unlike block ciphers (like AES) that process data in fixed chunks, RC4 encrypts data one byte at a time.
- **Speed & Efficiency**: Its design avoids complex mathematical operations, making it extremely fast in software and ideal for older, resource-constrained hardware.
- **Legacy Protocols**: Historically, it secured billions of connections through protocols like WEP and WPA (for Wi-Fi) and SSL/TLS (for web traffic). 

#### Current Status: Obsolete & Insecure
While popular for decades, RC4 is now considered broken and insecure due to significant cryptographic vulnerabilities. 
- **Statistical Biases**: The first few bytes of the keystream are not truly random, which can allow attackers to recover the secret key after observing enough encrypted traffic.
- **Global Deprecation**: The IETF banned RC4 in TLS in 2015. Modern browsers like Chrome, Firefox, and Edge have removed support for it.
- **Microsoft Phase-out**: As recently as early 2026, Microsoft has been actively phasing out RC4 from Windows Kerberos authentication to prevent "Kerberoasting" and other credential-cracking attacks. 


### How it works
RC4 encryption transforms plaintext into ciphertext through a two-phase process: initializing a secret state and then generating a pseudorandom stream of bytes to "lock" the data.

```text 
    [ User Input ]
          |
    +-----+-----+           +-----------------------+
    | Plaintext |           |      Secret Key       |
    +-----+-----+           +-----------+-----------+
          |                             |
          |                  1. Key Scheduling (KSA)
          |                [ Shuffles 256-byte S-Box ]
          |                             |
          |                             v
          |                  2. Stream Generation (PRGA)
          |                [ Generates Keystream Bytes ]
          |                             |
          +------------+   +------------+
                       |   |
                       v   v
                +-----------------+
                |  XOR Operation  | (Byte-by-Byte)
                +--------+--------+
                         |
                         v
                  +------------+
                  | Ciphertext |
                  +------------+

```

#### Detailed Breakdown of the Steps

- **Key Scheduling Algorithm (KSA)**: The process begins by initializing an array of 256 bytes (the S-box) with values from 0 to 255. The secret key is then used to swap elements in this array, creating a unique, secret permutation.
- **Pseudo-Random Generation Algorithm (PRGA)**: Once the S-box is scrambled, the algorithm generates a "keystream". It continues to swap values in the S-box to produce a new pseudorandom byte for every byte of your message.
- **XOR Operation**: This is the final step where encryption actually happens. Each byte of your plaintext is combined with a byte from the keystream using an XOR (Exclusive OR) logic gate. This results in the ciphertext, which is the same length as the original input.


### Python Implementation
Below is a simple Python implementation of the **RC4** algorithm. This script includes the two core phases: the **Key Scheduling Algorithm (KSA)** and the **Pseudo-Random Generation Algorithm (PRGA)**. 
```python 
def rc4_algorithm(key, data):
    # --- Phase 1: Key Scheduling Algorithm (KSA) ---
    # Initialize the S-box with values 0 to 255
    S = list(range(256))
    j = 0
    key_length = len(key)
    
    for i in range(256):
        # Scramble the S-box using the secret key
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]  # Swap

    # --- Phase 2: Pseudo-Random Generation Algorithm (PRGA) ---
    i = 0
    j = 0
    result = []
    
    for char in data:
        # Update pointers
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        
        # Swap values in the evolving S-box
        S[i], S[j] = S[j], S[i]
        
        # Pick the keystream byte
        keystream_byte = S[(S[i] + S[j]) % 256]
        
        # XOR the keystream byte with the data byte
        result.append(char ^ keystream_byte)
        
    return bytes(result)

# --- Usage Example ---
secret_key = b"SuperSecretKey"  # Must be bytes
plaintext = b"Hello, this is a secret message!"

# Encrypt
ciphertext = rc4_algorithm(secret_key, plaintext)
print(f"Ciphertext (Hex): {ciphertext.hex()}")

# Decrypt (RC4 is symmetric, so running it again with the same key decrypts)
decrypted_text = rc4_algorithm(secret_key, ciphertext)
print(f"Decrypted Message: {decrypted_text.decode()}")

```


#### Explanation of the Code
1. S-box Initialization: We create a list of 256 integers. This is our "internal state."
2. The Swaps: The S[i], S[j] = S[j], S[i] lines are critical. They ensure the state is shuffled based on your key during KSA and reshuffled during PRGA so the keystream never repeats the same pattern.
3. XOR Operator: The ^ symbol performs the bitwise XOR. Because XOR is its own inverse, the same function is used for both encryption and decryption. 


### C Implementation
Implementing RC4 in **C** requires manual management of the S-box array. Because RC4 is a symmetric stream cipher, the same function used for encryption also performs decryption. 

``` C
#include <stdio.h>
#include <string.h>

// Standard S-box size for RC4
#define N 256

// Helper to swap two values
void swap(unsigned char *a, unsigned char *b) {
    unsigned char tmp = *a;
    *a = *b;
    *b = tmp;
}

// 1. Key Scheduling Algorithm (KSA)
// Initializes the S-box permutation based on the provided key.
void rc4_ksa(unsigned char *S, const unsigned char *key, int key_len) {
    for (int i = 0; i < N; i++)
        S[i] = i;

    int j = 0;
    for (int i = 0; i < N; i++) {
        j = (j + S[i] + key[i % key_len]) % N;
        swap(&S[i], &S[j]);
    }
}

// 2. Pseudo-Random Generation Algorithm (PRGA) & XOR
// Generates the keystream and XORs it with the data.
void rc4_prga_xor(unsigned char *S, unsigned char *data, int data_len) {
    int i = 0, j = 0;
    for (int k = 0; k < data_len; k++) {
        i = (i + 1) % N;
        j = (j + S[i]) % N;
        swap(&S[i], &S[j]);
        
        unsigned char keystream_byte = S[(S[i] + S[j]) % N];
        data[k] ^= keystream_byte; // XOR operation for encryption/decryption
    }
}

int main() {
    unsigned char S[N];
    unsigned char key[] = "SecretKey";
    unsigned char data[] = "Hello, World!";
    int data_len = strlen((char*)data);

    printf("Original: %s\n", data);

    // Encrypt
    rc4_ksa(S, key, strlen((char*)key));
    rc4_prga_xor(S, data, data_len);
    printf("Encrypted (Hex): ");
    for(int i = 0; i < data_len; i++) printf("%02X ", data[i]);
    printf("\n");

    // Decrypt (Re-initialize S-box and run again)
    rc4_ksa(S, key, strlen((char*)key));
    rc4_prga_xor(S, data, data_len);
    printf("Decrypted: %s\n", data);

    return 0;
}

```

#### Key Implementation Details
- **Unsigned Char**: It is essential to use unsigned char (8-bit) for the S-box and data to ensure modulo 256 math works correctly and prevents sign-extension issues during bitwise operations.
- **State Reset**: Since the PRGA modifies the S-box state during encryption, you must re-run the KSA to reset the S-box before attempting to decrypt.
- **The XOR Inverse**: The logic for turning plaintext into ciphertext is identical to turning ciphertext back into plaintext. 



Since RC4 is a stream cipher both sides of the communications need to be aware of where in the stream the cipher is. If either side loses track of the location they become desynchronized. This can be solved in two ways:
	1. Including the KeyId in the message.
	2. Resetting the stream with each session/message. 

In modern cryptography, sending the key along with the ciphertext is a "security sin" because it defeats the purpose of encryption. However, this exact scenario happened in real-world history with WEP (Wired Equivalent Privacy), the original Wi-Fi security protocol.

WEP used RC4 in a way that included a portion of the keying material the Initialization Vector (IV) in every single network packet.

#### The WEP Packet Structure (RC4 in Action)
In a WEP-protected network, the "Key" used for the RC4 algorithm was actually a combination of two things:
1. **The Secret Key**: (e.g., 40-bit or 104-bit) which you typed into your router.
2. **The IV (Initialization Vector)**: A 24-bit number that changed with every packet.

Because the receiver needs the IV to know which "starting point" the sender used, the IV was sent in plain text at the beginning of every packet.

``` text
[ Non-Encrypted Header ] [ Encrypted Payload ]
+----------------------+----------------------+
|  IV (24-bit) | KeyID |  Data (RC4 Encrypted)|
| (SENT IN CLEAR)      |  (XOR'd with Stream) |
+----------+-----------+-----------+----------+
           |                       ^
           |   [ RC4 Algorithm ]   |
           +--> (Secret Key + IV) -+
                    |
              (Keystream)

```


#### Possible RC4 Implementation
``` text
0      7 8     15 16    23 24    31
+--------+--------+--------+--------+
|           IV (3 Bytes)            |  <-- Initialization Vector
|                 +-----------------+
|                 | Key (Variable)  |  <-- THE KEY
+--------+--------+                 |
|      (Key continued...)           |
+-----------------+-----------------+
|   Payload Len   |                 |  <-- Length of Ciphertext
+-----------------+                 |
|                                   |
|      RC4 Encrypted Payload        |  <-- Data
|      (Size = Payload Len)         |
|                                   |
+-----------------------------------+
|        Checksum / CRC32           |  <-- Integrity Check
+-----------------------------------+
```


#### Possible Salsa20 Implementation w/ 64-bit nonce
``` Text
0      7 8     15 16    23 24    31
+--------+--------+--------+--------+
|           Nonce (8 Bytes)         |  <-- 64-bit Nonce
|                                   |
+-----------------------------------+
|           Key (32 Bytes)          |  <-- 256-bit Secret Key
|                                   |
|        (Key continues...)         |
|                                   |
+-----------------+-----------------+
|   Payload Len   |                 |  <-- Length of Ciphertext
+-----------------+                 |
|                                   |
|     Salsa20 Encrypted Payload     |  <-- Data
|      (Size = Payload Len)         |
|                                   |
+-----------------------------------+
|        Checksum / CRC32           |  <-- Integrity Check
+-----------------------------------+
```


#### Possible AES-CBC Implementation w/ 128-bit Key and IV
``` text
0      7 8     15 16    23 24    31
+--------+--------+--------+--------+
|           IV (16 Bytes)           |  <-- Initialization Vector
|                                   |  
|        (IV continues...)          |
+-----------------------------------+
|           Key (16 Bytes)          |  <-- 128-bit Secret Key
|                                   |
|        (Key continues...)         |
+-----------------+-----------------+
|   Payload Len   |                 |  <-- Length of ORIGINAL data
+-----------------+                 |      (Before padding)
|                                   |
|       AES Encrypted Payload       |  <-- Data (Always a multiple 
|      (Multiple of 16 Bytes)       |      of 16 bytes)
|                                   |
+-----------------------------------+
|        Checksum / CRC32           |  <-- Integrity Check
+-----------------------------------+

```

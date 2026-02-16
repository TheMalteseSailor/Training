# Encryption
What is the difference between encryption and encoding?

#### Definitions

**Encoding**: The process of converting data into a new format so it can be safely stored or transmitted across different systems. Its primary goal is data usability and compatibility.

**Encryption**: The process of transforming data into an unreadable format using mathematical algorithms and a secret key. Its primary goal is confidentiality, ensuring only authorized parties can read the information. 


#### Types of Encryption

1. **Symmetric Encryption (One-Key)** 
In this method, the same secret key is used for both encryption and decryption. It is extremely fast and efficient, making it the "workhorse" for protecting large amounts of data. 
- Common Algorithms:
	- AES (Advanced Encryption Standard): The global gold standard used by governments and banks to secure classified files and Wi-Fi.
	- Blowfish / Twofish: Known for their high speed; Twofish is often found in password managers.
	- 3DES (Triple DES): An older, slower legacy method that is being phased out in favor of AES.
- Best For: Encrypting hard drives, databases, and large file transfers. 

2. **Asymmetric Encryption (Two-Key)**
Also known as Public-Key Cryptography, this uses a pair of keys: a public key (to lock) and a private key (to unlock). Because the keys are different, it solves the problem of how to safely share a secret over the open internet. 
- Common Algorithms:
	- RSA: Used for secure data transmission and digital signatures.
	- ECC (Elliptic Curve Cryptography): Provides the same security as RSA but with much smaller keys, making it ideal for mobile devices.
- Best For: SSL/TLS (HTTPS) for websites, digital signatures, and secure email (PGP). 

3. **Hybrid Encryption (The "Real World" Method)**
Modern systems like HTTPS or VPNs use both: 
-  Asymmetric encryption is used first to securely exchange a temporary secret key.
- Symmetric encryption then takes over to encrypt the actual data at high speed using that secret key. 





[RC4](RC4.md)

[Salsa20](Salsa20.md)

[AES](AES.md)

[Network Encryption](Network%20Encryption.md)

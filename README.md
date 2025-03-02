# SHA-256 Implementation

## Introduction
This project implements the SHA-256 (Secure Hash Algorithm 256-bit) as specified by NIST. SHA-256 is a cryptographic hash function that produces a 256-bit (32-byte) hash value, commonly used in various security applications and protocols, including TLS and SSL, PGP, SSH, and IPsec.

## Features
- **Cryptographic Security**: Provides a secure hash function suitable for various applications.
- **Customizable Input**: Accepts both string and byte inputs for hashing.
- **Hexadecimal Output**: Returns the hash as a 64-character hexadecimal string.

## Tech Stack
- **Python**: The implementation is written in Python.
- **No External Libraries**: The algorithm is implemented without relying on external libraries, ensuring portability and ease of use.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/prabhatpushp/sha256
   cd sha256
   ```
2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use .venv\Scripts\activate
   ```
3. Install any required dependencies (if applicable).

## Usage
To compute the SHA-256 hash of a message, you can use the `sha256` function:
```python
from main import sha256

message = "hello world"
hash_result = sha256(message)
print(f"SHA-256 hash of '{{message}}': {{hash_result}}")
```

## Development
- The main implementation is in `main.py`. You can modify or extend the functionality as needed.
- Ensure to test your changes thoroughly to maintain the integrity of the hashing function.

## Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes and create a pull request.

## License
This project is licensed under the MIT License. Feel free to use this project for personal or commercial purposes. 

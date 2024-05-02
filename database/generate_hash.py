from argon2 import PasswordHasher

# Replace 'your_password' with your actual PostgreSQL password
password = '12345'

# Create an instance of PasswordHasher
ph = PasswordHasher()

# Generate the Argon2 hash for the password
argon2_hash = ph.hash(password)

print("Argon2 Hash:", argon2_hash)

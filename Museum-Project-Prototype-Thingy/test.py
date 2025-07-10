import bcrypt

def hash_password(plain_password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed

if __name__ == "__main__":
    password = input("Enter password to hash: ")
    hashed_password = hash_password(password)
    print(f"Hashed password: {hashed_password}")
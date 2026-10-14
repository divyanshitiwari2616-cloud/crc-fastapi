import bcrypt


def generate_password(password: str) -> str:
    password_to_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    print("Salt value is:", salt)

    hashed_password = bcrypt.hashpw(
        password=password_to_bytes,
        salt=salt
    )

    print("Hashed value:", hashed_password)

    return hashed_password.decode("utf-8")


def check_password(plain_text: str, hashed_value: str) -> bool:
    plain_password_to_byte = plain_text.encode("utf-8")
    hashed_value_to_byte = hashed_value.encode("utf-8")

    return bcrypt.checkpw(
        password=plain_password_to_byte,
        hashed_password=hashed_value_to_byte
    )


# Generate hash
hashed = generate_password("pass123@")

print("Final password:", hashed)

# Check correct password
print("Password check:", check_password("pass123@", hashed))

# Check wrong password
print("Wrong password check:", check_password("wrong123", hashed))
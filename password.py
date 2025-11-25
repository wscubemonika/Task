import random
import string

def generate_password(length=12, use_digits=True, use_specials=True):
    # Base character set
    characters = string.ascii_letters  # a-zA-Z

    if use_digits:
        characters += string.digits     # 0-9
    if use_specials:
        characters += string.punctuation  # !@#$%^&*()...

    # Ensure at least one character from each selected category
    password = []
    if use_digits:
        password.append(random.choice(string.digits))
    if use_specials:
        password.append(random.choice(string.punctuation))
    password.append(random.choice(string.ascii_lowercase))
    password.append(random.choice(string.ascii_uppercase))

    # Fill the rest of the password
    while len(password) < length:
        password.append(random.choice(characters))

    # Shuffle to avoid predictable patterns
    random.shuffle(password)

    return ''.join(password)

# Example usage
print("Generated password:", generate_password(length=16))
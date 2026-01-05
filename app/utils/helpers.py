import secrets
import string

def generate_random_string(length: int = 32) -> str:
    """Generate a random string for tokens, etc."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

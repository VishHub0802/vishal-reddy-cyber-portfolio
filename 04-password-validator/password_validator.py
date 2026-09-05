import re
import sys

COMMON_PASSWORDS = {
    "123456", "password", "123456789", "qwerty", "abc123",
    "password1", "111111", "letmein", "admin", "welcome"
}

def has_sequential_chars(password, run_length=4):
    password = password.lower()
    for i in range(len(password) - run_length + 1):
        window = password[i:i + run_length]
        if all(ord(window[j + 1]) - ord(window[j]) == 1 for j in range(len(window) - 1)):
            return True
    return False

def score_to_strength(score, max_score):
    ratio = score / max_score
    if ratio == 1.0:
        return "Strong"
    elif ratio >= 0.7:
        return "Moderate"
    elif ratio >= 0.4:
        return "Weak"
    else:
        return "Very Weak"

def check_password(password):
    checks = []

    length_ok = len(password) >= 12
    checks.append((length_ok, "At least 12 characters long"))

    has_lowercase = bool(re.search(r"[a-z]", password))
    checks.append((has_lowercase, "Contains a lowercase letter"))

    has_uppercase = bool(re.search(r"[A-Z]", password))
    checks.append((has_uppercase, "Contains an uppercase letter"))

    has_digit = bool(re.search(r"[0-9]", password))
    checks.append((has_digit, "Contains a number"))

    has_speccharacter = bool(re.search(r"[^a-zA-Z0-9]", password))
    checks.append((has_speccharacter, "Contains a special character"))

    not_common = password.lower() not in COMMON_PASSWORDS
    checks.append((not_common, "Not a commonly used password"))

    no_sequential = not has_sequential_chars(password)
    checks.append((no_sequential, "No obvious sequential patterns (e.g. '1234', 'abcd')"))

    score = sum(1 for passed, _ in checks if passed)
    strength = score_to_strength(score, len(checks))

    return {"checks": checks, "score": score, "max_score": len(checks), "strength": strength}

def print_result(password, result):
    print(f"\nPassword: {'*' * len(password)}  (length {len(password)})")
    print(f"Strength: {result['strength']}  ({result['score']}/{result['max_score']} checks passed)")
    print("-" * 50)
    for passed, description in result["checks"]:
        mark = "✓" if passed else "✗"
        print(f"  [{mark}] {description}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python password_validator.py <password>")
        sys.exit(1)

    password = sys.argv[1]
    result = check_password(password)
    print_result(password, result)
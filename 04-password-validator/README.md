# Password Strength Validator

A Python tool that checks a password against common security best
practices and gives it a strength rating, similar to the "password
strength" meter used on most login/signup forms.

## Scenario

Weak passwords remain one of the most common root causes of account
compromise. This project builds the logic behind a password policy
checker: rather than just checking length, it evaluates a password
against multiple independent criteria commonly recommended by
security guidance (e.g. NIST SP 800-63B), including a check against a
list of frequently reused passwords.

## Checks Performed

- Minimum length (12+ characters)
- Contains lowercase and uppercase letters
- Contains at least one digit
- Contains at least one special character
- Not found in a list of commonly used passwords
- No obvious sequential patterns (e.g. `1234`, `abcd`)

## Tools & Techniques

- **Python 3** — regex-based pattern matching (`re` module), string analysis
- Rule-based scoring system (returns a strength rating, not just pass/fail)
- Common-password blocklist check using set membership for fast lookups
- Sliding-window algorithm to detect sequential character runs

## Files

| File | Purpose |
|---|---|
| `password_validator.py` | Core validator logic and CLI |

## Usage

```bash
python3 password_validator.py "MyP@ssw0rd123"
```

## Sample Output

Password: **************** (length 16)
Strength: Strong (7/7 checks passed)

[✓] At least 12 characters long
[✓] Contains a lowercase letter
[✓] Contains an uppercase letter
[✓] Contains a digit
[✓] Contains a special character (e.g. !@#$%^&*)
[✓] Not one of the most commonly used passwords
[✓] No obvious sequential patterns (e.g. '1234', 'abcd')

## Possible Extensions

- Check against a much larger breach-password dataset
- Bulk-check passwords from a file
- Estimate entropy/crack time (e.g. using the `zxcvbn` library)

## Deliverables

- Password strength validation tool with rule-based scoring
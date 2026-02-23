# Secure Coding Rule

Build secure by default. If a shortcut lowers security, reject it unless explicitly approved and documented.

## Must Do
- Validate all external input (allowlists/schemas/types).
- Encode/sanitize untrusted output for context.
- Use parameterized queries and safe APIs (no executable string building).
- Enforce server-side AuthN/AuthZ at trust boundaries.
- Apply least privilege and never hardcode secrets.
- Use modern cryptography and secure randomness.
- Fail closed with minimal error disclosure.
- Add security tests for risky paths.
- Keep dependencies minimal, maintained, and updated.

## Must Not
- Hardcode credentials, tokens, or private keys.
- Use `eval`, unsafe deserialization, or raw shell execution on untrusted input.
- Disable TLS/certificate validation in production.
- Rely on client-side-only authorization.
- Log secrets, passwords, tokens, or sensitive PII.

## Escalation
If a request conflicts with this rule, pause and propose a safer alternative.

---

name: auth-skill

description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.

---

# Authentication Skill

## Instructions

1. **User Signup**
   - Accept user credentials (email/username, password)
   - Validate input data
   - Hash passwords before storing
   - Prevent duplicate accounts

2. **User Signin**
   - Verify user credentials
   - Compare hashed passwords securely
   - Return authentication tokens on success
   - Handle invalid credentials gracefully

3. **Password Security**
   - Use strong hashing algorithms (bcrypt, argon2)
   - Apply salting
   - Never store plain-text passwords

4. **JWT Authentication**
   - Generate access tokens on login
   - Include user claims in JWT payload
   - Set expiration and refresh strategy
   - Protect private routes using middleware

5. **Better Auth Integration**
   - Configure Better Auth provider
   - Enable session and token-based auth
   - Support OAuth and email/password flows
   - Handle token refresh and logout

## Best Practices

- Use environment variables for secrets
- Enforce strong password rules
- Implement rate limiting on auth routes
- Use HTTPS only
- Validate JWT on every protected request
- Separate auth logic from business logic

## Example Structure

```ts
// Signup
POST /auth/signup
{
  email: string,
  password: string
}

// Signin
POST /auth/signin
{
  email: string,
  password: string
}

// JWT Middleware
function authenticate(req, res, next) {
  const token = req.headers.authorization
  verifyJWT(token)
  next()
}

---
name: backend-api-development
description: Generate backend routes, handle HTTP requests and responses, and connect APIs to databases. Use for server-side applications.
---

# Backend API Development

## Instructions

1. **Route Generation**

   - Define RESTful endpoints  
   - Organize routes by resource  
   - Use proper HTTP methods (GET, POST, PUT, DELETE)  

2. **Request & Response Handling**

   - Validate incoming data  
   - Handle query params, path params, and body  
   - Return standardized JSON responses  
   - Manage error handling and status codes  

3. **Database Connection**

   - Establish secure DB connections  
   - Perform CRUD operations  
   - Use ORM or query builders  
   - Handle connection pooling  

## Best Practices

- Keep controllers thin and logic reusable  
- Use environment variables for secrets  
- Follow REST conventions  
- Implement centralized error handling  
- Log requests and failures  
- Secure APIs with authentication & authorization  

## Example Structure

```ts
// routes/user.routes.ts
import express from "express";
import { createUser, getUsers } from "../controllers/user.controller";

const router = express.Router();

router.post("/users", createUser);
router.get("/users", getUsers);

export default router;

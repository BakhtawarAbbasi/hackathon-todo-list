---
name: database-schema-design
description: Design relational database schemas, create tables, and manage migrations. Use for backend and full-stack applications.
---

# Database Schema Design & Migrations

## Instructions

1. **Schema Design**

   - Identify entities and relationships  
   - Normalize data (avoid redundancy)  
   - Define primary and foreign keys  

2. **Table Creation**

   - Use appropriate data types  
   - Apply constraints (NOT NULL, UNIQUE, DEFAULT)  
   - Add indexes for performance  

3. **Migrations**

   - Create versioned migration files  
   - Support up and down (rollback) operations  
   - Keep schema changes incremental  

## Best Practices

- Follow normalization rules (up to 3NF when possible)  
- Use clear, consistent naming conventions  
- Never modify production data directly  
- Always test migrations on staging/dev  
- Document schema changes  

## Example Structure

```sql
-- users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- orders table
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  total_amount DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

import { betterAuth } from 'better-auth';
import { neon } from '@neondatabase/serverless';

// Initialize Better Auth with Neon DB
const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || 'fallback-secret-for-development',
  database: {
    provider: 'neon',
    url: process.env.AUTH_DATABASE_URL || process.env.NEON_DATABASE_URL || '',
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
  jwt: {
    expiresIn: '7d',
  },
});

// Export the API route handlers
export { auth as GET, auth as POST };
// frontend/services/auth.ts
import type { User, AuthResponse, LoginCredentials, RegisterCredentials } from '@/types/auth';

// API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Helper function to convert backend user response to our User type
const mapBackendUser = (userData: any): User => {
  return {
    id: userData.id || userData.user?.id,
    email: userData.email || userData.user?.email,
    name: userData.name || userData.user?.name || '',
    createdAt: userData.created_at || userData.user?.created_at || new Date().toISOString(),
    updatedAt: userData.updated_at || userData.user?.updated_at || new Date().toISOString(),
  };
};

class AuthService {
  // Sign up a new user
  async register(credentials: RegisterCredentials): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/sign-up`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: credentials.email,
          password: credentials.password,
          name: credentials.name,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || errorData.message || 'Registration failed');
      }

      const result = await response.json();
      const user = mapBackendUser(result);

      // Store the token in localStorage for API calls
      if (result.access_token) {
        if (typeof window !== 'undefined') {
          localStorage.setItem('better-auth-session-token', result.access_token);
        }
      }

      return {
        user,
        token: result.access_token || result.session?.token || '',
      };
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  }

  // Sign in an existing user
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/sign-in`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: credentials.email,
          password: credentials.password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || errorData.message || 'Login failed');
      }

      const result = await response.json();
      const user = mapBackendUser(result);

      // Store the token in localStorage for API calls
      if (result.access_token) {
        if (typeof window !== 'undefined') {
          localStorage.setItem('better-auth-session-token', result.access_token);
        }
      }

      return {
        user,
        token: result.access_token || result.session?.token || '',
      };
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  // Sign out the current user
  async logout(): Promise<void> {
    try {
      await fetch(`${API_BASE_URL}/api/auth/logout`, {
        method: 'POST',
      });
      // Clear any local storage or session data
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth-token');
      }
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  }

  // Get the current user session
  async getCurrentUser(): Promise<User | null> {
    try {
      const token = localStorage.getItem('auth-token');
      if (!token) {
        return null;
      }

      // Make a call to a protected endpoint to validate the token and get user info
      const response = await fetch(`${API_BASE_URL}/api/auth/user/profile`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const userData = await response.json();
        return mapBackendUser({user: userData}); // Wrap in user object to match expected format
      } else {
        // If the token is invalid, remove it from local storage
        if (typeof window !== 'undefined') {
          localStorage.removeItem('better-auth-session-token');
        }
        return null;
      }
    } catch (error) {
      console.error('Session check error:', error);
      return null;
    }
  }

  // Check if user is authenticated
  async isAuthenticated(): Promise<boolean> {
    const token = localStorage.getItem('better-auth-session-token');
    return token !== null && token.length > 0;
  }
}

// Export a singleton instance of the AuthService
export const authService = new AuthService();

// Export individual methods for convenience
export const { register, login, logout, getCurrentUser, isAuthenticated } = authService;
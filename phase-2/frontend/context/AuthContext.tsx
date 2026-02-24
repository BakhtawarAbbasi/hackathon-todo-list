'use client';

import { useState, useEffect, useContext, createContext, ReactNode } from 'react';
import { getCurrentUser, login as authLogin, logout as authLogout, register as authRegister } from '@/services/auth';
import { User } from '@/types/auth';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (email: string, password: string, name?: string) => Promise<void>;
  refetchUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthContextProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Check authentication status on initial load
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        setLoading(true);
        setError(null);

        const currentUser = await getCurrentUser();
        setUser(currentUser);
      } catch (err) {
        console.error('Auth check error:', err);
        // Don't set error if it's just no user logged in
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const refetchUser = async () => {
    try {
      setLoading(true);
      setError(null);

      const currentUser = await getCurrentUser();
      setUser(currentUser);

      return currentUser;
    } catch (err) {
      console.error('Refetch user error:', err);
      setError(err instanceof Error ? err.message : 'Failed to refetch user');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const loginHandler = async (email: string, password: string) => {
    try {
      setLoading(true);
      setError(null);

      const result = await authLogin({ email, password });
      // Store the token in localStorage for API calls
      if (result.token) {
        if (typeof window !== 'undefined') {
          localStorage.setItem('better-auth-session-token', result.token);
        }
      }
      const currentUser = await getCurrentUser();
      setUser(currentUser);
    } catch (err) {
      console.error('Login error:', err);
      setError(err instanceof Error ? err.message : 'Login failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logoutHandler = async () => {
    try {
      setLoading(true);
      setError(null);

      await authLogout();
      setUser(null);
      // Clear the token from localStorage
      if (typeof window !== 'undefined') {
        localStorage.removeItem('better-auth-session-token');
      }
    } catch (err) {
      console.error('Logout error:', err);
      setError(err instanceof Error ? err.message : 'Logout failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const registerHandler = async (email: string, password: string, name?: string) => {
    try {
      setLoading(true);
      setError(null);

      const result = await authRegister({ email, password, name });
      // Store the token in localStorage for API calls
      if (result.token) {
        if (typeof window !== 'undefined') {
          localStorage.setItem('better-auth-session-token', result.token);
        }
      }
      const currentUser = await getCurrentUser();
      setUser(currentUser);
    } catch (err) {
      console.error('Register error:', err);
      setError(err instanceof Error ? err.message : 'Registration failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const value = {
    user,
    loading,
    error,
    isAuthenticated: !!user,
    login: loginHandler,
    logout: logoutHandler,
    register: registerHandler,
    refetchUser
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthContextProvider');
  }
  return context;
}
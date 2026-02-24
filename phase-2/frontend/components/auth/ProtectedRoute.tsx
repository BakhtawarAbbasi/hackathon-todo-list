'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { ROUTES } from '@/lib/constants';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode; // Optional fallback component while checking auth status
  redirectTo?: string; // Optional redirect URL, defaults to login
}

export default function ProtectedRoute({
  children,
  fallback = <div className="flex items-center justify-center min-h-screen">Loading...</div>,
  redirectTo = ROUTES.LOGIN,
}: ProtectedRouteProps) {
  const router = useRouter();
  const { loading, isAuthenticated } = useAuth();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push(redirectTo);
    }
  }, [isAuthenticated, loading, redirectTo, router]);

  // Show fallback while checking authentication status
  if (loading) {
    return fallback;
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return null;
  }

  // Render children if authenticated
  return <>{children}</>;
}
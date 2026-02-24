'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import SignupForm from '@/components/auth/SignupForm';
import { ROUTES } from '@/lib/constants';

export default function SignupPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const [error, setError] = useState<string | null>(null);

  // If user is already authenticated, redirect to dashboard
  if (isAuthenticated) {
    router.push(ROUTES.DASHBOARD);
    return null;
  }

  const handleSuccess = () => {
    router.push(ROUTES.DASHBOARD);
    router.refresh();
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Or{' '}
            <Link
              href={ROUTES.LOGIN}
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              sign in to your account
            </Link>
          </p>
        </div>

        {error && (
          <div className="bg-red-50 text-red-700 p-3 rounded-md text-sm">
            {error}
          </div>
        )}

        <div className="mt-8 bg-white py-8 px-4 shadow rounded-lg sm:px-10">
          <SignupForm
            onSuccess={handleSuccess}
            onError={handleError}
          />
        </div>
      </div>
    </div>
  );
}
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function RegisterPage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to the actual signup page
    router.push('/auth/signup');
  }, [router]);

  return null;
}
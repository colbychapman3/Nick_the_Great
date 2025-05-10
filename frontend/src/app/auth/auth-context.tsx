'use client';

// This file is a compatibility layer for code that might be importing from '@/app/auth/auth-context'
// It re-exports everything from the actual AuthContext implementation in '@/lib/AuthContext'

export * from '@/lib/AuthContext';

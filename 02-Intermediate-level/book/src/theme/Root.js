import React from 'react';
import AuthProvider from '@site/src/auth/AuthProvider';

// Default implementation, that you can customize
export default function Root({children}) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}
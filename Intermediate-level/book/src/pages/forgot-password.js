import React, { useState } from 'react';
import Layout from '@theme/Layout';
import styles from './styles.module.css';

function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Try to get auth context, but provide fallback for SSG
  const { resetPassword } = (typeof window !== 'undefined' && window.location)
    ? require('@site/src/auth/AuthContext').useAuth
      ? require('@site/src/auth/AuthContext').useAuth()
      : { resetPassword: null }
    : { resetPassword: null };

  const handleSubmit = async (e) => {
    if (!resetPassword) {
      setError('Authentication service is not available during build');
      return;
    }

    e.preventDefault();
    setError('');
    setSuccess('');
    setIsSubmitting(true);

    try {
      await resetPassword(email);
      setSuccess('Check your inbox for further instructions.');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Layout title="Forgot Password">
      <div className={styles.container}>
        <div className={styles.formContainer}>
          <h2>Forgot Password</h2>
          <p>Enter your email to receive a password reset link.</p>
          {error && <p className={styles.error}>{error}</p>}
          {success && <p className={styles.success}>{success}</p>}
          <form onSubmit={handleSubmit}>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
              required
            />
            <button type="submit" disabled={isSubmitting || !resetPassword}>
              {isSubmitting ? 'Sending...' : resetPassword ? 'Reset Password' : 'Service not available'}
            </button>
          </form>
          <p>
            Remember your password? <a href="/login">Login</a>
          </p>
        </div>
      </div>
    </Layout>
  );
}

export default ForgotPassword;
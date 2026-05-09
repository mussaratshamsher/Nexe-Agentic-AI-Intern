import React, { useState, useEffect } from 'react';
import { useHistory } from '@docusaurus/router';
import Layout from '@theme/Layout';
import styles from './styles.module.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Get auth context - now available through the AuthProvider wrapper
  const { useAuth } = require('@site/src/auth/AuthContext');
  const { user, login, signInWithGoogle } = useAuth() || { user: null, login: null, signInWithGoogle: null };

  const history = useHistory();

  useEffect(() => {
    if (user) {
      if (typeof window !== 'undefined' && history) {
        history.push('/profile');
      }
    }
  }, [user, history]);

  const handleSubmit = async (e) => {
    if (!login) {
      setError('Authentication service is not available');
      return;
    }

    e.preventDefault();
    setError('');
    setIsSubmitting(true);
    try {
      await login(email, password);
      if (typeof window !== 'undefined' && history) {
        history.push('/profile');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleGoogleSignIn = async () => {
    if (!signInWithGoogle) {
      setError('Google sign-in is not available');
      return;
    }

    setError('');
    setIsSubmitting(true);
    try {
      await signInWithGoogle();
      if (typeof window !== 'undefined' && history) {
        history.push('/profile');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Layout title="Login">
      <div className={styles.container}>
        <div className={styles.formContainer}>
          <h2>Login</h2>
          {error && <p className={styles.error}>{error}</p>}
          <form onSubmit={handleSubmit}>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
              required
            />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              required
            />
            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Logging in...' : 'Login'}
            </button>
          </form>
          <div className={styles.orSeparator}>
            <span className={styles.orSeparatorText}>OR</span>
          </div>
          <button
            onClick={handleGoogleSignIn}
            className={styles.googleButton}
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Please wait...' : 'Sign in with Google'}
          </button>
          <p>
            Don't have an account? <a href="/signup">Sign up</a> |{' '}
            <a href="/forgot-password">Forgot Password?</a>
          </p>
        </div>
      </div>
    </Layout>
  );
}

export default Login;

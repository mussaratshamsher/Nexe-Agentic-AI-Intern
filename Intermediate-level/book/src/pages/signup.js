import React, { useState, useEffect } from 'react';
import { useHistory } from '@docusaurus/router';
import Layout from '@theme/Layout';
import styles from './styles.module.css';

function Signup() {
  const [displayName, setDisplayName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Try to get auth context, but provide fallback for SSG
  const { user, signup, signInWithGoogle } = (typeof window !== 'undefined' && window.location)
    ? require('@site/src/auth/AuthContext').useAuth
      ? require('@site/src/auth/AuthContext').useAuth()
      : { user: null, signup: null, signInWithGoogle: null }
    : { user: null, signup: null, signInWithGoogle: null };

  const history = useHistory();

  useEffect(() => {
    if (user) {
      if (typeof window !== 'undefined' && history) {
        history.push('/profile');
      }
    }
  }, [user, history]);

  const handleSubmit = async (e) => {
    if (!signup) {
      setError('Authentication service is not available');
      return;
    }

    e.preventDefault();
    setError('');
    setIsSubmitting(true);
    try {
      await signup(email, password, displayName);
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
    <Layout title="Sign Up">
      <div className={styles.container}>
        <div className={styles.formContainer}>
          <h2>Sign Up</h2>
          {error && <p className={styles.error}>{error}</p>}
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              placeholder="Display Name"
              required
            />
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
              {isSubmitting ? 'Signing up...' : 'Sign Up'}
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
            {isSubmitting ? 'Please wait...' : 'Sign up with Google'}
          </button>
          <p>
            Already have an account? <a href="/login">Login</a>
          </p>
        </div>
      </div>
    </Layout>
  );
}

export default Signup;

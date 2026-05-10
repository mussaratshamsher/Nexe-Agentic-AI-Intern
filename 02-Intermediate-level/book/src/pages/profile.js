import React, { useState, useEffect } from 'react';
import { useHistory } from '@docusaurus/router';
import Layout from '@theme/Layout';
import { useAuth } from '@site/src/auth/AuthContext';
import styles from './styles.module.css';

function Profile() {
  const { user, setUser, logout, updateProfile } = useAuth() || {};
  const [displayName, setDisplayName] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isSubmittingProfile, setIsSubmittingProfile] = useState(false);

  const history = useHistory();

  useEffect(() => {
    if (!user && typeof window !== 'undefined' && history) {
      // Small delay to allow auth state to load
      const timer = setTimeout(() => {
        if (!user) history.push('/login');
      }, 1000);
      return () => clearTimeout(timer);
    } else if (user) {
      setDisplayName(user.displayName || '');
    }
  }, [user, history]);

  const handleProfileUpdate = async (e) => {
    if (!updateProfile) {
      setError('Authentication service is not available');
      return;
    }

    e.preventDefault();
    setError('');
    setSuccess('');
    setIsSubmittingProfile(true);
    try {
      const updatedUser = await updateProfile({ displayName });
      setSuccess('Profile updated successfully!');
      if (setUser) {
        setUser(updatedUser);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmittingProfile(false);
    }
  };

  if (!user) {
    return (
      <Layout title="Profile">
        <div className={styles.container}>
          <div className={styles.formContainer}>
            <p>Loading profile...</p>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Profile">
      <div className={styles.container} style={{ height: 'auto', padding: '4rem 0' }}>
        <div className={styles.formContainer}>
          <h2>Your Profile</h2>
          
          <div className={styles.profileHeader}>
            <div style={{ position: 'relative' }}>
              <img
                src={
                  user.photoURL ||
                  `https://api.dicebear.com/8.x/initials/svg?seed=${encodeURIComponent(
                    user.email
                  )}`
                }
                alt="Profile"
                className={styles.profilePagePic}
              />
            </div>
            <h3>{user.displayName || user.email.split('@')[0]}</h3>
            <p style={{ color: 'var(--ifm-color-emphasis-600)', marginBottom: '1.5rem' }}>{user.email}</p>
          </div>

          <form onSubmit={handleProfileUpdate}>
            <label style={{ display: 'block', textAlign: 'left', marginBottom: '0.5rem', fontWeight: '600' }}>Display Name</label>
            <input
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              placeholder="Display Name"
            />
            <button type="submit" disabled={isSubmittingProfile}>
              {isSubmittingProfile ? 'Updating...' : 'Update Name'}
            </button>
          </form>

          {error && <p className={styles.error}>{error}</p>}
          {success && <p className={styles.success}>{success}</p>}

          <hr className={styles.separator} />

          <button
            onClick={logout}
            className="button button--danger button--outline"
            style={{ width: '100%' }}
          >
            Logout
          </button>
        </div>
      </div>
    </Layout>
  );
}

export default Profile;

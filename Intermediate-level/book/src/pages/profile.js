import React, { useState, useEffect } from 'react';
import { useHistory } from '@docusaurus/router';
import Layout from '@theme/Layout';
import { useAuth } from '@site/src/auth/AuthContext';
import styles from './styles.module.css';

function Profile() {
  const { user, setUser, logout, updatePassword, updateProfile, updateProfilePicture } = useAuth() || {};
  const [newPassword, setNewPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isSubmittingProfile, setIsSubmittingProfile] = useState(false);
  const [isSubmittingPassword, setIsSubmittingPassword] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

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

  const handleProfilePictureChange = async (e) => {
    const file = e.target.files[0];
    if (!file || !updateProfilePicture) return;

    setError('');
    setSuccess('');
    setIsUploading(true);
    try {
      await updateProfilePicture(file);
      setSuccess('Profile picture updated successfully!');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsUploading(false);
    }
  };

  const handlePasswordUpdate = async (e) => {
    if (!updatePassword) {
      setError('Authentication service is not available');
      return;
    }

    e.preventDefault();
    setError('');
    setSuccess('');
    setIsSubmittingPassword(true);
    try {
      await updatePassword(newPassword);
      setSuccess('Password updated successfully!');
      setNewPassword('');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmittingPassword(false);
    }
  };

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
              <label htmlFor="profile-upload" style={{
                position: 'absolute',
                bottom: '15px',
                right: '5px',
                backgroundColor: 'var(--ifm-color-primary)',
                color: 'white',
                borderRadius: '50%',
                width: '32px',
                height: '32px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                boxShadow: '0 2px 5px rgba(0,0,0,0.2)'
              }}>
                📷
                <input
                  id="profile-upload"
                  type="file"
                  accept="image/*"
                  onChange={handleProfilePictureChange}
                  style={{ display: 'none' }}
                />
              </label>
            </div>
            {isUploading && <p style={{ fontSize: '0.8rem' }}>Uploading...</p>}
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

          <hr className={styles.separator} />

          <form onSubmit={handlePasswordUpdate}>
            <label style={{ display: 'block', textAlign: 'left', marginBottom: '0.5rem', fontWeight: '600' }}>Change Password</label>
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="New Password"
            />
            <button type="submit" disabled={isSubmittingPassword}>
              {isSubmittingPassword ? 'Updating...' : 'Update Password'}
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

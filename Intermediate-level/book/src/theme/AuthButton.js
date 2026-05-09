import React, { useContext } from 'react';
import AuthContext from '@site/src/auth/AuthContext';
import Link from '@docusaurus/Link';
import styles from './AuthButton.module.css';

export default function AuthButton() {
  const { user, logout } = useContext(AuthContext);

  console.log('user in AuthButton', user);

  if (user) {
    return (
      <div className="navbar__item" style={{ display: 'flex', alignItems: 'center' }}>
        <Link to="/profile" className={styles.profileLink}>
          {user.photoURL ? (
            <img
              src={user.photoURL}
              alt={user.displayName || user.email}
              className={styles.profilePic}
            />
          ) : (
            <img
              src={`https://api.dicebear.com/8.x/initials/svg?seed=${encodeURIComponent(
                user.email
              )}`}
              alt={user.displayName || user.email}
              className={styles.profilePic}
            />
          )}
        </Link>
        <button
          onClick={logout}
          className="button button--secondary button--sm"
          style={{ marginLeft: '15px' }}>
          Logout
        </button>
      </div>
    );
  }

  return (
    <Link to="/login" className="navbar__item navbar__link">
      Login
    </Link>
  );
}
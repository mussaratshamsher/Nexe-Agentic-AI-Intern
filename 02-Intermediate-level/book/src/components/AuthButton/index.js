import React from 'react';
import { useAuth } from '../../auth/AuthContext';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

const AuthButton = () => {
  const { user, logout } = useAuth();

  return (
    <div className={styles.authButtonContainer}>
      {user ? (
        <div className={styles.userMenu}>
          <Link to="/profile" className={styles.profileLink}>
            {user.displayName || user.email}
          </Link>
          <button onClick={logout} className={styles.logoutButton}>Logout</button>
        </div>
      ) : (
        <Link to="/login" className="button button--secondary">
          Login / Sign Up
        </Link>
      )}
    </div>
  );
};

export default AuthButton;

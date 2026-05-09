import React from 'react';
import styles from './HeroSection.module.css';

function HeroSection({ title, subtitle }) {
  return (
    <header className={styles.heroSection}>
      <div className="container">
        {title && <h1 className={styles.heroTitle}>{title}</h1>}
        {subtitle && <p className={styles.heroSubtitle}>{subtitle}</p>}
      </div>
    </header>
  );
}

export default HeroSection;

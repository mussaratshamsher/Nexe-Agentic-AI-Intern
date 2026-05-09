import React from 'react';
import styles from './SectionBanner.module.css';

function SectionBanner({ children }) {
  return (
    <div className={styles.sectionBanner}>
      {children}
    </div>
  );
}

export default SectionBanner;

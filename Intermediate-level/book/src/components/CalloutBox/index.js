import React from 'react';
import clsx from 'clsx'; // A utility for constructing className strings conditionally
import styles from './CalloutBox.module.css';

const CalloutBox = ({ type, children }) => {
  const typeClass = styles[type] || styles.note; // Default to 'note' if type is not recognized

  // Simple icon representation for now
  const getIcon = (boxType) => {
    switch (boxType) {
      case 'note': return 'ℹ️';
      case 'tip': return '💡';
      case 'warning': return '⚠️';
      case 'insight': return '🧠';
      default: return 'ℹ️';
    }
  };

  return (
    <div className={clsx(styles.calloutBox, typeClass)}>
      <span className={styles.icon}>{getIcon(type)}</span>
      <div className={styles.content}>
        {children}
      </div>
    </div>
  );
};

export default CalloutBox;

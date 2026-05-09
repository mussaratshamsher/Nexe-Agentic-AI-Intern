import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  icon: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Foundations',
    icon: '🏗️',
    description: (
      <>
        Explore the theoretical principles of Physical AI, from cognitive architectures
        to the mathematical foundations of robotics.
      </>
    ),
  },
  {
    title: 'Hands-on Learning',
    icon: '⚙️',
    description: (
      <>
        Master practical implementation with ROS2, Gazebo simulations, and real-world 
        hardware integration guides.
      </>
    ),
  },
  {
    title: 'Advanced AI',
    icon: '🧠',
    description: (
      <>
        Dive into the future with Vision-Language-Action (VLA) models and 
        multimodal systems that power the next generation of humanoid robots.
      </>
    ),
  },
];

function Feature({title, icon, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className={styles.featureCard}>
        <div className={styles.iconWrapper}>
          {icon}
        </div>
        <div className="padding-horiz--md">
          <Heading as="h3" className={styles.featureTitle}>{title}</Heading>
          <p className={styles.featureDescription}>{description}</p>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

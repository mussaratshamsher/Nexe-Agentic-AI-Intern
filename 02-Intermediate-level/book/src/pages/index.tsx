import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';
import CodeBlock from '@theme/CodeBlock';
import Chatbot from '@site/src/components/Chatbot/Chatbot'; 
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();

  return (
    <header className={styles.heroBanner}>
      <div className={clsx('container', styles.heroContainer)}>

        {/* LEFT CONTENT */}
        <div className={styles.heroLeft}>
          <Heading as="h1" className={styles.hero__title}>
            {siteConfig.title}
          </Heading>

          <p className={styles.hero__subtitle}>
            {siteConfig.tagline}
          </p>

          <div className={styles.buttons}>
            <Link
              className={clsx(
                'button',
                styles.button,
                styles.buttonPrimary
              )}
              to="/docs/intro">
              Start Reading
            </Link>

            <Link
              className={clsx(
                'button',
                styles.button,
                styles.buttonSecondary
              )}
              to="/docs/author">
              Read About Author
            </Link>
          </div>
        </div>

        {/* RIGHT CODE PANEL */}
        <div className={styles.heroRight}>
          <div className={styles.codeWrapper}>

            {/* BACK LAYER */}
            <div className={styles.codeCardShadow}></div>

            {/* MAIN CARD */}
            <div className={styles.codeCard}>
              <div className={styles.codeHeader}>
                <div className={styles.codeDots}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <div className={styles.agentIconMini}>
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm9 7h-6v13h-2v-6h-2v6H9V9H3V7h18v2zM5 9v11h2V9H5zm12 0v11h2V9h-2z"/>
                  </svg>
                </div>
              </div>

              <div className={styles.codeBlock}>
                <CodeBlock language="python">
{`agent = Agent(
   name="AI Researcher",
   memory=True,
   tools=[
      "web_search",
      "rag",
      "email"
   ]
)`}
                </CodeBlock>
              </div>
            </div>

          </div>
        </div>

      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description={siteConfig.tagline}>
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <Chatbot />
      </main>
    </Layout>
  );
}

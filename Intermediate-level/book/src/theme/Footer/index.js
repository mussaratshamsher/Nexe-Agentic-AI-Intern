// This is a manual swizzle of the default Docusaurus Footer component.
// Original source: https://github.com/facebook/docusaurus/blob/main/packages/docusaurus-theme-classic/src/theme/Footer/index.tsx

import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './styles.module.css'; // Assuming local CSS module

function FooterLink({ to, href, label, prependBaseUrlToHref, ...props }) {
  const toUrl = useBaseUrl(to);
  const normalizedHref = useBaseUrl(href, { forcePrependBaseUrl: true });

  return (
    <Link
      className="footer__link-item"
      {...(href
        ? {
            target: '_blank',
            rel: 'noopener noreferrer',
            href: prependBaseUrlToHref ? normalizedHref : href,
          }
        : {
            to: toUrl,
          })}
      {...props}
    >
      {label}
    </Link>
  );
}

const Footer = () => {
  const { siteConfig } = useDocusaurusContext();
  const { themeConfig } = siteConfig;
  const { footer } = themeConfig || {};

  if (!footer) {
    return null;
  }

  const { copyright, links = [], logo = {} } = footer;

  return (
    <footer
      className={clsx('footer', {
        'footer--dark': footer.style === 'dark',
      })}
    >
      <div className="container container--fluid">
        <div className={clsx("row footer__links", styles.footerAdditionalLinks)}>
            <div className={clsx("col footer__col", styles.footerAbout)}>
              <h4 className="footer__title">About This Book</h4>
              <p>
                "Physical AI and Humanoid Robotics" explores the convergence of artificial intelligence with advanced robotics,
                focusing on creating intelligent, embodied systems. This book delves into the theoretical foundations,
                practical applications, and future implications of physical AI, providing comprehensive insights for researchers,
                engineers, and enthusiasts alike.
              </p>
            </div>
            <div className={clsx("col footer__col", styles.footerSocial)}>
                <h4 className="footer__title">Colaborate With Us</h4>
                <div className={styles.socialLinks}>
                    {links.find(linkItem => linkItem.title === 'Social')?.items?.map((item, key) => (
                        item.href ? (
                            <a key={key} href={item.href} target="_blank" rel="noopener noreferrer" className={styles.socialLink}>
                                {item.label}
                            </a>
                        ) : null
                    ))}
                </div>
            </div>
            {links.filter(linkItem => linkItem.title !== 'Social').map((linkItem, i) => (
              <div key={i} className="col footer__col">
                {linkItem.title != null ? (
                  <h4 className="footer__title">{linkItem.title}</h4>
                ) : null}
                {linkItem.items != null &&
                Array.isArray(linkItem.items) &&
                linkItem.items.length > 0 ? (
                  <ul className="footer__items">
                    {linkItem.items.map((item, key) =>
                      item.html ? (
                        <li
                          key={key}
                          className="footer__item"
                          // eslint-disable-next-line react/no-danger
                          dangerouslySetInnerHTML={{
                            __html: item.html,
                          }}
                        />
                      ) : (
                        <li key={item.href || item.to} className="footer__item">
                          <FooterLink {...item} />
                        </li>
                      ),
                    )}
                  </ul>
                ) : null}
              </div>
            ))}
          </div>
        
        {(logo || copyright) && (
          <div className="footer__bottom text--center">
            {logo && (
              <div className="margin-bottom--sm">
                {logo.href ? (
                  <Link href={logo.href} className={styles.footerLogoLink}>
                    <img
                      className={styles.footerLogo}
                      alt={logo.alt}
                      src={useBaseUrl(logo.src)}
                      {...(logo.srcDark && {
                        srcDark: useBaseUrl(logo.srcDark),
                      })}
                    />
                  </Link>
                ) : (
                  <img
                    className={styles.footerLogo}
                    alt={logo.alt}
                    src={useBaseUrl(logo.src)}
                    {...(logo.srcDark && {
                      srcDark: useBaseUrl(logo.srcDark),
                    })}
                  />
                )}
              </div>
            )}
            {copyright ? (
              <div
                className="footer__copyright"
                // eslint-disable-next-line react/no-danger
                dangerouslySetInnerHTML={{
                  __html: copyright,
                }}
              />
            ) : null}
          </div>
        )}
      </div>
    </footer>
  );
};

export default Footer;
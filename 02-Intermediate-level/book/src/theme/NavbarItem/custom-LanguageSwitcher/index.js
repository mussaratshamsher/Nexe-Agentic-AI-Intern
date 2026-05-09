import React from 'react';
import { useLocation } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

const CustomLanguageSwitcher = () => {
  const { i18n } = useDocusaurusContext();
  const { currentLocale, locales, localeConfigs } = i18n;
  const location = useLocation();

  const availableLanguages = locales.map((locale) => ({
    code: locale,
    label: localeConfigs[locale]?.label || locale,
  }));

  const getLocalePath = (targetLocale) => {
    const { pathname } = location;

    // If current locale is default (en), path doesn't have locale prefix
    // If target is default (en), remove any locale prefix
    // If target is non-default, add/replace locale prefix

    const defaultLocale = i18n.defaultLocale;

    // Remove current locale prefix if it exists
    let cleanPath = pathname;
    for (const locale of locales) {
      if (locale !== defaultLocale && pathname.startsWith(`/${locale}/`)) {
        cleanPath = pathname.substring(locale.length + 1);
        break;
      } else if (locale !== defaultLocale && pathname === `/${locale}`) {
        cleanPath = '/';
        break;
      }
    }

    // Add target locale prefix if not default
    if (targetLocale === defaultLocale) {
      return cleanPath || '/';
    } else {
      return `/${targetLocale}${cleanPath}`;
    }
  };

  const handleLanguageChange = (langCode) => {
    if (typeof window !== 'undefined') {
      const newPath = getLocalePath(langCode);
      window.location.href = newPath;
    }
  };

  return (
    <div className="navbar__item dropdown dropdown--hoverable">
      <a className="navbar__item navbar__link" href="#" onClick={(e) => e.preventDefault()}>
        {localeConfigs[currentLocale]?.label || currentLocale}
      </a>
      <ul className="dropdown__menu">
        {availableLanguages.map((lang) => (
          <li key={lang.code}>
            <a
              className={`dropdown__link ${currentLocale === lang.code ? 'dropdown__link--active' : ''}`}
              href={getLocalePath(lang.code)}
              onClick={(e) => {
                e.preventDefault();
                handleLanguageChange(lang.code);
              }}
            >
              {lang.label}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomLanguageSwitcher;

import React from 'react';
import NavbarItem from '@theme-original/NavbarItem';
import AuthButton from '@site/src/theme/AuthButton';
import LanguageSwitcher from './custom-LanguageSwitcher'; // Correctly import the switcher

export default function NavbarItemWrapper(props) {
  if (props.type === 'custom-AuthButton') {
    return <AuthButton {...props} />;
  }
  if (props.type === 'custom-LanguageSwitcher') {
    return <LanguageSwitcher {...props} />;
  }
  return <NavbarItem {...props} />;
}
import React, { useEffect, useState } from 'react';
import AuthContext from './AuthContext';
import firebase from '../firebase';
import { auth } from '../firebase/auth';

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (auth) {
      const unsubscribe = auth.onAuthStateChanged(user => {
        setUser(user);
        setLoading(false);
      });

      return () => unsubscribe();
    } else {
      setLoading(false);
    }
  }, []);

  const value = {
    user,
    loading,
    setUser,
    login: (email, password) => auth.signInWithEmailAndPassword(email, password),
    signup: async (email, password, displayName) => {
      const { user } = await auth.createUserWithEmailAndPassword(email, password);
      await user.updateProfile({ displayName });
      return user;
    },
    signInWithGoogle: () => {
      const provider = new firebase.auth.GoogleAuthProvider();
      return auth.signInWithPopup(provider);
    },
    logout: () => auth.signOut(),
    updatePassword: (password) => auth.currentUser.updatePassword(password),
    updateProfile: async (profile) => {
      await auth.currentUser.updateProfile(profile);
      const updatedUser = { ...auth.currentUser };
      setUser(updatedUser);
      return updatedUser;
    },
    updateProfilePicture: async (file) => {
      if (!auth.currentUser) return;
      const storage = firebase.storage();
      const fileRef = storage.ref(`profile-pics/${auth.currentUser.uid}`);
      await fileRef.put(file);
      const photoURL = await fileRef.getDownloadURL();
      await auth.currentUser.updateProfile({ photoURL });
      const updatedUser = { ...auth.currentUser };
      setUser(updatedUser);
      return updatedUser;
    },
    resetPassword: (email) => auth.sendPasswordResetEmail(email),
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;

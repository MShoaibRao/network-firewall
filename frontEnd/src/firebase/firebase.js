// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from 'firebase/firestore';
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDinRagS8ka9aPFv0NRSZHmvH9Voep2HU8",
  authDomain: "intellifirewall.firebaseapp.com",
  projectId: "intellifirewall",
  storageBucket: "intellifirewall.appspot.com",
  messagingSenderId: "777696736377",
  appId: "1:777696736377:web:9af1874e82ffd0643890a8",
  measurementId: "G-2Y519FSH20"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const firestore = getFirestore(app);

export { app, firestore };
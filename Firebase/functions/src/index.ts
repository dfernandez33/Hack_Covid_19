import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';
// initialize firebase app
admin.initializeApp({
    storageBucket: "hack-covid-19-e4018.appspot.com"
});

const db = admin.firestore();

import testRegistration = require("./testRegistration");

exports.testRegistration = functions.https.onCall((data, context) => {
    return testRegistration.handler(data, context, db);
});
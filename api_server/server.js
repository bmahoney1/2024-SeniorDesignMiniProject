const express = require('express');
const firebaseAdmin = require('firebase-admin');
const bodyParser = require('body-parser');

// Initialize Firebase Admin SDK
const serviceAccount = require('/Users/brennanmahoney/Downloads/miniproject-team-37-firebase-adminsdk-ia785-c9d7378d54.json');  // Ensure this path is correct

firebaseAdmin.initializeApp({
  credential: firebaseAdmin.credential.cert(serviceAccount)
});

const db = firebaseAdmin.firestore();  // For Firestore (or use firebaseAdmin.database() for Realtime DB)

// Create an Express application
const app = express();

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// Sign-up route using Firebase Admin SDK
app.post('/signup', async (req, res) => {
    const { email, password } = req.body;
  
    try {
      const userRecord = await firebaseAdmin.auth().createUser({
        email,
        password,
      });
      return res.status(200).json({ message: 'User created', userRecord });
    } catch (error) {
      return res.status(500).json({ error: error.message });
    }
});
  
// Login route (verify user credentials with Firebase Admin)
app.post('/login', async (req, res) => {
    const { email, password } = req.body;

    try {
        const user = await firebaseAdmin.auth().getUserByEmail(email);
        
        return res.status(200).json({ message: 'User exists', user });
    } catch (error) {
        return res.status(400).json({ error: 'User not found or invalid credentials' });
    }
});

app.get('/get_user_data/:uid', (req, res) => {
    const { uid } = req.params;
    const docRef = db.collection('scores').doc(uid);

    docRef.get()
        .then((doc) => {
            if (!doc.exists) {
                return res.status(404).send({ error: 'No data found for this user' });
            } else {
                return res.status(200).send(doc.data());
            }
        })
        .catch((error) => {
            console.error('Error retrieving data from Firebase:', error);
            return res.status(500).send({ error: 'Failed to retrieve data from Firebase' });
        });
});

// Define a POST route to handle score uploads
app.post('/upload_score', (req, res) => {
  const data = req.body;

  // Check if the required fields are present
  if (!data) {
    return res.status(400).send({ error: 'Invalid data or missing fields' });
  }

  const { Minimum, Maximum, Average, Score, timestamp } = data;
  // Convert numbers to strings
//   const scoreData = {
//     Minimum: String(data.Minimum),
//     Maximum: String(data.Maximum),
//     Average: String(data.Average),
//     Score: String(data.Score),
//   };

    const scoreData = {
        Minimum,
        Maximum,
        Average,
        Score
    };

  // Create a reference to the Firestore document
  const docRef = db.collection('scores').doc(timestamp);  // Use timestamp as document ID
  console.log(scoreData)
  // Save the data to Firestore
  docRef.set(scoreData)
    .then(() => {
      return res.status(200).send({ message: 'Data successfully uploaded to Firebase' });
    })
    .catch((error) => {
      console.error('Error writing to Firebase:', error);
      return res.status(500).send({ error: 'Failed to upload data to Firebase' });
    });
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

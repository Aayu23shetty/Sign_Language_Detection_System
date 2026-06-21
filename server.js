const express = require('express');
const mysql = require('mysql2');

// Create an instance of express
const app = express();
const port = 3000;

// Middleware for parsing JSON bodies
app.use(express.json());  // Use express's built-in JSON parser

// Create a connection pool to MySQL database
const db = mysql.createPool({
    host: 'localhost',        // Database host
    user: 'root',             // Database username
    password: '',             // Database password
    database: 'sign_language_detection' // Your database name (without spaces)
});

// Route for saving detections
app.post('/save-detection', (req, res) => {
    const { sign, confidence } = req.body;

    // Ensure that sign and confidence are provided
    if (!sign || !confidence) {
        return res.status(400).json({ error: 'Sign and confidence are required' });
    }

    // Insert the detection result into the database
    const query = 'INSERT INTO detections (sign, confidence) VALUES (?, ?)';
    db.query(query, [sign, confidence], (err, result) => {
        if (err) {
            console.error('Error inserting detection:', err);
            return res.status(500).json({ error: 'Failed to save detection' });
        }
        res.status(200).json({ message: 'Detection saved successfully', data: result });
    });
});

// Test route to check if the server is running
app.get('/', (req, res) => {
    res.send('Sign Language Detection Server is running!');
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});


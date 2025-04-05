// server.js

const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(bodyParser.json());

app.post('/api/deploy-bot', async (req, res) => {
  const { meetCode } = req.body;  

  if (!meetCode) {
    return res.status(400).json({ message: 'Put in a Google Meet Code' });
  }

  try {
    
    // Put backend stuff here

    const apiResponse = await axios.post('https://example.com/deploy-bot', { meetCode });

    // Send a success response
    return res.status(200).json({
      message: 'Bot deployed successfully!',
      data: apiResponse.data,
    });
  } catch (error) {
    console.error('Error deploying bot:', error);
    return res.status(500).json({ message: 'Failed to deploy bot' });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

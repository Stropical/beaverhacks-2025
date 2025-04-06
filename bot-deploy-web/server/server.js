const express = require('express');
const bodyParser = require('body-parser');
const puppeteer = require('puppeteer');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(bodyParser.json());

// Utility function to check if a Google Meet meeting exists
const checkMeetingExistence = async (meetCode) => {
  const meetUrl = `https://meet.google.com/${meetCode}`;

  // Launch Puppeteer to open the Google Meet page
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(meetUrl, { waitUntil: 'networkidle2' });

  // Check if the meeting exists (e.g., if we see a "Meeting not found" message or other indicators)
  const meetingExists = await page.evaluate(() => {
    return !document.body.innerText.includes('Meeting not found');
  });

  await browser.close();
  return meetingExists;
};

app.post('/api/deploy-bot', async (req, res) => {
  const { meetCode } = req.body;

  if (!meetCode) {
    return res.status(400).json({ message: 'Put in a Google Meet Code' });
  }

  try {
    // Check if the Google Meet meeting exists
    const meetingExists = await checkMeetingExistence(meetCode);

    if (!meetingExists) {
      return res.status(404).json({ message: 'Meeting not found or is inactive' });
    }

    // Proceed with your bot deployment (here's where you add the bot deployment logic)
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

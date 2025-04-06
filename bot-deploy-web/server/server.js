const express = require('express');
const bodyParser = require('body-parser');
const puppeteer = require('puppeteer');
const axios = require('axios');
const { exec } = require('child_process');
const path = require('path');

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
    
    // Put backend stuff here
    // Path to the batch script
    const scriptPath = path.join(__dirname, "..", "..", "deploy-bot.bat");

    // Execute the batch script with the meetCode as an argument
    exec(`"${scriptPath}" ${meetCode}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Execution error: ${error}`);
        return res.status(500).json({ message: 'Failed to deploy bot', error: error.message });
      }
      
      console.log(`Batch script output: ${stdout}`);
      
      if (stderr) {
        console.warn(`Batch script warnings: ${stderr}`);
      }
      
      return res.status(200).json({ 
        message: 'Bot deployment initiated', 
        meetCode,
        output: stdout
      });
    });
      } catch (error) {
        console.error(`Server error: ${error}`);
        return res.status(500).json({ message: 'Internal server error', error: error.message });
      }
  
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

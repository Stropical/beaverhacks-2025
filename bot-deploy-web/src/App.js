import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import logo from './logo.svg';

function App() {
  const [meetCode, setMeetCode] = useState('');
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState(null); // null, "success", "invalidFormat", "invalidId", "error"

  const handleCodeChange = (event) => {
    setMeetCode(event.target.value);
    setStatus(null);
    setMessage('');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const hyphenCount = (meetCode.match(/-/g) || []).length;

    // Check for 11-character length and exactly 2 hyphens
    if (meetCode.length !== 12 || hyphenCount !== 2) {
      setStatus('invalidFormat');
      setMessage('Invalid meeting code! Must be 11 characters and contain exactly 2 hyphens.');
      return;
    }

    try {
      // Check if meeting is valid
      const checkRes = await axios.get(`/api/check-meeting/${meetCode}`);
      if (!checkRes.data.valid) {
        setStatus('invalidId');
        setMessage('Invalid meeting ID! No such meeting found.');
        return;
      }

      // If valid, deploy the bot
      const deployRes = await axios.post('/api/deploy-bot', { meetCode });
      console.log(deployRes.data);
      setStatus('success');
      setMessage('Bot deployed successfully!');
    } catch (error) {
      console.error('Error during deployment:', error);
      setStatus('error');
      setMessage('An error occurred. Please try again.');
    }
  };

  return (
    <div className={`App ${status === 'success' ? 'fade-up' : ''}`}>
      <header className="App-header">
        <h1 className="Project-title">TeamDigest</h1>
        <img src={logo} className="App-logo" alt="logo" />
        <h1 className="App-title">Deploy SCRIBE here</h1>

        <form onSubmit={handleSubmit} className="App-form">
          <input
            type="text"
            value={meetCode}
            onChange={handleCodeChange}
            placeholder="Enter Google Meet Code"
            required
            className="App-input"
          />
          <button className="App-button" type="submit">
            Deploy Bot
          </button>
        </form>

        {status && (
          <div className={`popup-message ${status}`}>
            <p>{message}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;

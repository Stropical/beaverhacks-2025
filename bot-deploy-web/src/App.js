import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Assuming you'll modify this file
import logo from './logo.svg';

function App() {
  const [meetCode, setMeetCode] = useState('');

  const handleCodeChange = (event) => {
    setMeetCode(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('/api/deploy-bot', { meetCode });
      console.log(response.data);
    } catch (error) {
      console.error('Error deploying bot:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="Project-title" font-weight="bold">TeamDigest</h1>
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
      </header>
    </div>
  );
}

export default App;

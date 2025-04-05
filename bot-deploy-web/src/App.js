import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
import axios from 'axios';

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
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          <h1>Deploy SCRIBE here</h1>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={meetCode}
              onChange={handleCodeChange}
              placeholder="Enter Google Meet Code"
              required
            />
            <button>Click me</button>
          </form>
        </p>
      </header>
    </div>
  );
}

export default App;

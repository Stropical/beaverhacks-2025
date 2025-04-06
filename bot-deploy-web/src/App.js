import React, { useState, useEffect } from 'react';

function App() {
  const [meetCode, setMeetCode] = useState('');
  const [status, setStatus] = useState('idle'); // 'idle' | 'loading' | 'success' | 'error'
  const [errorMessage, setErrorMessage] = useState('');
  const [fadeIn, setFadeIn] = useState(false);

  useEffect(() => {
    setFadeIn(true);
  }, []);


  const handleCodeChange = (event) => {
    setMeetCode(event.target.value);
    setStatus('idle');
    setErrorMessage('');
  };

  const isValidMeetCode = (code) => {
    // Checks for format: 12 characters including exactly two hyphens, like "abc-def-ghij"
    const regex = /^[a-zA-Z0-9]{3}-[a-zA-Z0-9]{3}-[a-zA-Z0-9]{4}$/;
    return regex.test(code);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (meetCode.length !== 12) {
      setStatus('error');
      setErrorMessage('Invalid meeting code! The meeting code must be 12 characters including dashes.');
      return;
    }

    setStatus('loading');

    try {
      const response = await fetch('/api/deploy-bot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ meetCode }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log(data);
      setStatus('success');
    } catch (error) {
      console.error('Error deploying bot:', error);
      setStatus('error');
      setErrorMessage('Failed to deploy bot. Please try again.');
    }
  };

  return (
    <div style={styles.mainContainer}>
      <div style={styles.formContainer} className={`fade-down-init ${fadeIn ? 'fade-down' : ''}`}>
        <h1 style={styles.title}>TeamDigest</h1>
        <h2 style={styles.subtitle}>Deploy Scribe</h2>

        <form onSubmit={handleSubmit} style={styles.form}>
          <input
            type="text"
            value={meetCode}
            onChange={handleCodeChange}
            placeholder='e.g., "abc-def-ghij"'
            required
            style={styles.input}
          />

          <button
            type="submit"
            disabled={status === 'loading'}
            style={status === 'loading' ? { ...styles.button, ...styles.buttonDisabled } : styles.button}
          >
            {status === 'loading' ? 'Deploying...' : 'Deploy Bot'}
          </button>
        </form>

        {status === 'error' && (
          <div style={styles.errorAlert}>
            <div style={styles.alertIcon}>⚠️</div>
            <div>
              <div style={styles.alertTitle}>Error</div>
              <div style={styles.alertDescription}>{errorMessage}</div>
            </div>
          </div>
        )}

        {status === 'success' && (
          <div style={styles.successAlert}>
            <div style={styles.alertIcon}>✓</div>
            <div>
              <div style={styles.alertTitle}>Success</div>
              <div style={styles.alertDescription}>Bot successfully deployed!</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Inline styles object
const styles = {
  mainContainer: {
    display: 'flex',
    minHeight: '100vh',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '2rem',
    background: 'linear-gradient(to bottom right, #6366f1, #a855f7, #ec4899)',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
  },
  formContainer: {
    width: '100%',
    maxWidth: '28rem',
    backgroundColor: 'white',
    borderRadius: '1.5rem',
    boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    padding: '2rem',
    transition: 'transform 0.3s ease, box-shadow 0.3s ease, opacity 0.3s ease',
    ':hover': {
      transform: 'translateY(-5px)',
      boxShadow: '0 30px 60px -15px rgba(0, 0, 0, 0.3)',
    },
  },
  title: {
    fontSize: '3rem',
    fontWeight: '900',
    marginBottom: '4rem',
    textAlign: 'center',
    background: 'linear-gradient(to right, #6366f1, #a855f7, #ec4899)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
    color: 'transparent',
    transition: 'transform 0.3s ease',
    ':hover': {
      transform: 'scale(1.05)',
    },
  },
  subtitle: {
    fontSize: '1.5rem',
    fontWeight: '700',
    marginBottom: '1.2rem',
    textAlign: 'center',
    color: '#1f2937',
    transition: 'color 0.3s ease',
    ':hover': {
      color: '#6366f1',
    },
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1.5rem',
  },
  input: {
    width: '100%',
    fontSize: '1.125rem',
    padding: '0.75rem 1rem',
    borderRadius: '0.75rem',
    border: '1px solid #d1d5db',
    color: '#1f2937',
    outline: 'none',
    boxSizing: 'border-box',
    transition: 'border-color 0.3s ease, box-shadow 0.3s ease',
    ':hover': {
      borderColor: '#a855f7',
      boxShadow: '0 0 0 2px rgba(168, 85, 247, 0.2)',
    },
    ':focus': {
      borderColor: '#6366f1',
      boxShadow: '0 0 0 3px rgba(99, 102, 241, 0.3)',
    },
  },
  button: {
    width: '100%',
    fontSize: '1.125rem',
    padding: '1.5rem',
    borderRadius: '0.75rem',
    background: 'linear-gradient(to right, #6366f1, #a855f7, #ec4899)',
    color: 'white',
    fontWeight: '600',
    border: 'none',
    cursor: 'pointer',
    transition: 'opacity 0.2s ease, transform 0.2s ease, box-shadow 0.3s ease',
    ':hover': {
      transform: 'translateY(-2px)',
      boxShadow: '0 10px 25px -5px rgba(99, 102, 241, 0.5)',
    },
    ':active': {
      transform: 'translateY(1px)',
    },
  },
  buttonDisabled: {
    opacity: 0.7,
    cursor: 'not-allowed',
  },
  errorAlert: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '0.75rem',
    marginTop: '1.5rem',
    padding: '1rem',
    borderRadius: '0.5rem',
    backgroundColor: '#fee2e2',
    border: '1px solid #fecaca',
    color: '#b91c1c',
    transition: 'transform 0.2s ease',
    ':hover': {
      transform: 'scale(1.02)',
    },
  },
  successAlert: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '0.75rem',
    marginTop: '1.5rem',
    padding: '1rem',
    borderRadius: '0.5rem',
    backgroundColor: '#f0fdf4',
    border: '1px solid #dcfce7',
    color: '#166534',
    transition: 'transform 0.2s ease',
    ':hover': {
      transform: 'scale(1.02)',
    },
  },
  alertIcon: {
    fontSize: '1.25rem',
    lineHeight: '1.25rem',
  },
  alertTitle: {
    fontWeight: '600',
    fontSize: '0.875rem',
    marginBottom: '0.25rem',
  },
  alertDescription: {
    fontSize: '0.875rem',
  },
};

export default App;
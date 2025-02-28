import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState(''); // Stores what you type
  const [response, setResponse] = useState(''); // Stores Flask’s reply

  const sendMessage = async () => {
    try {
      console.log('Sending:', message);
      const res = await fetch('http://localhost:8080/chat', { // Changed to full URL
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: message }), // Flask expects "prompt"
      });
      console.log('Response status:', res.status);
      const data = await res.json();
      console.log('Response data:', data);
      setResponse(data.response); // Save the reply to show it
    } catch (error) {
      console.log('Error:', error);
      setResponse('Oops, something went wrong!'); // Show error to user
    }
  };

  return (
    <div className="App">
      <h1>Chatbot</h1>
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
      />
      <button onClick={sendMessage}>Send</button>
      <p>{response}</p>
    </div>
  );
}

export default App;
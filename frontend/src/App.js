import React, { useState } from 'react';
import './App.css'; // Forced redeploy

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const sendMessage = async () => {
    if (!message) {
      setResponse('Please type a message first!');
      return;
    }

    try {
      console.log('Sending message:', message);
      const payload = { prompt: message };
      console.log('Payload before JSON:', payload);
      const body = JSON.stringify(payload);
      console.log('Body after JSON:', body);
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8080';
      console.log('Fetching URL:', `${backendUrl}/chat`);

      const res = await fetch(`${backendUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: body,
      });

      console.log('Response status:', res.status);
      const data = await res.json();
      console.log('Response data:', data);

      if (res.status === 200) {
        setResponse(data.response);
      } else {
        setResponse(`Error: ${data.error}`);
      }
    } catch (error) {
      console.log('Fetch error:', error);
      setResponse('Oops, something went wrong! Check your connection.');
    }
  };

  return (
    <div className="App">
      <h1>Chatbot</h1>
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
        rows="4"
        style={{ width: '300px', margin: '10px' }}
      />
      <br />
      <button onClick={sendMessage}>Send</button>
      <p>{response}</p>
    </div>
  );
}

export default App;
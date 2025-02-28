import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState(''); // Stores what you type
  const [response, setResponse] = useState(''); // Stores the chatbot’s reply

  const sendMessage = async () => {
    if (!message) { // Check if you typed something
      setResponse('Please type a message first!');
      return;
    }

    try {
      console.log('Sending:', message); // Show what you typed
      const payload = { prompt: message }; // Create the data to send
      console.log('Payload:', payload); // Log the exact object
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8080'; // Get URL from .env
      const res = await fetch(`${backendUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }, // Tell Flask it’s JSON
        body: JSON.stringify(payload), // Send { "prompt": "your message" }
      });

      console.log('Response status:', res.status); // Show if it worked (200) or failed (400)
      const data = await res.json(); // Get Flask’s reply
      console.log('Response data:', data); // Log the full response

      if (res.status === 200) {
        setResponse(data.response); // Show ChatGPT’s answer
      } else {
        setResponse(`Error: ${data.error}`); // Show Flask’s error (e.g., "Missing prompt")
      }
    } catch (error) {
      console.log('Error:', error); // Log network problems
      setResponse('Oops, something went wrong! Check your connection.');
    }
  };

  return (
    <div className="App">
      <h1>Chatbot</h1>
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)} // Update message as you type
        placeholder="Type your message..."
        rows="4" // Make it taller
        style={{ width: '300px', margin: '10px' }} // Basic styling
      />
      <br />
      <button onClick={sendMessage}>Send</button>
      <p>{response}</p> // Show the reply or error
    </div>
  );
}

export default App;
import React, { useState } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return; // Prevent empty messages

    const newMessage = { role: "user", content: input };
    setMessages([...messages, newMessage]);

    try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();
      setMessages([...messages, newMessage, { role: "ai", content: data.response }]);
    } catch (error) {
      console.error("Error:", error);
    }

    setInput("");
  };

  return (
    <div style={{ maxWidth: "500px", margin: "auto", padding: "20px", textAlign: "center" }}>
      <h2>AI Chatbot</h2>
      <div
        style={{
          border: "1px solid #ddd",
          padding: "10px",
          height: "300px",
          overflowY: "auto",
          marginBottom: "10px",
        }}
      >
        {messages.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.role === "user" ? "right" : "left" }}>
            <b>{msg.role === "user" ? "You" : "AI"}:</b> {msg.content}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        style={{ width: "80%", padding: "5px" }}
        placeholder="Type a message..."
      />
      <button onClick={sendMessage} style={{ marginLeft: "10px", padding: "5px 10px" }}>
        Send
      </button>
    </div>
  );
}

export default App;

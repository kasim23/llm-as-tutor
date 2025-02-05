import React from 'react';
import ChatForm from '../components/ChatForm';

const Home = () => {
  const handleChatSubmit = async (question) => {
    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question })
      });
      const data = await response.json();
      return data.response;
    } catch (error) {
      console.error("Error fetching the answer:", error);
      return "Sorry, something went wrong.";
    }
  };

  return <ChatForm onSubmit={handleChatSubmit} />;
};

export default Home;

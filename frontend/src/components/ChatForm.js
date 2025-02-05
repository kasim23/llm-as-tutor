import React, { useState } from 'react';

const ChatForm = ({ onSubmit }) => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await onSubmit(question);
    setAnswer(response);
  };

  return (
    <div style={{ margin: '2rem' }}>
      <h1>LLM-Powered AWS Tutor</h1>
      <form onSubmit={handleSubmit}>
        <label>Ask an AWS question:</label><br />
        <input 
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={{ width: '300px', marginRight: '1rem' }}
        />
        <button type="submit">Submit</button>
      </form>
      {answer && (
        <div style={{ marginTop: '1rem', background: '#f9f9f9', padding: '1rem' }}>
          <strong>Answer:</strong> {answer}
        </div>
      )}
    </div>
  );
};

export default ChatForm;

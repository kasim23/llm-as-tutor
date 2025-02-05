import React, { useState } from 'react';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    // TODO: Call your backend API here
    // Example placeholder:
    setAnswer('This is where the LLM response will go.');
  }

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
}

export default App;

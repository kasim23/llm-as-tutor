import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App';

describe('App Component', () => {
  test('renders chat interface', () => {
    render(<App />);
    expect(screen.getByText('LLM-Powered AWS Tutor')).toBeInTheDocument();
  });

  test('submits question and displays response', async () => {
    const mockResponse = { response: 'Test answer about AWS' };
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockResponse),
      })
    );

    render(<App />);
    const input = screen.getByRole('textbox');
    const submitButton = screen.getByText('Submit');

    fireEvent.change(input, { target: { value: 'What is AWS?' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Test answer about AWS')).toBeInTheDocument();
    });
  });
});

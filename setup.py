import os
from pathlib import Path
import textwrap

def create_file(filepath: str, content: str = "") -> None:
    """Helper function to create a file with optional content.
    
    Args:
        filepath: Path where file should be created
        content: Optional content to write to file
    """
    # Use pathlib for more robust path handling
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Created {filepath}")

def create_structure(base_path: str, structure: dict) -> None:
    """Recursively create files and directories based on the structure dict."""
    for name, content in structure.items():
        full_path = Path(base_path) / name
        if isinstance(content, dict):
            full_path.mkdir(parents=True, exist_ok=True)
            create_structure(str(full_path), content)
        else:
            create_file(str(full_path), content)

def main() -> None:
    # Define project structure as a constant at module level
    PROJECT_STRUCTURE = {
        "backend": {
            "app": {
                "__init__.py": "",
                "main.py": textwrap.dedent("""\
                    # main.py
                    # Entry point for your Python backend (FastAPI, Flask, etc.)
                    
                    if __name__ == "__main__":
                        print("Backend entry point. Implement your app logic here.")
                """),
                "routes": {
                    "__init__.py": "",
                    "chat.py": textwrap.dedent("""\
                        from fastapi import APIRouter, HTTPException
                        from pydantic import BaseModel
                        from ..services.llm_service import get_answer

                        router = APIRouter()

                        class ChatRequest(BaseModel):
                            question: str

                        @router.post("/chat")
                        async def chat_endpoint(chat_request: ChatRequest):
                            answer = get_answer(chat_request.question)
                            if not answer:
                                raise HTTPException(status_code=404, detail="Answer not found")
                            return {"response": answer}
                    """),
                },
                "services": {
                    "__init__.py": "",
                    "llm_service.py": textwrap.dedent("""\
                        from ..utils.config import settings
                        import openai

                        def get_answer(question: str) -> str:
                            openai.api_key = settings.OPENAI_API_KEY
                            # Implement your LLM logic here. For demonstration, returning a placeholder.
                            response = f"Echoing your question: {question}"
                            return response
                    """),
                },
                "utils": {
                    "__init__.py": "",
                    "config.py": textwrap.dedent("""\
                        from pydantic import BaseSettings

                        class Settings(BaseSettings):
                            DATABASE_URL: str
                            OPENAI_API_KEY: str
                            VECTOR_DB_URL: str

                        settings = Settings()
                    """),
                },
            },
            "Dockerfile": textwrap.dedent("""\
                # Dockerfile for the backend
                FROM python:3.9-slim
                
                WORKDIR /app
                COPY requirements.txt requirements.txt
                RUN pip install --no-cache-dir -r requirements.txt
                COPY . .
                
                # Expose the port (e.g., 8000 for FastAPI/uvicorn)
                EXPOSE 8000
                
                # Adjust the CMD as needed for your framework, e.g., uvicorn
                CMD ["python", "main.py"]
            """),
            "requirements.txt": textwrap.dedent("""\
                # Python dependencies for the backend
                # e.g.:
                # fastapi
                # uvicorn
                # langchain
                # openai
            """),
        },
        "ingestion": {
            "ingest.py": textwrap.dedent("""\
                # ingest.py
                # Script or module to scrape and embed AWS docs, store in vector DB
                
                def main():
                    print("Document ingestion logic goes here.")
                
                if __name__ == "__main__":
                    main()
            """),
            "Dockerfile": textwrap.dedent("""\
                # Dockerfile for ingestion job
                FROM python:3.9-slim
                
                WORKDIR /ingestion
                COPY requirements.txt requirements.txt
                RUN pip install --no-cache-dir -r requirements.txt
                COPY . .
                CMD ["python", "ingest.py"]
            """),
        },
        "frontend": {
            "Dockerfile": textwrap.dedent("""\
                # Dockerfile for the frontend
                FROM node:18-alpine as build
                WORKDIR /app
                COPY package.json package-lock.json ./
                RUN npm install
                COPY . .
                RUN npm run build
                
                # Production stage
                FROM nginx:alpine
                COPY --from=build /app/build /usr/share/nginx/html
                EXPOSE 80
                CMD ["nginx", "-g", "daemon off;"]
            """),
            "package.json": textwrap.dedent("""\
                {
                  "name": "aws-tutor-frontend",
                  "version": "1.0.0",
                  "scripts": {
                    "start": "react-scripts start",
                    "build": "react-scripts build"
                  },
                  "dependencies": {
                    "react": "^18.0.0",
                    "react-dom": "^18.0.0"
                  }
                }
            """),
            "src": {
                "App.js": textwrap.dedent("""\
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
                """),
                "index.js": textwrap.dedent("""\
                    import React from 'react';
                    import ReactDOM from 'react-dom/client';
                    import App from './App';

                    const root = ReactDOM.createRoot(document.getElementById('root'));
                    root.render(
                      <React.StrictMode>
                        <App />
                      </React.StrictMode>
                    );
                """),
                "__tests__": {
                    "App.test.js": textwrap.dedent("""\
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
                    """)
                },
                "components": {
                    "ChatForm.js": textwrap.dedent("""\
                        import React from 'react';
                        
                        const ChatForm = ({ onSubmit }) => {
                          const handleSubmit = (e) => {
                            e.preventDefault();
                            const question = e.target.elements.question.value;
                            onSubmit(question);
                          };
                        
                          return (
                            <form onSubmit={handleSubmit}>
                              <input type="text" name="question" placeholder="Enter your question" />
                              <button type="submit">Send</button>
                            </form>
                          );
                        };
                        
                        export default ChatForm;
                    """)
                },
                "pages": {
                    "Home.js": textwrap.dedent("""\
                        import React from 'react';
                        
                        const Home = () => {
                          return (
                            <div>
                              <h2>Welcome to the AWS Tutor</h2>
                              <p>This is the home page.</p>
                            </div>
                          );
                        };
                        
                        export default Home;
                    """)
                },
                "styles": {
                    "App.css": textwrap.dedent("""\
                        /* App.css placeholder */
                        body {
                          margin: 0;
                          font-family: Arial, sans-serif;
                        }
                    """)
                }
            }
        },
        "k8s": {
            "deployment.yaml": textwrap.dedent("""\
                apiVersion: apps/v1
                kind: Deployment
                metadata:
                  name: aws-tutor-backend-deployment
                spec:
                  replicas: 1
                  selector:
                    matchLabels:
                      app: aws-tutor-backend
                  template:
                    metadata:
                      labels:
                        app: aws-tutor-backend
                    spec:
                      containers:
                      - name: aws-tutor-backend
                        image: <your-ecr-repo>/aws-tutor-backend:latest
                        ports:
                        - containerPort: 8000
            """),
            "service.yaml": textwrap.dedent("""\
                apiVersion: v1
                kind: Service
                metadata:
                  name: aws-tutor-backend-service
                spec:
                  selector:
                    app: aws-tutor-backend
                  ports:
                  - protocol: TCP
                    port: 80
                    targetPort: 8000
            """),
            "ingress.yaml": textwrap.dedent("""\
                apiVersion: networking.k8s.io/v1
                kind: Ingress
                metadata:
                  name: aws-tutor-ingress
                  annotations:
                    # example annotation for AWS ALB
                    kubernetes.io/ingress.class: alb
                spec:
                  rules:
                  - http:
                      paths:
                      - path: /
                        pathType: Prefix
                        backend:
                          service:
                            name: aws-tutor-backend-service
                            port:
                              number: 80
            """)
        },
        "backend/tests": {
            "__init__.py": "",
            "conftest.py": textwrap.dedent("""\
                import pytest
                import json
                
                @pytest.fixture
                def sample_aws_docs():
                    return {
                        "sample": "This is a test AWS documentation snippet"
                    }
                
                @pytest.fixture
                def mock_vector_store(sample_aws_docs):
                    # Setup mock vector store with test data
                    pass
            """),
            "test_api.py": textwrap.dedent("""\
                from fastapi.testclient import TestClient
                from main import app
                
                client = TestClient(app)
                
                def test_chat_endpoint():
                    response = client.post(
                        "/chat",
                        json={"question": "What is AWS Lambda?"}
                    )
                    assert response.status_code == 200
                    assert "response" in response.json()
            """),
            "test_llm_chain.py": textwrap.dedent("""\
                import pytest
                from unittest.mock import Mock, patch
                
                def test_placeholder():
                    # Add your LLM chain tests here
                    assert True
            """)
        },
        "ingestion/tests": {
            "__init__.py": "",
            "test_scraper.py": textwrap.dedent("""\
                import pytest
                
                def test_scraper():
                    # Add your scraper tests here
                    assert True
            """),
            "test_embeddings.py": textwrap.dedent("""\
                import pytest
                
                def test_embeddings():
                    # Add your embedding tests here
                    assert True
            """)
        }
    }

    TOP_LEVEL_FILES = {
        ".gitignore": textwrap.dedent("""\
            # .gitignore
            __pycache__/
            node_modules/
            .env
            *.pyc
            *.DS_Store
            .vscode/
            .idea/
        """),
        "README.md": textwrap.dedent("""\
            # LLM-Powered AWS Tutor

            This project is an MVP demonstrating a Retrieval-Augmented Generation (RAG) approach
            to building a chat-based AWS Tutor using GPT and AWS docs.

            ## Structure
            - **backend**: Python-based REST API (FastAPI/Flask) containerized with Docker.
            - **ingestion**: Scripts for scraping/embedding AWS docs and storing them in a vector DB.
            - **frontend**: React (or Next.js) app for the chat UI, containerized with Docker.
            - **k8s**: Kubernetes manifests for deploying on AWS EKS.
        """),
        "backend/pytest.ini": textwrap.dedent("""\
            [pytest]
            markers =
                unit: unit tests
                integration: integration tests
                regression: regression tests
            addopts = -v --tb=short
            testpaths = tests
        """),
        ".github": {
            "workflows": {
                "test.yml": textwrap.dedent("""\
                    name: Tests
                    
                    on: [push, pull_request]
                    
                    jobs:
                      test:
                        runs-on: ubuntu-latest
                        steps:
                          - uses: actions/checkout@v2
                          
                          - name: Set up Python
                            uses: actions/setup-python@v2
                            with:
                              python-version: '3.9'
                              
                          - name: Install dependencies
                            run: |
                              python -m pip install --upgrade pip
                              pip install -r backend/requirements.txt
                              pip install pytest pytest-cov
                              
                          - name: Run tests
                            run: |
                              cd backend
                              pytest --cov=. tests/
                              
                          - name: Frontend tests
                            run: |
                              cd frontend
                              npm install
                              npm test
                """)
            }
        }
    }

    # Update backend requirements.txt to include test dependencies
    PROJECT_STRUCTURE["backend"]["requirements.txt"] = textwrap.dedent("""\
        # Python dependencies for the backend
        fastapi
        uvicorn
        langchain
        openai
        pytest
        pytest-cov
        pytest-asyncio
        httpx
    """)

    # Create project files structure recursively
    create_structure(".", PROJECT_STRUCTURE)

    # Create top-level files (directories in keys are handled recursively)
    create_structure(".", TOP_LEVEL_FILES)

    print("Project structure created successfully!")

if __name__ == "__main__":
    main()

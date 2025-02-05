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

"""Comprehensive tests for embedder module."""
import pytest
from unittest.mock import patch, Mock
from logician.embedder import get_embedding


class TestGetEmbedding:
    """Test embedding generation"""
    
    def test_deterministic_pseudo_embedding(self):
        """Test deterministic pseudo embedding without LLM endpoint"""
        text = "Hello world"
        embedding1 = get_embedding(text)
        embedding2 = get_embedding(text)
        
        # Should be deterministic
        assert embedding1 == embedding2
        assert len(embedding1) == 128
        assert all(isinstance(v, float) for v in embedding1)
    
    def test_different_texts_different_embeddings(self):
        """Test different texts produce different embeddings"""
        emb1 = get_embedding("text one")
        emb2 = get_embedding("text two")
        
        assert emb1 != emb2
        assert len(emb1) == 128
        assert len(emb2) == 128
    
    def test_empty_text_embedding(self):
        """Test embedding for empty text"""
        embedding = get_embedding("")
        assert len(embedding) == 128
        assert all(isinstance(v, float) for v in embedding)
    
    @patch.dict('os.environ', {'LLM_ENDPOINT': 'http://localhost:8080'})
    @patch('logician.embedder.requests.post')
    def test_with_llm_endpoint_success(self, mock_post):
        """Test embedding with successful LLM endpoint"""
        mock_response = Mock()
        mock_response.json.return_value = {"embedding": [0.1] * 128}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        embedding = get_embedding("test text")
        
        assert embedding == [0.1] * 128
        mock_post.assert_called_once()
    
    @patch.dict('os.environ', {'LLM_ENDPOINT': 'http://localhost:8080', 'LLM_API_KEY': 'test-key'})
    @patch('logician.embedder.requests.post')
    def test_with_llm_endpoint_with_api_key(self, mock_post):
        """Test embedding with LLM endpoint and API key"""
        mock_response = Mock()
        mock_response.json.return_value = {"embedding": [0.2] * 128}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        embedding = get_embedding("test text")
        
        assert embedding == [0.2] * 128
        # Check that auth header was included
        call_kwargs = mock_post.call_args[1]
        assert "Authorization" in call_kwargs["headers"]
        assert call_kwargs["headers"]["Authorization"] == "Bearer test-key"
    
    @patch.dict('os.environ', {'LLM_ENDPOINT': 'http://localhost:8080'})
    @patch('logician.embedder.requests.post')
    def test_with_llm_endpoint_failure_fallback(self, mock_post):
        """Test fallback to pseudo embedding when LLM endpoint fails"""
        mock_post.side_effect = Exception("Connection failed")
        
        embedding = get_embedding("test text")
        
        # Should fallback to pseudo embedding
        assert len(embedding) == 128
        assert all(isinstance(v, float) for v in embedding)
    
    def test_unicode_text_embedding(self):
        """Test embedding with unicode characters"""
        text = "Hello 世界 🌍"
        embedding = get_embedding(text)
        
        assert len(embedding) == 128
        assert all(isinstance(v, float) for v in embedding)
    
    def test_long_text_embedding(self):
        """Test embedding with long text"""
        text = "word " * 1000
        embedding = get_embedding(text)
        
        assert len(embedding) == 128
        assert all(isinstance(v, float) for v in embedding)

"""Comprehensive tests for RAG orchestrator."""
import pytest
from unittest.mock import patch, Mock, MagicMock
from logician.rag import RagOrchestrator


class TestRagOrchestrator:
    """Test RAG orchestrator functionality"""
    
    def test_init_default(self):
        """Test initialization with defaults"""
        rag = RagOrchestrator()
        assert rag.collection == "log_entries"
        assert rag.qdrant is not None
    
    def test_init_custom_collection(self):
        """Test initialization with custom collection"""
        rag = RagOrchestrator(collection="custom_logs")
        assert rag.collection == "custom_logs"
    
    @patch('logician.rag.get_embedding')
    @patch.object(RagOrchestrator, '__init__', lambda self, collection="log_entries": setattr(self, 'collection', collection) or setattr(self, 'qdrant', MagicMock()) or setattr(self, 'llm_endpoint', None) or setattr(self, 'llm_api_key', None))
    def test_retrieve_no_hits(self, mock_embedding):
        """Test retrieve with no search hits"""
        mock_embedding.return_value = [0.1] * 128
        
        rag = RagOrchestrator()
        rag.qdrant.search = Mock(return_value=[])
        
        hits = rag.retrieve("test query")
        assert hits == []
    
    @patch('logician.rag.get_embedding')
    @patch.object(RagOrchestrator, '__init__', lambda self, collection="log_entries": setattr(self, 'collection', collection) or setattr(self, 'qdrant', MagicMock()) or setattr(self, 'llm_endpoint', None) or setattr(self, 'llm_api_key', None))
    def test_retrieve_with_hits(self, mock_embedding):
        """Test retrieve with search hits"""
        mock_embedding.return_value = [0.1] * 128
        mock_hits = [
            {"id": "1", "score": 0.9, "payload": {"text": "result 1"}},
            {"id": "2", "score": 0.8, "payload": {"text": "result 2"}}
        ]
        
        rag = RagOrchestrator()
        rag.qdrant.search = Mock(return_value=mock_hits)
        
        hits = rag.retrieve("test query", top_k=2)
        assert len(hits) == 2
        assert hits[0]["score"] == 0.9
    
    def test_call_llm_without_endpoint(self):
        """Test call_llm without LLM endpoint (fallback)"""
        rag = RagOrchestrator()
        result = rag.call_llm("test prompt")
        
        assert "[LLM placeholder]" in result
        assert "test prompt" in result or "test prompt"[:200] in result
    
    @patch.dict('os.environ', {'LLM_ENDPOINT': 'http://localhost:8080'})
    @patch('logician.rag.requests.post')
    def test_call_llm_with_endpoint_success(self, mock_post):
        """Test call_llm with successful LLM endpoint"""
        mock_response = Mock()
        mock_response.json.return_value = {"text": "LLM generated response"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        rag = RagOrchestrator()
        result = rag.call_llm("test prompt")
        
        assert result == "LLM generated response"
        mock_post.assert_called_once()
    
    @patch.dict('os.environ', {'LLM_ENDPOINT': 'http://localhost:8080', 'LLM_API_KEY': 'test-key'})
    @patch('logician.rag.requests.post')
    def test_call_llm_with_api_key(self, mock_post):
        """Test call_llm with API key"""
        mock_response = Mock()
        mock_response.json.return_value = {"text": "response"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        rag = RagOrchestrator()
        result = rag.call_llm("prompt")
        
        call_kwargs = mock_post.call_args[1]
        assert "Authorization" in call_kwargs["headers"]
    
    @patch.dict('os.environ', {'LLM_ENDPOINT': 'http://localhost:8080'})
    @patch('logician.rag.requests.post')
    def test_call_llm_with_endpoint_failure(self, mock_post):
        """Test call_llm fallback when endpoint fails"""
        mock_post.side_effect = Exception("Connection failed")
        
        rag = RagOrchestrator()
        result = rag.call_llm("test prompt")
        
        assert "[LLM placeholder]" in result
    
    @patch('logician.rag.get_embedding')
    @patch.object(RagOrchestrator, '__init__', lambda self, collection="log_entries": setattr(self, 'collection', collection) or setattr(self, 'qdrant', MagicMock()) or setattr(self, 'llm_endpoint', None) or setattr(self, 'llm_api_key', None))
    def test_answer_integration(self, mock_embedding):
        """Test answer method integration"""
        mock_embedding.return_value = [0.1] * 128
        mock_hits = [{"payload": {"text": "context 1"}}]
        
        rag = RagOrchestrator()
        rag.qdrant.search = Mock(return_value=mock_hits)
        
        answer = rag.answer("What is the weather?")
        
        assert isinstance(answer, str)
        assert len(answer) > 0
    
    @patch('logician.rag.get_embedding')
    @patch.object(RagOrchestrator, '__init__', lambda self, collection="log_entries": setattr(self, 'collection', collection) or setattr(self, 'qdrant', MagicMock()) or setattr(self, 'llm_endpoint', None) or setattr(self, 'llm_api_key', None))
    def test_answer_with_dict_hits(self, mock_embedding):
        """Test answer with dictionary hits"""
        mock_embedding.return_value = [0.1] * 128
        mock_hits = [
            {"payload": {"text": "result 1"}},
            {"payload": {"text": "result 2"}}
        ]
        
        rag = RagOrchestrator()
        rag.qdrant.search = Mock(return_value=mock_hits)
        
        answer = rag.answer("test query")
        assert "[LLM placeholder]" in answer
    
    @patch('logician.rag.get_embedding')
    @patch.object(RagOrchestrator, '__init__', lambda self, collection="log_entries": setattr(self, 'collection', collection) or setattr(self, 'qdrant', MagicMock()) or setattr(self, 'llm_endpoint', None) or setattr(self, 'llm_api_key', None))
    def test_answer_with_empty_hits(self, mock_embedding):
        """Test answer with no hits"""
        mock_embedding.return_value = [0.1] * 128
        
        rag = RagOrchestrator()
        rag.qdrant.search = Mock(return_value=[])
        
        answer = rag.answer("test query")
        assert isinstance(answer, str)

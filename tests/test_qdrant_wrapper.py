"""Comprehensive tests for QdrantWrapper."""
import pytest
from unittest.mock import patch, Mock, MagicMock
from logician.qdrant_wrapper import QdrantWrapper


class TestQdrantWrapper:
    """Test Qdrant wrapper functionality"""
    
    def test_init_without_qdrant_client(self):
        """Test initialization without qdrant-client installed"""
        wrapper = QdrantWrapper()
        assert wrapper.url == "http://localhost:6333"  # default
        assert wrapper.api_key is None
    
    def test_init_with_custom_url(self):
        """Test initialization with custom URL"""
        wrapper = QdrantWrapper(url="http://custom:6333")
        assert wrapper.url == "http://custom:6333"
    
    @patch.dict('os.environ', {'QDRANT_URL': 'http://env:6333', 'QDRANT_API_KEY': 'test-key'})
    def test_init_from_env(self):
        """Test initialization from environment variables"""
        wrapper = QdrantWrapper()
        assert wrapper.url == "http://env:6333"
        assert wrapper.api_key == "test-key"
    
    def test_create_collection_without_client(self):
        """Test create_collection when client not available"""
        wrapper = QdrantWrapper()
        # Should not raise error even without client
        wrapper.create_collection("test_collection")
    
    def test_upsert_without_client(self):
        """Test upsert when client not available"""
        wrapper = QdrantWrapper()
        # Should not raise error even without client
        wrapper.upsert("test", ["id1"], [[0.1]*128], [{"key": "value"}])
    
    def test_search_without_client(self):
        """Test search when client not available"""
        wrapper = QdrantWrapper()
        # Should return empty list when client not available
        results = wrapper.search("test", [0.1]*128)
        assert results == []
    
    def test_create_collection_skipped_without_qdrant(self):
        """Test create_collection is skipped when qdrant-client not available"""
        # This test verifies the graceful fallback behavior
        wrapper = QdrantWrapper()
        # Should not raise error
        wrapper.create_collection("test_collection", vector_size=256)
    
    @patch('logician.qdrant_wrapper._HAS_QDRANT', True)
    @patch('logician.qdrant_wrapper.QdrantClient')
    def test_upsert_with_client(self, mock_client_class):
        """Test upsert with qdrant-client available"""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        wrapper = QdrantWrapper()
        ids = ["id1", "id2"]
        vectors = [[0.1]*128, [0.2]*128]
        metadatas = [{"text": "one"}, {"text": "two"}]
        
        wrapper.upsert("test", ids, vectors, metadatas)
        
        mock_client.upsert.assert_called_once()
        call_args = mock_client.upsert.call_args
        assert call_args[1]["collection_name"] == "test"
        assert len(call_args[1]["points"]) == 2
    
    @patch('logician.qdrant_wrapper._HAS_QDRANT', True)
    @patch('logician.qdrant_wrapper.QdrantClient')
    def test_search_with_client(self, mock_client_class):
        """Test search with qdrant-client available"""
        mock_client = MagicMock()
        mock_result = [{"id": "1", "score": 0.9, "payload": {"text": "result"}}]
        mock_client.search.return_value = mock_result
        mock_client_class.return_value = mock_client
        
        wrapper = QdrantWrapper()
        results = wrapper.search("test", [0.1]*128, top_k=3)
        
        assert results == mock_result
        mock_client.search.assert_called_once()
        call_args = mock_client.search.call_args
        assert call_args[1]["collection_name"] == "test"
        assert call_args[1]["limit"] == 3

"""Comprehensive tests for CLI module."""
import pytest
from unittest.mock import patch, Mock
from logician.cli import main
import sys


class TestCLI:
    """Test CLI functionality"""
    
    @patch('logician.cli.RagOrchestrator')
    @patch('sys.argv', ['logician', 'What is the weather?'])
    def test_main_basic_query(self, mock_rag_class):
        """Test main with basic query"""
        mock_rag = Mock()
        mock_rag.answer.return_value = "It's sunny today"
        mock_rag_class.return_value = mock_rag
        
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called_once_with("It's sunny today")
    
    @patch('logician.cli.RagOrchestrator')
    @patch('sys.argv', ['logician', 'Tell me about Python'])
    def test_main_different_query(self, mock_rag_class):
        """Test main with different query"""
        mock_rag = Mock()
        mock_rag.answer.return_value = "Python is a programming language"
        mock_rag_class.return_value = mock_rag
        
        with patch('builtins.print') as mock_print:
            main()
            assert mock_rag.answer.called
            assert mock_rag.answer.call_args[0][0] == "Tell me about Python"
    
    @patch('sys.argv', ['logician'])
    def test_main_no_query(self):
        """Test main without query argument"""
        with pytest.raises(SystemExit):
            main()
    
    @patch('logician.cli.RagOrchestrator')
    @patch('sys.argv', ['logician', 'Query with multiple words'])
    def test_main_multiword_query(self, mock_rag_class):
        """Test main with multi-word query"""
        mock_rag = Mock()
        mock_rag.answer.return_value = "Response"
        mock_rag_class.return_value = mock_rag
        
        with patch('builtins.print'):
            main()
            assert mock_rag.answer.call_args[0][0] == "Query with multiple words"

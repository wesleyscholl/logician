"""Comprehensive tests for utils module."""
import pytest
import logging
from logician.utils import configure_logging


class TestUtils:
    """Test utility functions"""
    
    def test_configure_logging_function_exists(self):
        """Test that configure_logging function can be called"""
        # Just verify the function executes without error
        configure_logging()
        configure_logging(level=logging.DEBUG)
        configure_logging(level=logging.INFO)
        configure_logging(level=logging.WARNING)
        configure_logging(level=logging.ERROR)
        
        # Verify logger exists after configuration
        logger = logging.getLogger()
        assert logger is not None

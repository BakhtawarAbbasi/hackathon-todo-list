"""
Test configuration for the Todo application tests.
"""

import pytest
from src.services.task_manager import TaskManager


@pytest.fixture
def task_manager():
    """
    Fixture to provide a fresh TaskManager instance for each test.
    """
    return TaskManager()
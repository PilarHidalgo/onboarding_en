"""Models package initialization"""
from .base import DataTransferable, BaseModel
from .fruit import Fruit

__all__ = [
    'DataTransferable',
    'BaseModel',
    'Fruit'
]

# Version of the models package
__version__ = '1.0.0'

# Package metadata
__author__ = 'Your Name'
__email__ = 'your.email@example.com'
__description__ = 'Data models for the Fruit Store Management System'
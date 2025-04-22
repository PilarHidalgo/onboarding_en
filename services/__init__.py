"""Services package initialization"""
from .base_service import BaseService
from .fruit_service import FruitService
from .file_service import FileService

__all__ = [
    'BaseService',
    'FruitService',
    'FileService',
    'initialize_services'
]

# Version of the services package
__version__ = '1.0.0'

# Package metadata
__author__ = 'Your Name'
__email__ = 'your.email@example.com'
__description__ = 'Business logic services for the Fruit Store Management System'

def initialize_services(repositories):
    """Initialize all services
    
    This function creates service instances using the provided repositories.
    
    Args:
        repositories: Tuple containing all repositories
            (fruit_repository,)
        
    Returns:
        Tuple containing all initialized services
            (fruit_service, file_service)
    """
    # Unpack repositories
    fruit_repository, = repositories
    
    # Initialize services
    fruit_service = FruitService(fruit_repository)
    file_service = FileService(fruit_repository)
    
    # Return all services
    return (fruit_service, file_service)
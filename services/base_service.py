"""Base service implementation for business logic operations"""
from typing import TypeVar, Generic, List, Optional, Type, Any, Dict
import logging

from models.base import DataTransferable
from database.base_repository import BaseRepository

T = TypeVar('T', bound=DataTransferable)

class BaseService(Generic[T]):
    """Base service class for business logic operations
    
    Generic service pattern implementation for business logic operations
    on model objects that implement the DataTransferable interface.
    
    Attributes:
        repository: Repository for data access
        model_class: Class of the model this service handles
    """
    
    def __init__(
        self, 
        repository: BaseRepository[T],
        model_class: Type[T]
    ):
        """Initialize the service
        
        Args:
            repository: Repository for data access
            model_class: Class of the model this service handles
        """
        self.repository = repository
        self.model_class = model_class
        self.logger = logging.getLogger(__name__)
    
    def get_by_id(self, id_value: int) -> Optional[T]:
        """Get a model by its ID
        
        Args:
            id_value: ID of the model to retrieve
            
        Returns:
            Model instance or None if not found
            
        Raises:
            ValueError: If ID is invalid
        """
        if not isinstance(id_value, int) or id_value <= 0:
            raise ValueError(f"Invalid ID: {id_value}")
            
        try:
            return self.repository.find_by_id(id_value)
        except Exception as e:
            self.logger.error(f"Error retrieving {self.model_class.__name__} with ID {id_value}: {e}")
            raise
    
    def get_all(self) -> List[T]:
        """Get all models
        
        Returns:
            List of all model instances
        """
        try:
            return self.repository.find_all()
        except Exception as e:
            self.logger.error(f"Error retrieving all {self.model_class.__name__} instances: {e}")
            raise
    
    def create(self, data: Dict[str, Any]) -> T:
        """Create a new model
        
        Args:
            data: Dictionary containing model data
            
        Returns:
            Created model instance
            
        Raises:
            ValueError: If data is invalid
        """
        try:
            # Validate data
            self._validate_model_data(data)
            
            # Create model instance
            model = self.model_class.from_dict(data)
            
            # Save to repository
            created_model = self.repository.create(model)
            
            if not created_model:
                raise ValueError(f"Failed to create {self.model_class.__name__}")
                
            return created_model
        except Exception as e:
            self.logger.error(f"Error creating {self.model_class.__name__}: {e}")
            raise
    
    def update(self, id_value: int, data: Dict[str, Any]) -> Optional[T]:
        """Update an existing model
        
        Args:
            id_value: ID of the model to update
            data: Dictionary containing updated model data
            
        Returns:
            Updated model instance or None if not found
            
        Raises:
            ValueError: If ID or data is invalid
        """
        if not isinstance(id_value, int) or id_value <= 0:
            raise ValueError(f"Invalid ID: {id_value}")
            
        try:
            # Check if model exists
            existing_model = self.repository.find_by_id(id_value)
            if not existing_model:
                return None
                
            # Validate data
            self._validate_model_data(data, update=True)
            
            # Update model with new data
            for key, value in data.items():
                if hasattr(existing_model, key):
                    setattr(existing_model, key, value)
            
            # Save to repository
            updated_model = self.repository.update(existing_model)
            
            if not updated_model:
                raise ValueError(f"Failed to update {self.model_class.__name__} with ID {id_value}")
                
            return updated_model
        except Exception as e:
            self.logger.error(f"Error updating {self.model_class.__name__} with ID {id_value}: {e}")
            raise
    
    def delete(self, id_value: int) -> bool:
        """Delete a model
        
        Args:
            id_value: ID of the model to delete
            
        Returns:
            True if deleted successfully, False otherwise
            
        Raises:
            ValueError: If ID is invalid
        """
        if not isinstance(id_value, int) or id_value <= 0:
            raise ValueError(f"Invalid ID: {id_value}")
            
        try:
            # Check if model exists
            if not self.repository.exists(id_value):
                return False
                
            # Delete from repository
            return self.repository.delete(id_value)
        except Exception as e:
            self.logger.error(f"Error deleting {self.model_class.__name__} with ID {id_value}: {e}")
            raise
    
    def count(self) -> int:
        """Count the number of models
        
        Returns:
            Number of models
        """
        try:
            return self.repository.count()
        except Exception as e:
            self.logger.error(f"Error counting {self.model_class.__name__} instances: {e}")
            raise
    
    def _validate_model_data(self, data: Dict[str, Any], update: bool = False) -> None:
        """Validate model data
        
        Args:
            data: Dictionary containing model data
            update: Whether this is an update operation
            
        Raises:
            ValueError: If data is invalid
        """
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
            
        # Basic validation - override in subclasses for specific validation
        required_fields = self._get_required_fields()
        
        # For updates, we don't require all fields
        if not update:
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    def _get_required_fields(self) -> List[str]:
        """Get required fields for the model
        
        Returns:
            List of required field names
        """
        # Override in subclasses to specify required fields
        return []
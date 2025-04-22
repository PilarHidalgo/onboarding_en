"""Base models and interfaces for data transfer objects"""
from abc import ABC, abstractmethod
from typing import Optional, Tuple, Dict, Any, TypeVar, Type, Generic

T = TypeVar('T', bound='DataTransferable')

class DataTransferable(ABC):
    """Interface for objects that can be converted to/from data structures"""
    
    @classmethod
    @abstractmethod
    def from_tuple(cls: Type[T], data_tuple: Optional[Tuple]) -> Optional[T]:
        """Create an object from a tuple representation
        
        Args:
            data_tuple: Tuple containing data to create object from
            
        Returns:
            Instance of class or None if data_tuple is None
        """
        pass
    
    @abstractmethod
    def to_tuple(self) -> Tuple:
        """Convert object to a tuple representation
        
        Returns:
            Tuple containing object data
        """
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert object to a dictionary representation
        
        Returns:
            Dictionary containing object data
        """
        pass


class BaseModel(DataTransferable):
    """Base class for models with common functionality"""
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create an object from a dictionary
        
        Args:
            data: Dictionary containing object data
            
        Returns:
            Instance of class initialized with dictionary data
        """
        return cls(**data)
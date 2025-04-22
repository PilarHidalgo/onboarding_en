# File: app.py
"""
Fruit Store Management System - Main Application
A Streamlit application for managing fruit inventory.
"""
import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Protocol, Tuple, Type

import streamlit as st
import pandas as pd

from config import AppConfig
from models.fruit import Fruit
from services.database_service import DatabaseService
from services.file_service import FileService
from services.fruit_service import FruitService
from ui.components import UIComponents
from ui.pages.inventory_page import InventoryPage
from ui.pages.add_fruit_page import AddFruitPage
from ui.pages.update_fruit_page import UpdateFruitPage
from ui.pages.delete_fruit_page import DeleteFruitPage


class LoggingService:
    """Service for application logging with configurable handlers"""
    
    @staticmethod
    def configure(
        level: int = logging.ERROR,
        log_format: str = '%(asctime)s - %(levelname)s - %(message)s',
        log_file: str = 'app.log'
    ) -> None:
        """Configure application logging with file and console handlers
        
        Args:
            level: Logging level (default: ERROR)
            log_format: Format string for log messages
            log_file: Path to log file
        """
        handlers = [
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
        
        logging.basicConfig(
            level=level,
            format=log_format,
            handlers=handlers
        )


class Page(Protocol):
    """Protocol defining the interface for application pages"""
    
    def render(self) -> None:
        """Render the page content"""
        ...


class PageFactory:
    """Factory for creating application pages"""
    
    @staticmethod
    def create_pages(
        fruit_service: FruitService,
        file_service: FileService,
        ui_components: UIComponents
    ) -> Dict[str, Page]:
        """Create all application pages
        
        Args:
            fruit_service: Service for fruit operations
            file_service: Service for file operations
            ui_components: UI components for rendering
            
        Returns:
            Dictionary mapping page names to page instances
        """
        return {
            "View Inventory": InventoryPage(fruit_service, ui_components),
            "Add Fruit": AddFruitPage(fruit_service, file_service, ui_components),
            "Update Fruit": UpdateFruitPage(fruit_service, file_service, ui_components),
            "Delete Fruit": DeleteFruitPage(fruit_service, ui_components)
        }


class AppConfiguration:
    """Configuration manager for Streamlit application"""
    
    @staticmethod
    def configure_page() -> None:
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title=AppConfig.PAGE_TITLE,
            page_icon=AppConfig.PAGE_ICON,
            layout=AppConfig.LAYOUT
        )


class NavigationManager:
    """Manager for application navigation"""
    
    def __init__(self, pages: Dict[str, Page]):
        """Initialize with available pages
        
        Args:
            pages: Dictionary mapping page names to page instances
        """
        self.pages = pages
        self.current_page_name = None
    
    def setup_sidebar(self) -> None:
        """Set up the sidebar navigation menu"""
        st.sidebar.title("Fruit Store Management")
        self.current_page_name = st.sidebar.selectbox(
            "Choose an action", 
            list(self.pages.keys())
        )
        
        # Add footer information
        st.sidebar.markdown("---")
        st.sidebar.info(f"{AppConfig.APP_NAME} v{AppConfig.VERSION}")
    
    def get_current_page(self) -> Optional[Page]:
        """Get the currently selected page
        
        Returns:
            The current page instance or None if not set
        """
        if self.current_page_name and self.current_page_name in self.pages:
            return self.pages[self.current_page_name]
        return None


class ServiceLocator:
    """Service locator for application dependencies"""
    
    _instance = None
    _services = {}
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of the service locator"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def register(self, service_name: str, service_instance: object) -> None:
        """Register a service
        
        Args:
            service_name: Name of the service
            service_instance: Instance of the service
        """
        self._services[service_name] = service_instance
    
    def get(self, service_name: str) -> Optional[object]:
        """Get a registered service
        
        Args:
            service_name: Name of the service
            
        Returns:
            The service instance or None if not found
        """
        return self._services.get(service_name)


class FruitStoreApp:
    """Main application class implementing the Facade pattern"""
    
    def __init__(self):
        """Initialize the application and its dependencies"""
        # Configure logging
        LoggingService.configure()
        
        # Configure Streamlit page
        AppConfiguration.configure_page()
        
        # Initialize service locator
        self.service_locator = ServiceLocator.get_instance()
        
        # Initialize and register services
        self._initialize_services()
        
        # Initialize pages using factory
        pages = PageFactory.create_pages(
            self.service_locator.get("fruit_service"),
            self.service_locator.get("file_service"),
            self.service_locator.get("ui_components")
        )
        
        # Initialize navigation
        self.navigation = NavigationManager(pages)
    
    def _initialize_services(self) -> None:
        """Initialize and register all application services"""
        # Create services
        db_service = DatabaseService()
        file_service = FileService(AppConfig.IMAGE_DIR)
        fruit_service = FruitService(db_service)
        ui_components = UIComponents()
        
        # Register services in the service locator
        self.service_locator.register("db_service", db_service)
        self.service_locator.register("file_service", file_service)
        self.service_locator.register("fruit_service", fruit_service)
        self.service_locator.register("ui_components", ui_components)
    
    def run(self) -> None:
        """Run the application - set up navigation and display the selected page"""
        # Set up navigation sidebar
        self.navigation.setup_sidebar()
        
        # Get and render the current page
        current_page = self.navigation.get_current_page()
        if current_page:
            current_page.render()


# Entry point of the application
if __name__ == "__main__":
    app = FruitStoreApp()
    app.run()

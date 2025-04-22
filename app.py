# File: app.py
"""
Fruit Store Management System - Main Application
A Streamlit application for managing fruit inventory.
"""
import logging
import os
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any

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

# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

class FruitStoreApp:
    """Main application class implementing the Facade pattern"""
    
    def __init__(self):
        """Initialize the application and its dependencies"""
        # Configure the Streamlit page
        st.set_page_config(
            page_title=AppConfig.PAGE_TITLE,
            page_icon=AppConfig.PAGE_ICON,
            layout=AppConfig.LAYOUT
        )
        
        # Initialize services (Dependency Injection)
        self.db_service = DatabaseService()
        self.file_service = FileService(AppConfig.IMAGE_DIR)
        self.fruit_service = FruitService(self.db_service)
        
        # Initialize UI components
        self.ui = UIComponents()
        
        # Initialize pages (Strategy Pattern)
        self.pages = {
            "View Inventory": InventoryPage(self.fruit_service, self.ui),
            "Add Fruit": AddFruitPage(self.fruit_service, self.file_service, self.ui),
            "Update Fruit": UpdateFruitPage(self.fruit_service, self.file_service, self.ui),
            "Delete Fruit": DeleteFruitPage(self.fruit_service, self.ui)
        }
        
        # Create sidebar navigation
        self._setup_sidebar()
    
    def _setup_sidebar(self) -> None:
        """Set up the sidebar navigation menu"""
        st.sidebar.title("Fruit Store Management")
        self.current_page = st.sidebar.selectbox(
            "Choose an action", 
            list(self.pages.keys())
        )
        
        # Add footer information
        st.sidebar.markdown("---")
        st.sidebar.info(f"{AppConfig.APP_NAME} v{AppConfig.VERSION}")
    
    def run(self) -> None:
        """Run the application - display the selected page"""
        # Get the appropriate page based on selection and render it
        current_page = self.pages[self.current_page]
        current_page.render()


# Entry point of the application
if __name__ == "__main__":
    app = FruitStoreApp()
    app.run()

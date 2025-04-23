"""UI module initialization for the fruit inventory management application.

This module provides the user interface components for the application,
including the main application window, pages, and reusable UI components.
"""

import tkinter as tk
from tkinter import ttk
import logging
import os
import sys

# Configure logging for UI module
logger = logging.getLogger(__name__)

# Import UI components
from app import FruitInventoryApp
from ui.page import Page
from ui.components import (
    StatusBar,
    SearchBar,
    DataTable,
    FilterPanel,
    ConfirmDialog,
    InfoDialog,
    ErrorDialog,
    WarningDialog,
    LoadingOverlay,
    Pagination,
    SortableHeader,
    ToolTip
)

# Import pages
from ui.pages import (
    InventoryPage,
    AddFruitPage,
    UpdateFruitPage,
    DeleteFruitPage,
    DashboardPage,
    SettingsPage,
    AboutPage,
    LoginPage,
    PAGE_CLASSES
)

# Setup custom styles
def setup_styles():
    """Setup custom styles for the application"""
    style = ttk.Style()
    
    # Configure default theme
    if sys.platform.startswith('win'):
        style.theme_use('vista')
    elif sys.platform.startswith('darwin'):
        style.theme_use('aqua')
    else:
        style.theme_use('clam')
    
    # Configure common styles
    style.configure('TFrame', background='#f5f5f5')
    style.configure('TLabel', background='#f5f5f5')
    style.configure('TButton', padding=6)
    style.configure('TEntry', padding=6)
    
    # Configure header style
    style.configure('Header.TFrame', background='#3498db')
    style.configure('Header.TLabel', background='#3498db', foreground='white', font=('TkDefaultFont', 12, 'bold'))
    
    # Configure footer style
    style.configure('Footer.TFrame', background='#f0f0f0')
    style.configure('Footer.TLabel', background='#f0f0f0')
    
    # Configure content style
    style.configure('Content.TFrame', background='white')
    
    # Configure button styles
    style.configure('Primary.TButton', background='#3498db', foreground='white')
    style.configure('Success.TButton', background='#2ecc71', foreground='white')
    style.configure('Danger.TButton', background='#e74c3c', foreground='white')
    style.configure('Warning.TButton', background='#f39c12', foreground='white')
    
    # Configure table styles
    style.configure('Table.TFrame', background='white')
    style.configure('Table.TLabel', background='white')
    style.configure('TableHeader.TLabel', background='#e0e0e0', font=('TkDefaultFont', 10, 'bold'))
    
    # Configure alternating row colors for tables
    style.configure('EvenRow.TFrame', background='white')
    style.configure('OddRow.TFrame', background='#f9f9f9')
    
    # Configure selected row style
    style.configure('Selected.TFrame', background='#d4e6f1')
    
    logger.debug("Custom styles configured")

# Function to start the UI
def start_application(config=None):
    """Start the fruit inventory management application
    
    Args:
        config: Application configuration
    
    Returns:
        The application instance
    """
    # Setup styles
    setup_styles()
    
    # Create root window
    root = tk.Tk()
    root.title("Fruit Inventory Management")
    
    # Set window size and position
    window_width = 1024
    window_height = 768
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Set window icon if available
    icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.png')
    if os.path.exists(icon_path):
        try:
            icon = tk.PhotoImage(file=icon_path)
            root.iconphoto(True, icon)
        except Exception as e:
            logger.warning(f"Failed to load application icon: {e}")
    
    # Create and start application
    app = FruitInventoryApp(root, config)
    
    logger.info("Application UI initialized")
    
    return app

__all__ = [
    # Main application
    'FruitInventoryApp',
    'start_application',
    
    # Base classes
    'Page',
    
    # Components
    'StatusBar',
    'SearchBar',
    'DataTable',
    'FilterPanel',
    'ConfirmDialog',
    'InfoDialog',
    'ErrorDialog',
    'WarningDialog',
    'LoadingOverlay',
    'Pagination',
    'SortableHeader',
    'ToolTip',
    
    # Pages
    'InventoryPage',
    'AddFruitPage',
    'UpdateFruitPage',
    'DeleteFruitPage',
    'DashboardPage',
    'SettingsPage',
    'AboutPage',
    'LoginPage',
    'PAGE_CLASSES',
    
    # Styles
    'setup_styles'
]
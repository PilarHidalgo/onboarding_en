"""Configuration module for the Fruit Inventory Management application.

This module provides configuration management for the application,
including loading configuration from files, environment variables,
and command-line arguments.
"""

import os
import sys
import json
import logging
import argparse
from typing import Dict, Any, Optional
from dataclasses import dataclass, field, asdict
import logging.config

# Default configuration values
DEFAULT_CONFIG = {
    # Application settings
    "app": {
        "name": "Fruit Inventory Management",
        "version": "1.0.0",
        "debug": False,
        "theme": "default",
        "language": "en",
        "auto_save": True,
        "save_interval": 300,  # seconds
        "max_recent_files": 5,
        "startup_page": "InventoryPage"
    },
    
    # Database settings
    "database": {
        "type": "sqlite",
        "path": "data/inventory.db",
        "backup_dir": "data/backups",
        "backup_count": 5,
        "auto_backup": True,
        "backup_interval": 86400,  # 24 hours in seconds
        "connection_timeout": 30,
        "connection_retries": 3
    },
    
    # Logging settings
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "logs/app.log",
        "max_size": 10485760,  # 10 MB
        "backup_count": 3,
        "console_output": True
    },
    
    # UI settings
    "ui": {
        "width": 1024,
        "height": 768,
        "fullscreen": False,
        "font_family": "",  # System default
        "font_size": 10,
        "table_rows_per_page": 15,
        "confirm_exit": True,
        "show_tooltips": True,
        "animation_speed": 200,  # milliseconds
        "double_click_action": "edit"
    },
    
    # Feature flags
    "features": {
        "enable_dashboard": True,
        "enable_reports": True,
        "enable_export": True,
        "enable_import": True,
        "enable_notifications": True,
        "enable_auto_update": True,
        "enable_cloud_sync": False
    }
}

@dataclass
class AppConfig:
    """Application configuration settings"""
    name: str = "Fruit Inventory Management"
    version: str = "1.0.0"
    debug: bool = False
    theme: str = "default"
    language: str = "en"
    auto_save: bool = True
    save_interval: int = 300
    max_recent_files: int = 5
    startup_page: str = "InventoryPage"

@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    type: str = "sqlite"
    path: str = "data/inventory.db"
    backup_dir: str = "data/backups"
    backup_count: int = 5
    auto_backup: bool = True
    backup_interval: int = 86400
    connection_timeout: int = 30
    connection_retries: int = 3

@dataclass
class LoggingConfig:
    """Logging configuration settings"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: str = "logs/app.log"
    max_size: int = 10485760
    backup_count: int = 3
    console_output: bool = True

@dataclass
class UIConfig:
    """UI configuration settings"""
    width: int = 1024
    height: int = 768
    fullscreen: bool = False
    font_family: str = ""
    font_size: int = 10
    table_rows_per_page: int = 15
    confirm_exit: bool = True
    show_tooltips: bool = True
    animation_speed: int = 200
    double_click_action: str = "edit"

@dataclass
class FeatureConfig:
    """Feature flag configuration"""
    enable_dashboard: bool = True
    enable_reports: bool = True
    enable_export: bool = True
    enable_import: bool = True
    enable_notifications: bool = True
    enable_auto_update: bool = True
    enable_cloud_sync: bool = False

@dataclass
class Config:
    """Main configuration class"""
    app: AppConfig = field(default_factory=AppConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    features: FeatureConfig = field(default_factory=FeatureConfig)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'Config':
        """Create a Config instance from a dictionary
        
        Args:
            config_dict: Dictionary containing configuration values
            
        Returns:
            Config instance
        """
        app_config = AppConfig(**config_dict.get("app", {}))
        db_config = DatabaseConfig(**config_dict.get("database", {}))
        logging_config = LoggingConfig(**config_dict.get("logging", {}))
        ui_config = UIConfig(**config_dict.get("ui", {}))
        feature_config = FeatureConfig(**config_dict.get("features", {}))
        
        return cls(
            app=app_config,
            database=db_config,
            logging=logging_config,
            ui=ui_config,
            features=feature_config
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Config instance to dictionary
        
        Returns:
            Dictionary representation of the configuration
        """
        return {
            "app": asdict(self.app),
            "database": asdict(self.database),
            "logging": asdict(self.logging),
            "ui": asdict(self.ui),
            "features": asdict(self.features)
        }
    
    def save(self, filepath: str) -> None:
        """Save configuration to a JSON file
        
        Args:
            filepath: Path to save the configuration file
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save configuration to file
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)


def load_config(config_file: Optional[str] = None) -> Config:
    """Load configuration from file, environment variables, and command-line arguments
    
    Args:
        config_file: Path to configuration file (optional)
        
    Returns:
        Config instance
    """
    # Start with default configuration
    config_dict = DEFAULT_CONFIG.copy()
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Fruit Inventory Management")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], 
                        help="Set logging level")
    parser.add_argument("--db-path", help="Path to database file")
    args = parser.parse_args()
    
    # Use provided config file or default
    config_file = args.config or config_file or "config.json"
    
    # Load configuration from file if it exists
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                
                # Update configuration with file values
                for section, values in file_config.items():
                    if section in config_dict:
                        config_dict[section].update(values)
        except Exception as e:
            print(f"Error loading configuration file: {e}")
    
    # Override with environment variables
    _update_from_env(config_dict)
    
    # Override with command-line arguments
    if args.debug:
        config_dict["app"]["debug"] = True
    
    if args.log_level:
        config_dict["logging"]["level"] = args.log_level
    
    if args.db_path:
        config_dict["database"]["path"] = args.db_path
    
    # Create Config instance
    config = Config.from_dict(config_dict)
    
    # Setup logging
    _setup_logging(config.logging)
    
    return config


def _update_from_env(config_dict: Dict[str, Any]) -> None:
    """Update configuration from environment variables
    
    Environment variables should be in the format:
    FRUIT_APP_DEBUG=true
    FRUIT_DATABASE_PATH=/path/to/db
    
    Args:
        config_dict: Configuration dictionary to update
    """
    prefix = "FRUIT_"
    
    for key, value in os.environ.items():
        if key.startswith(prefix):
            # Remove prefix and split into section and option
            key_parts = key[len(prefix):].lower().split('_', 1)
            
            if len(key_parts) == 2:
                section, option = key_parts
                
                # Check if section and option exist in config
                if section in config_dict and option in config_dict[section]:
                    # Convert value to appropriate type
                    original_value = config_dict[section][option]
                    
                    if isinstance(original_value, bool):
                        config_dict[section][option] = value.lower() in ('true', 'yes', '1')
                    elif isinstance(original_value, int):
                        try:
                            config_dict[section][option] = int(value)
                        except ValueError:
                            pass
                    elif isinstance(original_value, float):
                        try:
                            config_dict[section][option] = float(value)
                        except ValueError:
                            pass
                    else:
                        config_dict[section][option] = value


def _setup_logging(logging_config: LoggingConfig) -> None:
    """Setup logging configuration
    
    Args:
        logging_config: Logging configuration
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(logging_config.file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': logging_config.format
            },
        },
        'handlers': {
            'file': {
                'level': logging_config.level,
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': logging_config.file,
                'maxBytes': logging_config.max_size,
                'backupCount': logging_config.backup_count,
                'formatter': 'standard',
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['file'],
                'level': logging_config.level,
                'propagate': True
            }
        }
    }
    
    # Add console handler if enabled
    if logging_config.console_output:
        log_config['handlers']['console'] = {
            'level': logging_config.level,
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        }
        log_config['loggers']['']['handlers'].append('console')
    
    # Apply logging configuration
    logging.config.dictConfig(log_config)


# Create a global configuration instance
config = load_config()
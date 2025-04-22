"""Delete Fruit page implementation for removing fruits from inventory"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Dict, Any, Optional

from models import Fruit
from ui.page import Page
from ui.components import StatusBar, ConfirmDialog

class DeleteFruitPage(Page):
    """Delete Fruit page for removing fruits from inventory
    
    This page displays fruit details and provides confirmation
    for deleting fruits from the inventory.
    
    Attributes:
        parent: Parent widget
        controller: Application controller
    """
    
    def __init__(self, parent: tk.Widget, controller: Any):
        """Initialize the delete fruit page
        
        Args:
            parent: Parent widget
            controller: Application controller
        """
        super().__init__(parent, controller)
        self.logger = logging.getLogger(__name__)
        self.current_fruit = None
        self.fruit_id = None
        self.detail_labels = {}
    
    def _init_ui(self) -> None:
        """Initialize UI components"""
        # Create main layout frames
        self.header_frame = self.create_header("Delete Fruit")
        self.content_frame = self.create_content_frame()
        self.footer_frame = self.create_footer()
        
        # Configure content frame layout
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Create warning message
        self._create_warning_message()
        
        # Create fruit details display
        self._create_fruit_details()
        
        # Create action buttons
        self._create_action_buttons()
        
        # Create status bar
        self.status_bar = StatusBar(self.footer_frame)
        self.status_bar.grid(row=0, column=0, sticky="ew")
        self.status_bar.set_status("Select a fruit to delete")
    
    def _create_warning_message(self) -> None:
        """Create warning message"""
        warning_frame = ttk.Frame(self.content_frame)
        warning_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        # Warning icon
        warning_icon = ttk.Label(warning_frame, text="⚠️", font=("TkDefaultFont", 24))
        warning_icon.grid(row=0, column=0, padx=10, pady=10)
        
        # Warning message
        warning_message = ttk.Label(
            warning_frame, 
            text="You are about to delete a fruit from the inventory.\n"
                 "This action cannot be undone. Please review the details below.",
            wraplength=400,
            justify="left"
        )
        warning_message.grid(row=0, column=1, sticky="w", padx=10, pady=10)
    
    def _create_fruit_details(self) -> None:
        """Create fruit details display"""
        # Create details frame
        self.details_frame = ttk.LabelFrame(self.content_frame, text="Fruit Details")
        self.details_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.details_frame.grid_columnconfigure(1, weight=1)
        
        # Create detail fields
        fields = [
            ("id", "ID:"),
            ("name", "Name:"),
            ("category", "Category:"),
            ("price", "Price ($):"),
            ("quantity", "Quantity:"),
            ("description", "Description:"),
            ("origin", "Origin:"),
            ("organic", "Organic:"),
            ("season", "Season:"),
            ("created_at", "Created:"),
            ("updated_at", "Updated:")
        ]
        
        for i, (field_name, label_text) in enumerate(fields):
            # Create label
            label = ttk.Label(self.details_frame, text=label_text)
            label.grid(row=i, column=0, sticky="w", padx=(10, 5), pady=5)
            
            # Create value label
            value_label = ttk.Label(self.details_frame, text="", font=("TkDefaultFont", 10, "bold"))
            value_label.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            
            # Store reference
            self.detail_labels[field_name] = value_label
    
    def _create_action_buttons(self) -> None:
        """Create action buttons"""
        button_frame = ttk.Frame(self.content_frame)
        button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        # Delete button
        self.delete_button = ttk.Button(
            button_frame,
            text="Delete",
            command=self._on_delete,
            style="Danger.TButton",
            state="disabled"
        )
        self.delete_button.grid(row=0, column=0, sticky="e", padx=5)
        
        # Cancel button
        cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel
        )
        cancel_button.grid(row=0, column=1, sticky="w", padx=5)
    
    def load_fruit(self, fruit_id: int) -> None:
        """Load a fruit for deletion
        
        Args:
            fruit_id: ID of the fruit to load
        """
        try:
            # Show progress
            self.status_bar.set_status("Loading fruit...")
            self.status_bar.start_progress()
            
            # Get fruit from service
            fruit = self.controller.fruit_service.get_by_id(fruit_id)
            
            if not fruit:
                self.status_bar.stop_progress()
                self.status_bar.set_status("Fruit not found")
                self.show_error(f"Fruit with ID {fruit_id} not found")
                return
            
            # Store current fruit
            self.current_fruit = fruit
            self.fruit_id = fruit_id
            
            # Update details frame title
            self.details_frame.config(text=f"Fruit Details - {fruit.name}")
            
            # Display fruit details
            self._display_fruit_details(fruit)
            
            # Enable delete button
            self.delete_button.config(state="normal")
            
            # Stop progress
            self.status_bar.stop_progress()
            self.status_bar.set_status(f"Ready to delete: {fruit.name}")
            
        except Exception as e:
            # Stop progress
            self.status_bar.stop_progress()
            self.status_bar.set_status("Error loading fruit")
            
            # Log error
            self.logger.error(f"Error loading fruit: {e}")
            
            # Show error message
            self.show_error(f"Failed to load fruit: {str(e)}")
    
    def _display_fruit_details(self, fruit: Fruit) -> None:
        """Display fruit details
        
        Args:
            fruit: Fruit object to display
        """
        # Display basic fields
        self.detail_labels["id"].config(text=str(fruit.id) if fruit.id else "")
        self.detail_labels["name"].config(text=fruit.name or "")
        self.detail_labels["category"].config(text=fruit.category or "")
        self.detail_labels["price"].config(text=f"${fruit.price:.2f}" if fruit.price is not None else "")
        self.detail_labels["quantity"].config(text=str(fruit.quantity) if fruit.quantity is not None else "")
        self.detail_labels["description"].config(text=fruit.description or "")
        self.detail_labels["origin"].config(text=fruit.origin or "")
        self.detail_labels["organic"].config(text="Yes" if fruit.organic else "No")
        self.detail_labels["season"].config(text=fruit.season or "")
        
        # Format dates
        created_at = fruit.created_at.strftime("%Y-%m-%d %H:%M:%S") if fruit.created_at else ""
        updated_at = fruit.updated_at.strftime("%Y-%m-%d %H:%M:%S") if fruit.updated_at else ""
        
        self.detail_labels["created_at"].config(text=created_at)
        self.detail_labels["updated_at"].config(text=updated_at)
        
        # Highlight low stock in red if applicable
        if fruit.quantity is not None and fruit.quantity < 10:
            self.detail_labels["quantity"].config(foreground="red")
        else:
            self.detail_labels["quantity"].config(foreground="black")
    
    def _on_delete(self) -> None:
        """Handle delete button click"""
        if not self.current_fruit:
            return
        
        # Show confirmation dialog
        ConfirmDialog(
            self,
            title="Confirm Deletion",
            message=f"Are you sure you want to permanently delete '{self.current_fruit.name}'?\n\n"
                   f"This action cannot be undone.",
            on_confirm=self._confirm_delete,
            on_cancel=lambda: self.status_bar.set_status(f"Deletion cancelled")
        )
    
    def _confirm_delete(self) -> None:
        """Handle deletion confirmation"""
        if not self.current_fruit:
            return
            
        try:
            # Show progress
            self.status_bar.set_status("Deleting fruit...")
            self.status_bar.start_progress()
            
            # Delete fruit
            fruit_name = self.current_fruit.name
            self.controller.fruit_service.delete(self.current_fruit.id)
            
            # Stop progress
            self.status_bar.stop_progress()
            self.status_bar.set_status(f"Fruit '{fruit_name}' deleted successfully")
            
            # Show success message
            self.show_info(f"Fruit '{fruit_name}' deleted successfully")
            
            # Reset page
            self._reset_page()
            
            # Navigate back to inventory page after short delay
            self.after(2000, lambda: self.controller.show_page("InventoryPage"))
            
        except Exception as e:
            # Stop progress
            self.status_bar.stop_progress()
            self.status_bar.set_status("Error deleting fruit")
            
            # Log error
            self.logger.error(f"Error deleting fruit: {e}")
            
            # Show error message
            self.show_error(f"Failed to delete fruit: {str(e)}")
    
    def _on_cancel(self) -> None:
        """Handle cancel button click"""
        # Navigate back to inventory page
        self.controller.show_page("InventoryPage")
    
    def _reset_page(self) -> None:
        """Reset page state"""
        # Clear current fruit
        self.current_fruit = None
        self.fruit_id = None
        
        # Reset details frame title
        self.details_frame.config(text="Fruit Details")
        
        # Clear detail labels
        for field_name, label in self.detail_labels.items():
            label.config(text="")
            if field_name == "quantity":
                label.config(foreground="black")
        
        # Disable delete button
        self.delete_button.config(state="disabled")
        
        # Reset status
        self.status_bar.set_status("Select a fruit to delete")
    
    def _setup_bindings(self) -> None:
        """Set up event bindings"""
        # Add keyboard shortcut for delete (Delete key)
        self.bind_all("<Delete>", lambda e: self._on_delete() if self.delete_button["state"] == "normal" else None)
        
        # Add keyboard shortcut for cancel (Escape)
        self.bind_all("<Escape>", lambda e: self._on_cancel())
    
    def on_show(self) -> None:
        """Called when the page is shown"""
        super().on_show()
        
        # Check if fruit ID is provided in controller
        fruit_id = self.controller.get_context("selected_fruit_id")
        if fruit_id:
            # Load fruit
            self.load_fruit(fruit_id)
        else:
            # Reset page
            self._reset_page()
    
    def on_hide(self) -> None:
        """Called when the page is hidden"""
        super().on_hide()
        # Unbind keyboard shortcuts
        self.unbind_all("<Delete>")
        self.unbind_all("<Escape>")
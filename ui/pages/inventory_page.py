"""Inventory page implementation for fruit inventory management"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Dict, Any, List, Optional

from models import Fruit
from ui.page import Page
from ui.components import SearchBar, FilterPanel, StatusBar, ConfirmDialog, DataEntryForm

class InventoryPage(Page):
    """Inventory page for managing fruit inventory
    
    This page displays the fruit inventory in a table and provides
    functionality for adding, editing, and deleting fruits, as well
    as searching and filtering the inventory.
    
    Attributes:
        parent: Parent widget
        controller: Application controller
    """
    
    def __init__(self, parent: tk.Widget, controller: Any):
        """Initialize the inventory page
        
        Args:
            parent: Parent widget
            controller: Application controller
        """
        super().__init__(parent, controller)
        self.logger = logging.getLogger(__name__)
        self.current_fruits = []
        self.selected_fruit_id = None
    
    def _init_ui(self) -> None:
        """Initialize UI components"""
        # Create main layout frames
        self.header_frame = self.create_header("Fruit Inventory")
        self.content_frame = self.create_content_frame()
        self.footer_frame = self.create_footer()
        
        # Configure content frame layout
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Create toolbar with search and filters
        self._create_toolbar()
        
        # Create inventory table
        self._create_inventory_table()
        
        # Create action buttons
        self._create_action_buttons()
        
        # Create status bar
        self.status_bar = StatusBar(self.footer_frame)
        self.status_bar.grid(row=0, column=0, sticky="ew")
    
    def _create_toolbar(self) -> None:
        """Create toolbar with search and filters"""
        toolbar_frame = ttk.Frame(self.content_frame)
        toolbar_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        toolbar_frame.grid_columnconfigure(0, weight=1)
        
        # Create search bar
        self.search_bar = SearchBar(
            toolbar_frame,
            on_search=self._on_search,
            placeholder="Search by name or category..."
        )
        self.search_bar.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # Create filter panel
        filters = {
            'category': {
                'type': 'combobox',
                'label': 'Category',
                'options': ['Citrus', 'Berries', 'Tropical', 'Stone Fruit', 'Other']
            },
            'price_range': {
                'type': 'range',
                'label': 'Price Range'
            },
            'in_stock': {
                'type': 'checkbox',
                'label': 'In Stock Only',
                'default': False
            }
        }
        
        self.filter_panel = FilterPanel(
            toolbar_frame,
            on_filter=self._on_filter,
            filters=filters
        )
        self.filter_panel.grid(row=0, column=1, sticky="e")
    
    def _create_inventory_table(self) -> None:
        """Create inventory table"""
        # Create table frame
        table_frame = ttk.Frame(self.content_frame)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # Define columns
        columns = [
            {'id': 'id', 'text': 'ID', 'width': 50},
            {'id': 'name', 'text': 'Name', 'width': 150},
            {'id': 'category', 'text': 'Category', 'width': 100},
            {'id': 'price', 'text': 'Price ($)', 'width': 80},
            {'id': 'quantity', 'text': 'Quantity', 'width': 80},
            {'id': 'created_at', 'text': 'Created', 'width': 120},
            {'id': 'updated_at', 'text': 'Updated', 'width': 120}
        ]
        
        # Create table
        self.inventory_table = self.create_data_table(table_frame, columns)
        
        # Configure selection event
        self.inventory_table.bind("<<TreeviewSelect>>", self._on_fruit_selected)
        
        # Configure double-click event for editing
        self.inventory_table.bind("<Double-1>", self._on_edit_fruit)
    
    def _create_action_buttons(self) -> None:
        """Create action buttons"""
        button_frame = ttk.Frame(self.content_frame)
        button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        # Create buttons
        buttons = [
            {
                'text': 'Add Fruit',
                'command': self._on_add_fruit,
                'style': 'Primary.TButton'
            },
            {
                'text': 'Edit Fruit',
                'command': self._on_edit_fruit
            },
            {
                'text': 'Delete Fruit',
                'command': self._on_delete_fruit
            },
            {
                'text': 'Import',
                'command': self._on_import
            },
            {
                'text': 'Export',
                'command': self._on_export
            },
            {
                'text': 'Refresh',
                'command': self.refresh
            }
        ]
        
        self.create_button_group(button_frame, buttons)
    
    def refresh(self) -> None:
        """Refresh the inventory table"""
        try:
            # Get all fruits from service
            fruits = self.controller.fruit_service.get_all()
            self.current_fruits = fruits
            
            # Apply search and filters
            filtered_fruits = self._apply_filters(fruits)
            
            # Update table
            self._update_table(filtered_fruits)
            
            # Update status
            self.status_bar.set_status(f"Showing {len(filtered_fruits)} of {len(fruits)} fruits")
            
        except Exception as e:
            self.logger.error(f"Error refreshing inventory: {e}")
            self.show_error(f"Failed to refresh inventory: {str(e)}")
    
    def _update_table(self, fruits: List[Fruit]) -> None:
        """Update the inventory table with fruits
        
        Args:
            fruits: List of fruits to display
        """
        # Clear table
        self.inventory_table.delete(*self.inventory_table.get_children())
        
        # Add fruits to table
        for fruit in fruits:
            # Format dates
            created_at = fruit.created_at.strftime("%Y-%m-%d %H:%M") if fruit.created_at else ""
            updated_at = fruit.updated_at.strftime("%Y-%m-%d %H:%M") if fruit.updated_at else ""
            
            # Format price
            price_str = f"${fruit.price:.2f}" if fruit.price is not None else ""
            
            # Determine row tag based on quantity
            tag = "low_stock" if fruit.quantity is not None and fruit.quantity < 10 else ""
            
            # Insert row
            self.inventory_table.insert(
                "", 
                "end", 
                values=(
                    fruit.id,
                    fruit.name,
                    fruit.category,
                    price_str,
                    fruit.quantity,
                    created_at,
                    updated_at
                ),
                tags=(tag,)
            )
        
        # Configure row colors
        self.inventory_table.tag_configure("low_stock", background="#FFCCCC")
    
    def _on_search(self, query: str) -> None:
        """Handle search event
        
        Args:
            query: Search query
        """
        # Apply filters with search query
        filtered_fruits = self._apply_filters(self.current_fruits, query)
        
        # Update table
        self._update_table(filtered_fruits)
        
        # Update status
        self.status_bar.set_status(f"Showing {len(filtered_fruits)} of {len(self.current_fruits)} fruits")
    
    def _on_filter(self, filter_values: Dict[str, Any]) -> None:
        """Handle filter event
        
        Args:
            filter_values: Dictionary of filter values
        """
        # Get search query
        query = self.search_bar.get_query()
        
        # Apply filters with search query
        filtered_fruits = self._apply_filters(self.current_fruits, query)
        
        # Update table
        self._update_table(filtered_fruits)
        
        # Update status
        self.status_bar.set_status(f"Showing {len(filtered_fruits)} of {len(self.current_fruits)} fruits")
    
    def _apply_filters(self, fruits: List[Fruit], search_query: str = "") -> List[Fruit]:
        """Apply filters and search to fruits
        
        Args:
            fruits: List of fruits to filter
            search_query: Search query
            
        Returns:
            Filtered list of fruits
        """
        filtered_fruits = fruits
        
        # Apply search query if provided
        if search_query:
            search_query = search_query.lower()
            filtered_fruits = [
                fruit for fruit in filtered_fruits
                if (fruit.name and search_query in fruit.name.lower()) or
                   (fruit.category and search_query in fruit.category.lower())
            ]
        
        # Apply filters if filter panel exists
        if hasattr(self, 'filter_panel'):
            filter_values = self.filter_panel.get_filter_values()
            
            # Filter by category
            if 'category' in filter_values and filter_values['category']:
                category = filter_values['category']
                filtered_fruits = [
                    fruit for fruit in filtered_fruits
                    if fruit.category == category
                ]
            
            # Filter by price range
            if 'price_range' in filter_values:
                price_range = filter_values['price_range']
                
                if price_range.get('min'):
                    try:
                        min_price = float(price_range['min'])
                        filtered_fruits = [
                            fruit for fruit in filtered_fruits
                            if fruit.price is not None and fruit.price >= min_price
                        ]
                    except ValueError:
                        pass
                
                if price_range.get('max'):
                    try:
                        max_price = float(price_range['max'])
                        filtered_fruits = [
                            fruit for fruit in filtered_fruits
                            if fruit.price is not None and fruit.price <= max_price
                        ]
                    except ValueError:
                        pass
            
            # Filter by in-stock status
            if 'in_stock' in filter_values and filter_values['in_stock']:
                filtered_fruits = [
                    fruit for fruit in filtered_fruits
                    if fruit.quantity is not None and fruit.quantity > 0
                ]
        
        return filtered_fruits
    
    def _on_fruit_selected(self, event) -> None:
        """Handle fruit selection event"""
        selection = self.inventory_table.selection()
        if selection:
            # Get selected item
            item = self.inventory_table.item(selection[0])
            values = item['values']
            
            if values:
                # Store selected fruit ID
                self.selected_fruit_id = values[0]
    
    def _on_add_fruit(self) -> None:
        """Handle add fruit button click"""
        # Define form fields
        fields = {
            'name': {
                'type': 'entry',
                'label': 'Name',
                'required': True,
                'max_length': 100
            },
            'category': {
                'type': 'combobox',
                'label': 'Category',
                'required': True,
                'options': ['Citrus', 'Berries', 'Tropical', 'Stone Fruit', 'Other']
            },
            'price': {
                'type': 'entry',
                'label': 'Price ($)',
                'required': True,
                'pattern': r'^\d+(\.\d{1,2})?$'
            },
            'quantity': {
                'type': 'spinbox',
                'label': 'Quantity',
                'required': True,
                'min': 0,
                'max': 1000,
                'step': 1,
                'integer': True
            },
            'description': {
                'type': 'text',
                'label': 'Description',
                'required': False,
                'height': 3
            }
        }
        
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Add New Fruit")
        dialog.transient(self)
        dialog.grab_set()
        
        # Position dialog
        x = self.winfo_rootx() + 50
        y = self.winfo_rooty() + 50
        dialog.geometry(f"+{x}+{y}")
        
        # Create form
        form = DataEntryForm(
            dialog,
            fields=fields,
            on_submit=lambda data: self._submit_add_fruit(data, dialog),
            on_cancel=dialog.destroy
        )
        form.grid(padx=20, pady=20)
    
    def _submit_add_fruit(self, form_data: Dict[str, Any], dialog: tk.Toplevel) -> None:
        """Handle form submission for adding fruit
        
        Args:
            form_data: Form data
            dialog: Dialog window to close on success
        """
        try:
            # Convert price to float
            form_data['price'] = float(form_data['price'])
            
            # Create fruit
            fruit = Fruit.from_dict(form_data)
            
            # Save fruit
            self.controller.fruit_service.create(fruit)
            
            # Close dialog
            dialog.destroy()
            
            # Refresh inventory
            self.refresh()
            
            # Show success message
            self.show_info(f"Fruit '{fruit.name}' added successfully")
            
        except Exception as e:
            self.logger.error(f"Error adding fruit: {e}")
            self.show_error(f"Failed to add fruit: {str(e)}")
    
    def _on_edit_fruit(self, event=None) -> None:
        """Handle edit fruit button click or double-click event"""
        # Check if a fruit is selected
        if not self.selected_fruit_id:
            self.show_warning("Please select a fruit to edit")
            return
        
        try:
            # Get selected fruit
            fruit = self.controller.fruit_service.get_by_id(self.selected_fruit_id)
            if not fruit:
                self.show_warning(f"Fruit with ID {self.selected_fruit_id} not found")
                return
            
            # Define form fields
            fields = {
                'name': {
                    'type': 'entry',
                    'label': 'Name',
                    'required': True,
                    'max_length': 100
                },
                'category': {
                    'type': 'combobox',
                    'label': 'Category',
                    'required': True,
                    'options': ['Citrus', 'Berries', 'Tropical', 'Stone Fruit', 'Other']
                },
                'price': {
                    'type': 'entry',
                    'label': 'Price ($)',
                    'required': True,
                    'pattern': r'^\d+(\.\d{1,2})?$'
                },
                'quantity': {
                    'type': 'spinbox',
                    'label': 'Quantity',
                    'required': True,
                    'min': 0,
                    'max': 1000,
                    'step': 1,
                    'integer': True
                },
                'description': {
                    'type': 'text',
                    'label': 'Description',
                    'required': False,
                    'height': 3
                }
            }
            
            # Create initial values
            initial_values = {
                'name': fruit.name,
                'category': fruit.category,
                'price': f"{fruit.price:.2f}" if fruit.price is not None else "",
                'quantity': fruit.quantity,
                'description': fruit.description or ""
            }
            
            # Create dialog window
            dialog = tk.Toplevel(self)
            dialog.title(f"Edit Fruit: {fruit.name}")
            dialog.transient(self)
            dialog.grab_set()
            
            # Position dialog
            x = self.winfo_rootx() + 50
            y = self.winfo_rooty() + 50
            dialog.geometry(f"+{x}+{y}")
            
            # Create form
            form = DataEntryForm(
                dialog,
                fields=fields,
                on_submit=lambda data: self._submit_edit_fruit(fruit.id, data, dialog),
                on_cancel=dialog.destroy,
                initial_values=initial_values
            )
            form.grid(padx=20, pady=20)
            
        except Exception as e:
            self.logger.error(f"Error preparing edit form: {e}")
            self.show_error(f"Failed to prepare edit form: {str(e)}")
    
    def _submit_edit_fruit(self, fruit_id: int, form_data: Dict[str, Any], dialog: tk.Toplevel) -> None:
        """Handle form submission for editing fruit
        
        Args:
            fruit_id: ID of fruit to edit
            form_data: Form data
            dialog: Dialog window to close on success
        """
        try:
            # Convert price to float
            form_data['price'] = float(form_data['price'])
            
            # Get existing fruit
            fruit = self.controller.fruit_service.get_by_id(fruit_id)
            if not fruit:
                self.show_warning(f"Fruit with ID {fruit_id} not found")
                return
            
            # Update fruit attributes
            for key, value in form_data.items():
                setattr(fruit, key, value)
            
            # Save fruit
            self.controller.fruit_service.update(fruit)
            
            # Close dialog
            dialog.destroy()
            
            # Refresh inventory
            self.refresh()
            
            # Show success message
            self.show_info(f"Fruit '{fruit.name}' updated successfully")
            
        except Exception as e:
            self.logger.error(f"Error updating fruit: {e}")
            self.show_error(f"Failed to update fruit: {str(e)}")
    
    def _on_delete_fruit(self) -> None:
        """Handle delete fruit button click"""
        # Check if a fruit is selected
        if not self.selected_fruit_id:
            self.show_warning("Please select a fruit to delete")
            return
        
        try:
            # Get selected fruit
            fruit = self.controller.fruit_service.get_by_id(self.selected_fruit_id)
            if not fruit:
                self.show_warning(f"Fruit with ID {self.selected_fruit_id} not found")
                return
            
            # Confirm deletion
            ConfirmDialog(
                self,
                title="Confirm Deletion",
                message=f"Are you sure you want to delete '{fruit.name}'?",
                on_confirm=lambda: self._confirm_delete_fruit(fruit.id, fruit.name)
            )
            
        except Exception as e:
            self.logger.error(f"Error preparing delete: {e}")
            self.show_error(f"Failed to prepare delete: {str(e)}")
    
    def _confirm_delete_fruit(self, fruit_id: int, fruit_name: str) -> None:
        """Handle confirmation of fruit deletion
        
        Args:
            fruit_id: ID of fruit to delete
            fruit_name: Name of fruit for success message
        """
        try:
            # Delete fruit
            self.controller.fruit_service.delete(fruit_id)
            
            # Reset selected fruit
            self.selected_fruit_id = None
            
            # Refresh inventory
            self.refresh()
            
            # Show success message
            self.show_info(f"Fruit '{fruit_name}' deleted successfully")
            
        except Exception as e:
            self.logger.error(f"Error deleting fruit: {e}")
            self.show_error(f"Failed to delete fruit: {str(e)}")
    
    def _on_import(self) -> None:
        """Handle import button click"""
        # Show file dialog
        file_path = tk.filedialog.askopenfilename(
            title="Import Inventory",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("JSON Files", "*.json"),
                ("All Files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        try:
            # Determine file type
            if file_path.lower().endswith('.csv'):
                # Import from CSV
                imported_fruits = self.controller.file_service.import_from_csv(file_path)
                self.show_info(f"Successfully imported {len(imported_fruits)} fruits from CSV")
            elif file_path.lower().endswith('.json'):
                # Import from JSON
                imported_fruits = self.controller.file_service.import_from_json(file_path)
                self.show_info(f"Successfully imported {len(imported_fruits)} fruits from JSON")
            else:
                self.show_warning("Unsupported file format. Please use CSV or JSON files.")
                return
            
            # Refresh inventory
            self.refresh()
            
        except Exception as e:
            self.logger.error(f"Error importing inventory: {e}")
            self.show_error(f"Failed to import inventory: {str(e)}")
    
    def _on_export(self) -> None:
        """Handle export button click"""
        # Show file dialog
        file_path = tk.filedialog.asksaveasfilename(
            title="Export Inventory",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("JSON Files", "*.json"),
                ("All Files", "*.*")
            ],
            defaultextension=".csv"
        )
        
        if not file_path:
            return
        
        try:
            # Get all fruits or filtered fruits
            fruits = self.current_fruits
            
            # Determine file type
            if file_path.lower().endswith('.csv'):
                # Export to CSV
                self.controller.file_service.export_to_csv(file_path, fruits)
                self.show_info(f"Successfully exported {len(fruits)} fruits to CSV")
            elif file_path.lower().endswith('.json'):
                # Export to JSON
                self.controller.file_service.export_to_json(file_path, fruits)
                self.show_info(f"Successfully exported {len(fruits)} fruits to JSON")
            else:
                self.show_warning("Unsupported file format. Please use CSV or JSON files.")
                return
            
        except Exception as e:
            self.logger.error(f"Error exporting inventory: {e}")
            self.show_error(f"Failed to export inventory: {str(e)}")
    
    def on_show(self) -> None:
        """Called when the page is shown"""
        super().on_show()
        # Additional initialization when page is shown
        self.status_bar.set_status("Loading inventory...")
        self.refresh()
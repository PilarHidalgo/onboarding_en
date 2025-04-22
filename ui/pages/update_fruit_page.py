"""Update Fruit page implementation for editing existing fruits in inventory"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from models import Fruit
from ui.page import Page
from ui.components import StatusBar

class UpdateFruitPage(Page):
    """Update Fruit page for editing existing fruits in inventory
    
    This page provides a form for updating existing fruits in the inventory
    with validation and error handling.
    
    Attributes:
        parent: Parent widget
        controller: Application controller
    """
    
    def __init__(self, parent: tk.Widget, controller: Any):
        """Initialize the update fruit page
        
        Args:
            parent: Parent widget
            controller: Application controller
        """
        super().__init__(parent, controller)
        self.logger = logging.getLogger(__name__)
        self.form_data = {}
        self.form_widgets = {}
        self.validation_errors = {}
        self.current_fruit = None
        self.fruit_id = None
    
    def _init_ui(self) -> None:
        """Initialize UI components"""
        # Create main layout frames
        self.header_frame = self.create_header("Update Fruit")
        self.content_frame = self.create_content_frame()
        self.footer_frame = self.create_footer()
        
        # Configure content frame layout
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Create form
        self._create_form()
        
        # Create action buttons
        self._create_action_buttons()
        
        # Create status bar
        self.status_bar = StatusBar(self.footer_frame)
        self.status_bar.grid(row=0, column=0, sticky="ew")
        self.status_bar.set_status("Select a fruit to update")
    
    def _create_form(self) -> None:
        """Create the update fruit form"""
        # Create form frame
        self.form_frame = ttk.LabelFrame(self.content_frame, text="Fruit Details")
        self.form_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        self.form_frame.grid_columnconfigure(1, weight=1)
        
        # ID field (read-only)
        self._add_form_field(
            self.form_frame, 
            "id", 
            "ID:", 
            field_type="readonly",
            row=0
        )
        
        # Name field
        self._add_form_field(
            self.form_frame, 
            "name", 
            "Name:", 
            required=True, 
            row=1
        )
        
        # Category field
        categories = ["Citrus", "Berries", "Tropical", "Stone Fruit", "Other"]
        self._add_form_field(
            self.form_frame, 
            "category", 
            "Category:", 
            field_type="combobox",
            options=categories,
            required=True, 
            row=2
        )
        
        # Price field
        self._add_form_field(
            self.form_frame, 
            "price", 
            "Price ($):", 
            required=True, 
            row=3
        )
        
        # Quantity field
        self._add_form_field(
            self.form_frame, 
            "quantity", 
            "Quantity:", 
            field_type="spinbox",
            options={"from_": 0, "to": 1000, "increment": 1},
            required=True, 
            row=4
        )
        
        # Description field
        self._add_form_field(
            self.form_frame, 
            "description", 
            "Description:", 
            field_type="text",
            options={"height": 4, "width": 40},
            required=False, 
            row=5
        )
        
        # Origin field
        self._add_form_field(
            self.form_frame, 
            "origin", 
            "Origin:", 
            required=False, 
            row=6
        )
        
        # Organic checkbox
        self._add_form_field(
            self.form_frame, 
            "organic", 
            "Organic:", 
            field_type="checkbox",
            required=False, 
            row=7
        )
        
        # Season field
        seasons = ["Spring", "Summer", "Fall", "Winter", "All Year"]
        self._add_form_field(
            self.form_frame, 
            "season", 
            "Season:", 
            field_type="combobox",
            options=seasons,
            required=False, 
            row=8
        )
        
        # Created at field (read-only)
        self._add_form_field(
            self.form_frame, 
            "created_at", 
            "Created:", 
            field_type="readonly",
            row=9
        )
        
        # Updated at field (read-only)
        self._add_form_field(
            self.form_frame, 
            "updated_at", 
            "Updated:", 
            field_type="readonly",
            row=10
        )
    
    def _add_form_field(
        self, 
        parent: ttk.Frame, 
        field_name: str, 
        label_text: str, 
        field_type: str = "entry", 
        options: Dict[str, Any] = None,
        required: bool = False, 
        row: int = 0
    ) -> None:
        """Add a form field to the form
        
        Args:
            parent: Parent frame
            field_name: Field name
            label_text: Label text
            field_type: Field type (entry, combobox, spinbox, text, checkbox, readonly)
            options: Field options
            required: Whether the field is required
            row: Row index
        """
        options = options or {}
        
        # Create label with required indicator
        label = ttk.Label(parent, text=label_text)
        if required:
            label.config(text=label_text + " *")
        label.grid(row=row, column=0, sticky="w", padx=(10, 5), pady=5)
        
        # Create field based on type
        widget = None
        var = None
        
        if field_type == "entry":
            var = tk.StringVar()
            widget = ttk.Entry(parent, textvariable=var)
            widget.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
            
        elif field_type == "combobox":
            var = tk.StringVar()
            widget = ttk.Combobox(parent, textvariable=var, values=options)
            widget.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
            
        elif field_type == "spinbox":
            var = tk.StringVar()
            widget = ttk.Spinbox(
                parent, 
                textvariable=var,
                from_=options.get("from_", 0),
                to=options.get("to", 100),
                increment=options.get("increment", 1)
            )
            widget.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
            
        elif field_type == "text":
            widget = tk.Text(
                parent, 
                height=options.get("height", 4),
                width=options.get("width", 40)
            )
            widget.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
            
        elif field_type == "checkbox":
            var = tk.BooleanVar(value=False)
            widget = ttk.Checkbutton(parent, variable=var)
            widget.grid(row=row, column=1, sticky="w", padx=5, pady=5)
            
        elif field_type == "readonly":
            var = tk.StringVar()
            widget = ttk.Entry(parent, textvariable=var, state="readonly")
            widget.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        
        # Create error label (initially empty)
        error_label = ttk.Label(parent, text="", foreground="red")
        error_label.grid(row=row, column=2, sticky="w", padx=5, pady=5)
        
        # Store widget references
        self.form_widgets[field_name] = {
            "widget": widget,
            "var": var,
            "type": field_type,
            "required": required,
            "error_label": error_label
        }
    
    def _create_action_buttons(self) -> None:
        """Create action buttons"""
        button_frame = ttk.Frame(self.content_frame)
        button_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=20)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        
        # Update button
        self.update_button = ttk.Button(
            button_frame,
            text="Update",
            command=self._on_update,
            style="Primary.TButton",
            state="disabled"
        )
        self.update_button.grid(row=0, column=0, sticky="e", padx=5)
        
        # Reset button
        self.reset_button = ttk.Button(
            button_frame,
            text="Reset",
            command=self._on_reset,
            state="disabled"
        )
        self.reset_button.grid(row=0, column=1, padx=5)
        
        # Cancel button
        cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel
        )
        cancel_button.grid(row=0, column=2, sticky="w", padx=5)
    
    def load_fruit(self, fruit_id: int) -> None:
        """Load a fruit for editing
        
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
            
            # Update form title
            self.form_frame.config(text=f"Fruit Details - {fruit.name}")
            
            # Populate form fields
            self._populate_form(fruit)
            
            # Enable buttons
            self.update_button.config(state="normal")
            self.reset_button.config(state="normal")
            
            # Stop progress
            self.status_bar.stop_progress()
            self.status_bar.set_status(f"Editing fruit: {fruit.name}")
            
        except Exception as e:
            # Stop progress
            self.status_bar.stop_progress()
            self.status_bar.set_status("Error loading fruit")
            
            # Log error
            self.logger.error(f"Error loading fruit: {e}")
            
            # Show error message
            self.show_error(f"Failed to load fruit: {str(e)}")
    
    def _populate_form(self, fruit: Fruit) -> None:
        """Populate form fields with fruit data
        
        Args:
            fruit: Fruit object to populate form with
        """
        # Clear previous validation errors
        for field_name, field_info in self.form_widgets.items():
            field_info["error_label"].config(text="")
        
        # Populate fields
        self._set_field_value("id", str(fruit.id) if fruit.id else "")
        self._set_field_value("name", fruit.name or "")
        self._set_field_value("category", fruit.category or "")
        self._set_field_value("price", f"{fruit.price:.2f}" if fruit.price is not None else "")
        self._set_field_value("quantity", str(fruit.quantity) if fruit.quantity is not None else "")
        self._set_field_value("description", fruit.description or "")
        self._set_field_value("origin", fruit.origin or "")
        self._set_field_value("organic", fruit.organic or False)
        self._set_field_value("season", fruit.season or "")
        
        # Format dates
        created_at = fruit.created_at.strftime("%Y-%m-%d %H:%M:%S") if fruit.created_at else ""
        updated_at = fruit.updated_at.strftime("%Y-%m-%d %H:%M:%S") if fruit.updated_at else ""
        
        self._set_field_value("created_at", created_at)
        self._set_field_value("updated_at", updated_at)
    
    def _set_field_value(self, field_name: str, value: Any) -> None:
        """Set value of a form field
        
        Args:
            field_name: Field name
            value: Field value
        """
        if field_name not in self.form_widgets:
            return
        
        field_info = self.form_widgets[field_name]
        widget = field_info["widget"]
        field_type = field_info["type"]
        
        if field_type == "text":
            widget.delete("1.0", tk.END)
            if value:
                widget.insert("1.0", value)
        elif field_type == "checkbox":
            field_info["var"].set(bool(value))
        else:
            field_info["var"].set(value)
    
    def _on_update(self) -> None:
        """Handle update button click"""
        # Validate form
        if not self._validate_form():
            return
        
        try:
            # Show progress
            self.status_bar.set_status("Updating fruit...")
            self.status_bar.start_progress()
            
            # Update fruit object
            self.current_fruit.name = self.form_data["name"]
            self.current_fruit.category = self.form_data["category"]
            self.current_fruit.price = self.form_data["price"]
            self.current_fruit.quantity = self.form_data["quantity"]
            self.current_fruit.description = self.form_data.get("description")
            self.current_fruit.origin = self.form_data.get("origin")
            self.current_fruit.organic = self.form_data.get("organic", False)
            self.current_fruit.season = self.form_data.get("season")
            self.current_fruit.updated_at = datetime.now()
            
            # Save fruit
            updated_fruit = self.controller.fruit_service.update(self.current_fruit)
            
            # Stop progress
            self.status_bar.stop_progress()
            self.status_bar.set_status(f"Fruit '{updated_fruit.name}' updated successfully")
            
            # Show success message
            self.show_info(f"Fruit '{updated_fruit.name}' updated successfully")
            
            # Update form with latest data
            self._populate_form(updated_fruit)
            
        except Exception as e:
            # Stop progress
            self.status_bar.stop_progress()
            self.status_bar.set_status("Error updating fruit")
            
            # Log error
            self.logger.error(f"Error updating fruit: {e}")
            
            # Show error message
            self.show_error(f"Failed to update fruit: {str(e)}")
    
    def _on_reset(self) -> None:
        """Handle reset button click"""
        if self.current_fruit:
            # Confirm reset
            if self._form_has_changes() and not self.ask_yes_no("Discard changes and reset form?"):
                return
                
            # Reload fruit data
            self._populate_form(self.current_fruit)
            self.status_bar.set_status(f"Form reset to original values")
    
    def _on_cancel(self) -> None:
        """Handle cancel button click"""
        # Confirm if form has changes
        if self._form_has_changes() and not self.ask_yes_no("Discard changes and return to inventory?"):
            return
        
        # Navigate back to inventory page
        self.controller.show_page("InventoryPage")
    
    def _validate_form(self) -> bool:
        """Validate form data
        
        Returns:
            True if form is valid, False otherwise
        """
        # Clear previous validation errors
        self.validation_errors = {}
        self.form_data = {}
        
        # Clear error labels
        for field_name, field_info in self.form_widgets.items():
            field_info["error_label"].config(text="")
        
        # Validate each field
        for field_name, field_info in self.form_widgets.items():
            # Skip read-only fields
            if field_info["type"] == "readonly":
                continue
                
            widget = field_info["widget"]
            field_type = field_info["type"]
            required = field_info["required"]
            
            # Get field value
            value = None
            
            if field_type == "text":
                value = widget.get("1.0", tk.END).strip()
            elif field_type == "checkbox":
                value = field_info["var"].get()
            else:
                value = field_info["var"].get().strip()
            
            # Check required fields
            if required and not value:
                self.validation_errors[field_name] = "This field is required"
                field_info["error_label"].config(text="Required")
                continue
            
            # Validate and convert specific fields
            if field_name == "price" and value:
                try:
                    price = float(value)
                    if price < 0:
                        self.validation_errors[field_name] = "Price cannot be negative"
                        field_info["error_label"].config(text="Invalid price")
                    else:
                        self.form_data[field_name] = price
                except ValueError:
                    self.validation_errors[field_name] = "Price must be a number"
                    field_info["error_label"].config(text="Invalid price")
            
            elif field_name == "quantity" and value:
                try:
                    quantity = int(value)
                    if quantity < 0:
                        self.validation_errors[field_name] = "Quantity cannot be negative"
                        field_info["error_label"].config(text="Invalid quantity")
                    else:
                        self.form_data[field_name] = quantity
                except ValueError:
                    self.validation_errors[field_name] = "Quantity must be a whole number"
                    field_info["error_label"].config(text="Invalid quantity")
            
            else:
                # Store other fields as is
                self.form_data[field_name] = value
        
        # Show validation error message if any
        if self.validation_errors:
            error_message = "Please correct the following errors:\n\n"
            for field, error in self.validation_errors.items():
                field_label = next((f["widget"].master.grid_slaves(row=i, column=0)[0]["text"].replace(" *", "") 
                                  for i, f in enumerate(self.form_widgets.values()) 
                                  if f["widget"] == self.form_widgets[field]["widget"]), field)
                error_message += f"• {field_label} {error}\n"
            
            self.show_error(error_message)
            return False
        
        return True
    
    def _form_has_changes(self) -> bool:
        """Check if form has any changes from the current fruit
        
        Returns:
            True if form has changes, False otherwise
        """
        if not self.current_fruit:
            return False
            
        # Check each editable field
        if self._get_field_value("name") != (self.current_fruit.name or ""):
            return True
            
        if self._get_field_value("category") != (self.current_fruit.category or ""):
            return True
            
        current_price = f"{self.current_fruit.price:.2f}" if self.current_fruit.price is not None else ""
        if self._get_field_value("price") != current_price:
            return True
            
        current_quantity = str(self.current_fruit.quantity) if self.current_fruit.quantity is not None else ""
        if self._get_field_value("quantity") != current_quantity:
            return True
            
        if self._get_field_value("description") != (self.current_fruit.description or ""):
            return True
            
        if self._get_field_value("origin") != (self.current_fruit.origin or ""):
            return True
            
        if self._get_field_value("organic") != (self.current_fruit.organic or False):
            return True
            
        if self._get_field_value("season") != (self.current_fruit.season or ""):
            return True
            
        return False
    
    def _get_field_value(self, field_name: str) -> Any:
        """Get value of a form field
        
        Args:
            field_name: Field name
            
        Returns:
            Field value
        """
        if field_name not in self.form_widgets:
            return None
            
        field_info = self.form_widgets[field_name]
        widget = field_info["widget"]
        field_type = field_info["type"]
        
        if field_type == "text":
            return widget.get("1.0", tk.END).strip()
        elif field_type == "checkbox":
            return field_info["var"].get()
        else:
            return field_info["var"].get().strip()
    
    def _setup_bindings(self) -> None:
        """Set up event bindings"""
        # Add keyboard shortcut for update (Ctrl+S)
        self.bind_all("<Control-s>", lambda e: self._on_update())
        
        # Add keyboard shortcut for reset (Ctrl+R)
        self.bind_all("<Control-r>", lambda e: self._on_reset())
        
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
            self.current_fruit = None
            self.fruit_id = None
            self.form_frame.config(text="Fruit Details")
            self.update_button.config(state="disabled")
            self.reset_button.config(state="disabled")
            self.status_bar.set_status("No fruit selected")
    
    def on_hide(self) -> None:
        """Called when the page is hidden"""
        super().on_hide()
        # Unbind keyboard shortcuts
        self.unbind_all("<Control-s>")
        self.unbind_all("<Control-r>")
        self.unbind_all("<Escape>")
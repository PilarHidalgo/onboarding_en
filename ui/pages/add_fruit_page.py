"""Add Fruit page implementation for adding new fruits to inventory"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from models import Fruit
from ui.page import Page
from ui.components import StatusBar

class AddFruitPage(Page):
    """Add Fruit page for adding new fruits to inventory
    
    This page provides a form for adding new fruits to the inventory
    with validation and error handling.
    
    Attributes:
        parent: Parent widget
        controller: Application controller
    """
    
    def __init__(self, parent: tk.Widget, controller: Any):
        """Initialize the add fruit page
        
        Args:
            parent: Parent widget
            controller: Application controller
        """
        super().__init__(parent, controller)
        self.logger = logging.getLogger(__name__)
        self.form_data = {}
        self.form_widgets = {}
        self.validation_errors = {}
    
    def _init_ui(self) -> None:
        """Initialize UI components"""
        # Create main layout frames
        self.header_frame = self.create_header("Add New Fruit")
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
        self.status_bar.set_status("Ready to add new fruit")
    
    def _create_form(self) -> None:
        """Create the add fruit form"""
        # Create form frame
        form_frame = ttk.LabelFrame(self.content_frame, text="Fruit Details")
        form_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Name field
        self._add_form_field(
            form_frame, 
            "name", 
            "Name:", 
            required=True, 
            row=0
        )
        
        # Category field
        categories = ["Citrus", "Berries", "Tropical", "Stone Fruit", "Other"]
        self._add_form_field(
            form_frame, 
            "category", 
            "Category:", 
            field_type="combobox",
            options=categories,
            required=True, 
            row=1
        )
        
        # Price field
        self._add_form_field(
            form_frame, 
            "price", 
            "Price ($):", 
            required=True, 
            row=2
        )
        
        # Quantity field
        self._add_form_field(
            form_frame, 
            "quantity", 
            "Quantity:", 
            field_type="spinbox",
            options={"from_": 0, "to": 1000, "increment": 1},
            required=True, 
            row=3
        )
        
        # Description field
        self._add_form_field(
            form_frame, 
            "description", 
            "Description:", 
            field_type="text",
            options={"height": 4, "width": 40},
            required=False, 
            row=4
        )
        
        # Origin field
        self._add_form_field(
            form_frame, 
            "origin", 
            "Origin:", 
            required=False, 
            row=5
        )
        
        # Organic checkbox
        self._add_form_field(
            form_frame, 
            "organic", 
            "Organic:", 
            field_type="checkbox",
            required=False, 
            row=6
        )
        
        # Season field
        seasons = ["Spring", "Summer", "Fall", "Winter", "All Year"]
        self._add_form_field(
            form_frame, 
            "season", 
            "Season:", 
            field_type="combobox",
            options=seasons,
            required=False, 
            row=7
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
            field_type: Field type (entry, combobox, spinbox, text, checkbox)
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
        
        # Save button
        save_button = ttk.Button(
            button_frame,
            text="Save",
            command=self._on_save,
            style="Primary.TButton"
        )
        save_button.grid(row=0, column=0, sticky="e", padx=5)
        
        # Cancel button
        cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel
        )
        cancel_button.grid(row=0, column=1, sticky="w", padx=5)
    
    def _on_save(self) -> None:
        """Handle save button click"""
        # Validate form
        if not self._validate_form():
            return
        
        try:
            # Show progress
            self.status_bar.set_status("Saving fruit...")
            self.status_bar.start_progress()
            
            # Create fruit object
            fruit = Fruit(
                id=None,  # ID will be assigned by the database
                name=self.form_data["name"],
                category=self.form_data["category"],
                price=self.form_data["price"],
                quantity=self.form_data["quantity"],
                description=self.form_data.get("description"),
                origin=self.form_data.get("origin"),
                organic=self.form_data.get("organic", False),
                season=self.form_data.get("season"),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Save fruit
            saved_fruit = self.controller.fruit_service.create(fruit)
            
            # Stop progress
            self.status_bar.stop_progress()
            self.status_bar.set_status(f"Fruit '{saved_fruit.name}' saved successfully")
            
            # Show success message
            self.show_info(f"Fruit '{saved_fruit.name}' added successfully")
            
            # Clear form
            self._clear_form()
            
        except Exception as e:
            # Stop progress
            self.status_bar.stop_progress()
            self.status_bar.set_status("Error saving fruit")
            
            # Log error
            self.logger.error(f"Error saving fruit: {e}")
            
            # Show error message
            self.show_error(f"Failed to save fruit: {str(e)}")
    
    def _on_cancel(self) -> None:
        """Handle cancel button click"""
        # Confirm if form has data
        if self._form_has_data():
            if not self.ask_yes_no("Discard changes and return to inventory?"):
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
    
    def _clear_form(self) -> None:
        """Clear the form"""
        for field_name, field_info in self.form_widgets.items():
            widget = field_info["widget"]
            field_type = field_info["type"]
            
            # Clear field based on type
            if field_type == "text":
                widget.delete("1.0", tk.END)
            elif field_type == "checkbox":
                field_info["var"].set(False)
            else:
                field_info["var"].set("")
            
            # Clear error label
            field_info["error_label"].config(text="")
        
        # Clear form data and validation errors
        self.form_data = {}
        self.validation_errors = {}
        
        # Update status
        self.status_bar.set_status("Ready to add new fruit")
    
    def _form_has_data(self) -> bool:
        """Check if form has any data entered
        
        Returns:
            True if form has data, False otherwise
        """
        for field_name, field_info in self.form_widgets.items():
            widget = field_info["widget"]
            field_type = field_info["type"]
            
            # Check field based on type
            if field_type == "text":
                if widget.get("1.0", tk.END).strip():
                    return True
            elif field_type == "checkbox":
                if field_info["var"].get():
                    return True
            else:
                if field_info["var"].get().strip():
                    return True
        
        return False
    
    def _setup_bindings(self) -> None:
        """Set up event bindings"""
        # Add keyboard shortcut for save (Ctrl+S)
        self.bind_all("<Control-s>", lambda e: self._on_save())
        
        # Add keyboard shortcut for cancel (Escape)
        self.bind_all("<Escape>", lambda e: self._on_cancel())
    
    def on_show(self) -> None:
        """Called when the page is shown"""
        super().on_show()
        # Clear form when page is shown
        self._clear_form()
        
        # Set focus to name field
        if "name" in self.form_widgets:
            self.form_widgets["name"]["widget"].focus_set()
    
    def on_hide(self) -> None:
        """Called when the page is hidden"""
        super().on_hide()
        # Unbind keyboard shortcuts
        self.unbind_all("<Control-s>")
        self.unbind_all("<Escape>")
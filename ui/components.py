```python
"""Reusable UI components for the application"""
import tkinter as tk
from tkinter import ttk, filedialog
import logging
from typing import Dict, Any, Optional, Callable, List, Union, Tuple
from datetime import datetime
import re

class SearchBar(ttk.Frame):
    """Search bar component with search button
    
    Attributes:
        parent: Parent widget
        on_search: Callback function for search
        placeholder: Placeholder text for search entry
    """
    
    def __init__(
        self, 
        parent: tk.Widget, 
        on_search: Callable[[str], None], 
        placeholder: str = "Search..."
    ):
        """Initialize the search bar
        
        Args:
            parent: Parent widget
            on_search: Callback function for search
            placeholder: Placeholder text for search entry
        """
        super().__init__(parent)
        self.parent = parent
        self.on_search = on_search
        self.placeholder = placeholder
        self.logger = logging.getLogger(__name__)
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        
        # Initialize UI components
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize UI components"""
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Set placeholder
        self.search_entry.insert(0, self.placeholder)
        self.search_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.search_entry.bind("<FocusOut>", self._on_entry_focus_out)
        self.search_entry.bind("<Return>", lambda e: self._perform_search())
        
        # Search button
        self.search_button = ttk.Button(
            self, 
            text="Search", 
            command=self._perform_search
        )
        self.search_button.grid(row=0, column=1, sticky="e")
    
    def _on_entry_focus_in(self, event) -> None:
        """Handle entry focus in event"""
        if self.search_var.get() == self.placeholder:
            self.search_entry.delete(0, tk.END)
    
    def _on_entry_focus_out(self, event) -> None:
        """Handle entry focus out event"""
        if not self.search_var.get():
            self.search_entry.insert(0, self.placeholder)
    
    def _perform_search(self) -> None:
        """Perform search operation"""
        query = self.search_var.get()
        if query and query != self.placeholder:
            self.on_search(query)
    
    def get_query(self) -> str:
        """Get the current search query
        
        Returns:
            Current search query or empty string if placeholder
        """
        query = self.search_var.get()
        return "" if query == self.placeholder else query
    
    def set_query(self, query: str) -> None:
        """Set the search query
        
        Args:
            query: Search query to set
        """
        self.search_var.set(query)
        if not query:
            self.search_entry.insert(0, self.placeholder)


class FilterPanel(ttk.LabelFrame):
    """Filter panel component with multiple filter options
    
    Attributes:
        parent: Parent widget
        on_filter: Callback function for filter changes
        filters: Dictionary of filter definitions
    """
    
    def __init__(
        self, 
        parent: tk.Widget, 
        on_filter: Callable[[Dict[str, Any]], None],
        filters: Dict[str, Dict[str, Any]]
    ):
        """Initialize the filter panel
        
        Args:
            parent: Parent widget
            on_filter: Callback function for filter changes
            filters: Dictionary of filter definitions with keys as filter names
                    and values as dictionaries with 'type', 'label', and 'options'
        """
        super().__init__(parent, text="Filters")
        self.parent = parent
        self.on_filter = on_filter
        self.filters = filters
        self.logger = logging.getLogger(__name__)
        self.filter_widgets = {}
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        
        # Initialize UI components
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize UI components"""
        row = 0
        
        # Create filter widgets based on filter definitions
        for filter_name, filter_def in self.filters.items():
            # Create label
            label = ttk.Label(self, text=filter_def.get('label', filter_name))
            label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
            
            # Create filter widget based on type
            filter_type = filter_def.get('type', 'combobox')
            widget = None
            
            if filter_type == 'combobox':
                values = filter_def.get('options', [])
                var = tk.StringVar()
                widget = ttk.Combobox(self, textvariable=var, values=values)
                widget.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
                widget.bind("<<ComboboxSelected>>", lambda e: self._on_filter_change())
                widget.var = var
                
            elif filter_type == 'checkbox':
                var = tk.BooleanVar(value=filter_def.get('default', False))
                widget = ttk.Checkbutton(
                    self, 
                    variable=var, 
                    command=self._on_filter_change
                )
                widget.grid(row=row, column=1, sticky="w", padx=5, pady=5)
                widget.var = var
                
            elif filter_type == 'range':
                frame = ttk.Frame(self)
                frame.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
                
                min_var = tk.StringVar()
                max_var = tk.StringVar()
                
                min_entry = ttk.Entry(frame, width=10, textvariable=min_var)
                min_entry.grid(row=0, column=0, padx=(0, 5))
                
                ttk.Label(frame, text="-").grid(row=0, column=1, padx=5)
                
                max_entry = ttk.Entry(frame, width=10, textvariable=max_var)
                max_entry.grid(row=0, column=2, padx=(5, 0))
                
                min_entry.bind("<FocusOut>", lambda e: self._on_filter_change())
                max_entry.bind("<FocusOut>", lambda e: self._on_filter_change())
                
                widget = frame
                widget.min_var = min_var
                widget.max_var = max_var
            
            # Store widget reference
            if widget:
                self.filter_widgets[filter_name] = widget
            
            row += 1
        
        # Add reset button
        reset_button = ttk.Button(
            self, 
            text="Reset Filters", 
            command=self.reset_filters
        )
        reset_button.grid(row=row, column=0, columnspan=2, pady=10)
    
    def _on_filter_change(self) -> None:
        """Handle filter change event"""
        filter_values = self.get_filter_values()
        self.on_filter(filter_values)
    
    def get_filter_values(self) -> Dict[str, Any]:
        """Get current filter values
        
        Returns:
            Dictionary of filter values
        """
        values = {}
        
        for filter_name, widget in self.filter_widgets.items():
            filter_type = self.filters[filter_name].get('type', 'combobox')
            
            if filter_type == 'combobox':
                value = widget.var.get()
                if value:  # Only include non-empty values
                    values[filter_name] = value
                    
            elif filter_type == 'checkbox':
                value = widget.var.get()
                values[filter_name] = value
                
            elif filter_type == 'range':
                min_val = widget.min_var.get().strip()
                max_val = widget.max_var.get().strip()
                
                if min_val or max_val:
                    values[filter_name] = {
                        'min': min_val if min_val else None,
                        'max': max_val if max_val else None
                    }
        
        return values
    
    def reset_filters(self) -> None:
        """Reset all filters to default values"""
        for filter_name, widget in self.filter_widgets.items():
            filter_type = self.filters[filter_name].get('type', 'combobox')
            
            if filter_type == 'combobox':
                widget.var.set('')
                
            elif filter_type == 'checkbox':
                default = self.filters[filter_name].get('default', False)
                widget.var.set(default)
                
            elif filter_type == 'range':
                widget.min_var.set('')
                widget.max_var.set('')
        
        # Trigger filter change event
        self._on_filter_change()


class StatusBar(ttk.Frame):
    """Status bar component with message and progress indicator
    
    Attributes:
        parent: Parent widget
    """
    
    def __init__(self, parent: tk.Widget):
        """Initialize the status bar
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.parent = parent
        self.logger = logging.getLogger(__name__)
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        
        # Initialize UI components
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize UI components"""
        # Status message
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self, textvariable=self.status_var)
        self.status_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        # Progress bar (initially hidden)
        self.progress_bar = ttk.Progressbar(self, mode="indeterminate", length=100)
        self.progress_bar.grid(row=0, column=1, sticky="e", padx=5, pady=2)
        self.progress_bar.grid_remove()  # Hide initially
    
    def set_status(self, message: str) -> None:
        """Set the status message
        
        Args:
            message: Status message to display
        """
        self.status_var.set(message)
    
    def start_progress(self) -> None:
        """Start progress indicator"""
        self.progress_bar.grid()  # Show progress bar
        self.progress_bar.start()
    
    def stop_progress(self) -> None:
        """Stop progress indicator"""
        self.progress_bar.stop()
        self.progress_bar.grid_remove()  # Hide progress bar


class ConfirmDialog(tk.Toplevel):
    """Custom confirmation dialog
    
    Attributes:
        parent: Parent widget
        title: Dialog title
        message: Dialog message
        on_confirm: Callback function for confirmation
        on_cancel: Callback function for cancellation
    """
    
    def __init__(
        self, 
        parent: tk.Widget, 
        title: str, 
        message: str,
        on_confirm: Callable[[], None],
        on_cancel: Optional[Callable[[], None]] = None
    ):
        """Initialize the confirmation dialog
        
        Args:
            parent: Parent widget
            title: Dialog title
            message: Dialog message
            on_confirm: Callback function for confirmation
            on_cancel: Callback function for cancellation (optional)
        """
        super().__init__(parent)
        self.parent = parent
        self.title(title)
        self.message = message
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel or (lambda: None)
        self.logger = logging.getLogger(__name__)
        
        # Configure dialog
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Position dialog relative to parent
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        dialog_width = 300
        dialog_height = 150
        
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # Initialize UI components
        self._init_ui()
        
        # Wait for dialog to close
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.wait_visibility()
        self.focus_set()
    
    def _init_ui(self) -> None:
        """Initialize UI components"""
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        main_frame = ttk.Frame(self, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Message label
        message_label = ttk.Label(
            main_frame, 
            text=self.message, 
            wraplength=280, 
            justify="center"
        )
        message_label.grid(row=0, column=0, pady=10)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=10)
        
        # Confirm button
        confirm_button = ttk.Button(
            button_frame, 
            text="Confirm", 
            command=self._on_confirm,
            style="Primary.TButton"
        )
        confirm_button.grid(row=0, column=0, padx=5)
        
        # Cancel button
        cancel_button = ttk.Button(
            button_frame, 
            text="Cancel", 
            command=self._on_cancel
        )
        cancel_button.grid(row=0, column=1, padx=5)
    
    def _on_confirm(self) -> None:
        """Handle confirm button click"""
        self.destroy()
        self.on_confirm()
    
    def _on_cancel(self) -> None:
        """Handle cancel button click"""
        self.destroy()
        self.on_cancel()


class DataEntryForm(ttk.Frame):
    """Data entry form component with validation
    
    Attributes:
        parent: Parent widget
        fields: Dictionary of field definitions
        on_submit: Callback function for form submission
        on_cancel: Callback function for form cancellation
    """
    
    def __init__(
        self, 
        parent: tk.Widget, 
        fields: Dict[str, Dict[str, Any]],
        on_submit: Callable[[Dict[str, Any]], None],
        on_cancel: Optional[Callable[[], None]] = None,
        initial_values: Optional[Dict[str, Any]] = None
    ):
        """Initialize the data entry form
        
        Args:
            parent: Parent widget
            fields: Dictionary of field definitions with keys as field names
                   and values as dictionaries with 'type', 'label', 'required', etc.
            on_submit: Callback function for form submission
            on_cancel: Callback function for form cancellation (optional)
            initial_values: Initial values for fields (optional)
        """
        super().__init__(parent)
        self.parent = parent
        self.fields = fields
        self.on_submit = on_submit
        self.on_cancel = on_cancel or (lambda: None)
        self.initial_values = initial_values or {}
        self.logger = logging.getLogger(__name__)
        self.field_widgets = {}
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        
        # Initialize UI components
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize UI components"""
        row = 0
        
        # Create field widgets based on field definitions
        for field_name, field_def in self.fields.items():
            # Create label
            label_text = field_def.get('label', field_name)
            if field_def.get('required', False):
                label_text += " *"
                
            label = ttk.Label(self, text=label_text)
            label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
            
            # Create field widget based on type
            field_type = field_def.get('type', 'entry')
            widget = None
            
            if field_type == 'entry':
                var = tk.StringVar()
                widget = ttk.Entry(self, textvariable=var)
                widget.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
                widget.var = var
                
            elif field_type == 'combobox':
                values = field_def.get('options', [])
                var = tk.StringVar()
                widget = ttk.Combobox(self, textvariable=var, values=values)
                widget.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
                widget.var = var
                
            elif field_type == 'checkbox':
                var = tk.BooleanVar(value=field_def.get('default', False))
                widget = ttk.Checkbutton(self, variable=var)
                widget.grid(row=row, column=1, sticky="w", padx=5, pady=5)
                widget.var = var
                
            elif field_type == 'spinbox':
                var = tk.StringVar()
                widget = ttk.Spinbox(
                    self, 
                    textvariable=var,
                    from_=field_def.get('min', 0),
                    to=field_def.get('max', 100),
                    increment=field_def.get('step', 1)
                )
                widget.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
                widget.var = var
                
            elif field_type == 'text':
                var = tk.StringVar()
                widget = tk.Text(self, height=field_def.get('height', 5), width=field_def.get('width', 40))
                widget.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
                # For text widget, we don't use var
                
            elif field_type == 'date':
                var = tk.StringVar()
                widget = ttk.Entry(self, textvariable=var)
                widget.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
                widget.var = var
                
                # Add date format hint
                hint = ttk.Label(self, text="(YYYY-MM-DD)", foreground="gray")
                hint.grid(row=row, column=2, sticky="w", padx=5, pady=5)
            
            # Set initial value if provided
            if widget and field_name in self.initial_values:
                initial_value = self.initial_values[field_name]
                
                if field_type == 'text':
                    widget.delete(1.0, tk.END)
                    widget.insert(tk.END, str(initial_value) if initial_value is not None else "")
                elif field_type == 'checkbox':
                    widget.var.set(bool(initial_value))
                elif field_type == 'date' and isinstance(initial_value, datetime):
                    widget.var.set(initial_value.strftime("%Y-%m-%d"))
                else:
                    widget.var.set(initial_value if initial_value is not None else "")
            
            # Store widget reference
            if widget:
                self.field_widgets[field_name] = widget
            
            row += 1
        
        # Add button frame
        button_frame = ttk.Frame(self)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        # Submit button
        submit_button = ttk.Button(
            button_frame, 
            text="Submit", 
            command=self._on_submit,
            style="Primary.TButton"
        )
        submit_button.grid(row=0, column=0, padx=5)
        
        # Cancel button
        if self.on_cancel:
            cancel_button = ttk.Button(
                button_frame, 
                text="Cancel", 
                command=self.on_cancel
            )
            cancel_button.grid(row=0, column=1, padx=5)
    
    def _on_submit(self) -> None:
        """Handle form submission"""
        # Validate and collect form data
        form_data, errors = self.validate_and_get_data()
        
        if errors:
            # Show validation errors
            error_message = "Please correct the following errors:\n\n"
            error_message += "\n".join(errors)
            tk.messagebox.showerror("Validation Error", error_message)
            return
        
        # Call submit callback with form data
        self.on_submit(form_data)
    
    def validate_and_get_data(self) -> Tuple[Dict[str, Any], List[str]]:
        """Validate form data and return values
        
        Returns:
            Tuple of (form_data, errors)
        """
        form_data = {}
        errors = []
        
        for field_name, field_def in self.fields.items():
            widget = self.field_widgets.get(field_name)
            if not widget:
                continue
                
            field_type = field_def.get('type', 'entry')
            required = field_def.get('required', False)
            label = field_def.get('label', field_name)
            
            # Get field value
            value = None
            
            if field_type == 'text':
                value = widget.get(1.0, tk.END).strip()
            else:
                value = widget.var.get()
                
                # Convert empty strings to None
                if value == "" and field_type != 'checkbox':
                    value = None
            
            # Check required fields
            if required and (value is None or value == ""):
                errors.append(f"{label} is required")
                continue
            
            # Skip further validation if value is None and field is not required
            if value is None:
                form_data[field_name] = None
                continue
            
            # Validate and convert based on field type
            try:
                if field_type == 'entry' or field_type == 'combobox' or field_type == 'text':
                    # Check max length if specified
                    max_length = field_def.get('max_length')
                    if max_length and len(str(value)) > max_length:
                        errors.append(f"{label} exceeds maximum length of {max_length}")
                        continue
                        
                    # Check pattern if specified
                    pattern = field_def.get('pattern')
                    if pattern and not re.match(pattern, str(value)):
                        errors.append(f"{label} does not match required format")
                        continue
                        
                    form_data[field_name] = value
                    
                elif field_type == 'checkbox':
                    form_data[field_name] = bool(value)
                    
                elif field_type == 'spinbox':
                    # Convert to number
                    if field_def.get('integer', True):
                        form_data[field_name] = int(value)
                    else:
                        form_data[field_name] = float(value)
                        
                elif field_type == 'date':
                    # Validate date format
                    try:
                        date_value = datetime.strptime(value, "%Y-%m-%d").date()
                        form_data[field_name] = date_value
                    except ValueError:
                        errors.append(f"{label} must be in YYYY-MM-DD format")
                        continue
                
            except (ValueError, TypeError) as e:
                errors.append(f"Invalid value for {label}: {str(e)}")
                continue
        
        return form_data, errors


class FileSelector(ttk.Frame):
    """File selector component
    
    Attributes:
        parent: Parent widget
        on_file_selected: Callback function for file selection
        file_types: List of file type tuples
        mode: 'open' or 'save'
    """
    
    def __init__(
        self, 
        parent: tk.Widget, 
        on_file_selected: Callable[[str], None],
        file_types: List[Tuple[str, str]] = None,
        mode: str = 'open',
        label: str = "Select File:"
    ):
        """Initialize the file selector
        
        Args:
            parent: Parent widget
            on_file_selected: Callback function for file selection
            file_types: List of file type tuples (description, extension)
            mode: 'open' or 'save'
            label: Label text
        """
        super().__init__(parent)
        self.parent = parent
        self.on_file_selected = on_file_selected
        self.file_types = file_types or [("All Files", "*.*")]
        self.mode = mode
        self.label_text = label
        self.logger = logging.getLogger(__name__)
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        
        # Initialize UI components
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize UI components"""
        # Label
        label = ttk.Label(self, text=self.label_text)
        label.grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        # File path entry
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(self, textvariable=self.path_var)
        self.path_entry.grid(row=0, column=1, sticky="ew", padx=5)
        
        # Browse button
        browse_button = ttk.Button(
            self, 
            text="Browse...", 
            command=self._browse_file
        )
        browse_button.grid(row=0, column=2, sticky="e")
    
    def _browse_file(self) -> None:
        """Open file dialog and handle selection"""
        filepath = ""
        
        if self.mode == 'open':
            filepath = filedialog.askopenfilename(
                parent=self.parent,
                filetypes=self.file_types,
                title="Open File"
            )
        else:  # save mode
            filepath = filedialog.asksaveasfilename(
                parent=self.parent,
                filetypes=self.file_types,
                title="Save File"
            )
        
        if filepath:
            self.path_var.set(filepath)
            self.on_file_selected(filepath)
    
    def get_filepath(self) -> str:
        """Get the selected file path
        
        Returns:
            Selected file path
        """
        return self.path_var.get()
    
    def set_filepath(self, filepath: str) -> None:
        """Set the file path
        
        Args:
            filepath: File path to set
        """
        self.path_var.set(filepath)


class Pagination(ttk.Frame):
    """Pagination component
    
    Attributes:
        parent: Parent widget
        on_page_change: Callback function for page changes
        total_items: Total number of items
        items_per_page: Number of items per page
    """
    
    def __init__(
        self, 
        parent: tk.Widget, 
        on_page_change: Callable[[int], None],
        total_items: int = 0,
        items_per_page: int = 10
    ):
        """Initialize the pagination component
        
        Args:
            parent: Parent widget
            on_page_change: Callback function for page changes
            total_items: Total number of items
            items_per_page: Number of items per page
        """
        super().__init__(parent)
        self.parent = parent
        self.on_page_change = on_page_change
        self.total_items = total_items
        self.items_per_page = items_per_page
        self.current_page = 1
        self.logger = logging.getLogger(__name__)
        
        # Calculate total pages
        self.total_pages = max(1, (self.total_items + self.items_per_page - 1) // self.items_per_page)
        
        # Initialize UI components
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize UI components"""
        # Previous page button
        self.prev_button = ttk.Button(
            self, 
            text="< Prev", 
            command=self._go_to_prev_page,
            state="disabled" if self.current_page <= 1 else "normal"
        )
        self.prev_button.grid(row=0, column=0, padx=5)
        
        # Page info label
        self.page_info_var = tk.StringVar()
        self._update_page_info()
        page_info_label = ttk.Label(self, textvariable=self.page_info_var)
        page_info_label.grid(row=0, column=1, padx=10)
        
        # Next page button
        self.next_button = ttk.Button(
            self, 
            text="Next >", 
            command=self._go_to_next_page,
            state="disabled" if self.current_page >= self.total_pages else "normal"
        )
        self.next_button.grid(row=0, column=2, padx=5)
    
    def _update_page_info(self) -> None:
        """Update page information text"""
        self.page_info_var.set(f"Page {self.current_page} of {self.total_pages}")
    
    def _update_button_states(self) -> None:
        """Update button states based on current page"""
        self.prev_button.config(state="normal" if self.current_page > 1 else "disabled")
        self.next_button.config(state="normal" if self.current_page < self.total_pages else "disabled")
    
    def _go_to_prev_page(self) -> None:
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self._update_page_info()
            self._update_button_states()
            self.on_page_change(self.current_page)
    
    def _go_to_next_page(self) -> None:
        """Go to next page"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._update_page_info()
            self._update_button_states()
            self.on_page_change
"""Base page implementation for UI components"""
import tkinter as tk
from tkinter import ttk
import logging
from typing import Dict, Any, Optional, Callable, List, Union
from abc import ABC, abstractmethod

class Page(ABC, ttk.Frame):
    """Base class for all UI pages
    
    This abstract class provides a foundation for building UI pages
    with consistent navigation, styling, and error handling.
    
    Attributes:
        parent: Parent widget
        controller: Application controller
        logger: Logger instance
    """
    
    def __init__(self, parent: tk.Widget, controller: Any):
        """Initialize the page
        
        Args:
            parent: Parent widget
            controller: Application controller
        """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.logger = logging.getLogger(__name__)
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Initialize UI components
        self._init_ui()
        
        # Set up event bindings
        self._setup_bindings()
    
    @abstractmethod
    def _init_ui(self) -> None:
        """Initialize UI components
        
        This method must be implemented by subclasses to create
        the page's UI components.
        """
        pass
    
    def _setup_bindings(self) -> None:
        """Set up event bindings
        
        Override this method to add custom event bindings.
        """
        pass
    
    def refresh(self) -> None:
        """Refresh the page content
        
        Called when the page is shown or needs to be updated.
        Override this method to update dynamic content.
        """
        pass
    
    def on_show(self) -> None:
        """Called when the page is shown
        
        Override this method to perform actions when the page becomes visible.
        """
        self.refresh()
    
    def on_hide(self) -> None:
        """Called when the page is hidden
        
        Override this method to perform actions when the page becomes invisible.
        """
        pass
    
    def create_header(self, title: str) -> ttk.Frame:
        """Create a standard header with title and navigation
        
        Args:
            title: Page title
            
        Returns:
            Frame containing the header
        """
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Back button
        back_btn = ttk.Button(
            header_frame, 
            text="← Back", 
            command=self.controller.go_back,
            style="Secondary.TButton"
        )
        back_btn.grid(row=0, column=0, sticky="w")
        
        # Title
        title_label = ttk.Label(
            header_frame, 
            text=title, 
            font=("TkDefaultFont", 16, "bold")
        )
        title_label.grid(row=0, column=1, sticky="w", padx=10)
        
        # Home button
        home_btn = ttk.Button(
            header_frame, 
            text="Home", 
            command=lambda: self.controller.show_page("HomePage"),
            style="Secondary.TButton"
        )
        home_btn.grid(row=0, column=2, sticky="e")
        
        return header_frame
    
    def create_content_frame(self) -> ttk.Frame:
        """Create a standard content frame
        
        Returns:
            Frame for page content
        """
        content_frame = ttk.Frame(self)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        return content_frame
    
    def create_footer(self) -> ttk.Frame:
        """Create a standard footer
        
        Returns:
            Frame containing the footer
        """
        footer_frame = ttk.Frame(self)
        footer_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
        footer_frame.grid_columnconfigure(0, weight=1)
        
        # Status label
        status_label = ttk.Label(footer_frame, text="Ready")
        status_label.grid(row=0, column=0, sticky="w")
        
        # Store reference to status label
        self.status_label = status_label
        
        return footer_frame
    
    def set_status(self, message: str) -> None:
        """Set the status message in the footer
        
        Args:
            message: Status message to display
        """
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
    
    def show_error(self, message: str) -> None:
        """Show an error message
        
        Args:
            message: Error message to display
        """
        self.logger.error(message)
        tk.messagebox.showerror("Error", message)
    
    def show_warning(self, message: str) -> None:
        """Show a warning message
        
        Args:
            message: Warning message to display
        """
        self.logger.warning(message)
        tk.messagebox.showwarning("Warning", message)
    
    def show_info(self, message: str) -> None:
        """Show an information message
        
        Args:
            message: Information message to display
        """
        self.logger.info(message)
        tk.messagebox.showinfo("Information", message)
    
    def ask_yes_no(self, message: str) -> bool:
        """Ask a yes/no question
        
        Args:
            message: Question to ask
            
        Returns:
            True if yes, False if no
        """
        return tk.messagebox.askyesno("Question", message)
    
    def create_scrollable_frame(self, parent: tk.Widget) -> ttk.Frame:
        """Create a scrollable frame
        
        Args:
            parent: Parent widget
            
        Returns:
            Frame that can be scrolled
        """
        # Create a canvas with scrollbar
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Configure scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure weights
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        return scrollable_frame
    
    def create_data_table(
        self, 
        parent: tk.Widget, 
        columns: List[Dict[str, Any]], 
        data: List[Dict[str, Any]] = None
    ) -> ttk.Treeview:
        """Create a data table
        
        Args:
            parent: Parent widget
            columns: List of column definitions with keys 'id', 'text', and 'width'
            data: Optional initial data for the table
            
        Returns:
            Treeview widget configured as a data table
        """
        # Create frame for table and scrollbar
        table_frame = ttk.Frame(parent)
        table_frame.grid(sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # Create treeview columns
        column_ids = [col['id'] for col in columns]
        
        # Create treeview with scrollbars
        tree = ttk.Treeview(
            table_frame, 
            columns=column_ids, 
            show='headings',
            selectmode='browse'
        )
        
        # Configure columns
        for col in columns:
            tree.heading(col['id'], text=col['text'])
            tree.column(col['id'], width=col.get('width', 100), anchor=col.get('anchor', 'w'))
        
        # Add vertical scrollbar
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        # Add horizontal scrollbar
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=hsb.set)
        
        # Grid layout
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Add initial data if provided
        if data:
            self.update_data_table(tree, data)
        
        return tree
    
    def update_data_table(
        self, 
        table: ttk.Treeview, 
        data: List[Dict[str, Any]]
    ) -> None:
        """Update data in a table
        
        Args:
            table: Treeview widget to update
            data: New data for the table
        """
        # Clear existing data
        table.delete(*table.get_children())
        
        # Add new data
        for item in data:
            values = [item.get(col, '') for col in table['columns']]
            table.insert('', 'end', values=values, tags=(item.get('tag', '')))
    
    def create_form_field(
        self, 
        parent: tk.Widget, 
        label_text: str, 
        field_type: str = 'entry', 
        options: Dict[str, Any] = None
    ) -> Union[ttk.Entry, ttk.Combobox, ttk.Checkbutton, ttk.Spinbox]:
        """Create a form field with label
        
        Args:
            parent: Parent widget
            label_text: Label text
            field_type: Type of field ('entry', 'combobox', 'checkbox', 'spinbox')
            options: Additional options for the field
            
        Returns:
            Created field widget
        """
        options = options or {}
        
        # Create frame for field
        field_frame = ttk.Frame(parent)
        field_frame.grid(sticky="ew", pady=5)
        field_frame.grid_columnconfigure(1, weight=1)
        
        # Create label
        label = ttk.Label(field_frame, text=label_text)
        label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        # Create field based on type
        field = None
        
        if field_type == 'entry':
            field = ttk.Entry(field_frame, **options)
            field.grid(row=0, column=1, sticky="ew")
            
        elif field_type == 'combobox':
            field = ttk.Combobox(field_frame, **options)
            field.grid(row=0, column=1, sticky="ew")
            
        elif field_type == 'checkbox':
            var = tk.BooleanVar(value=options.get('value', False))
            field = ttk.Checkbutton(field_frame, variable=var, **options)
            field.grid(row=0, column=1, sticky="w")
            field.var = var  # Store variable for easy access
            
        elif field_type == 'spinbox':
            field = ttk.Spinbox(field_frame, **options)
            field.grid(row=0, column=1, sticky="ew")
        
        return field
    
    def create_button_group(
        self, 
        parent: tk.Widget, 
        buttons: List[Dict[str, Any]]
    ) -> List[ttk.Button]:
        """Create a group of buttons
        
        Args:
            parent: Parent widget
            buttons: List of button definitions with keys 'text', 'command', and 'style'
            
        Returns:
            List of created button widgets
        """
        # Create frame for buttons
        button_frame = ttk.Frame(parent)
        button_frame.grid(sticky="ew", pady=10)
        
        created_buttons = []
        
        # Create buttons
        for i, btn_def in enumerate(buttons):
            style = btn_def.get('style', 'TButton')
            button = ttk.Button(
                button_frame,
                text=btn_def['text'],
                command=btn_def['command'],
                style=style
            )
            button.grid(row=0, column=i, padx=5)
            created_buttons.append(button)
        
        return created_buttons
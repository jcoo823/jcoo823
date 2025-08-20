#!/usr/bin/env python3
"""
Simple GUI Calculator using Tkinter
A basic calculator with number input, arithmetic operations, and result display.
"""

import tkinter as tk
from tkinter import messagebox
import operator

class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        # Calculator state
        self.current_input = ""
        self.total = 0
        self.operator = None
        self.reset_display = False
        
        # Operations mapping
        self.operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create the calculator user interface"""
        # Display frame
        display_frame = tk.Frame(self.root)
        display_frame.pack(pady=10, padx=10, fill='x')
        
        # Display entry
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        self.display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=('Arial', 16),
            state='readonly',
            justify='right',
            relief='sunken',
            bd=2
        )
        self.display.pack(fill='x', ipady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=10, padx=10, expand=True, fill='both')
        
        # Button layout: 4x5 grid
        # Row 0: Clear, ±, %, ÷
        # Row 1: 7, 8, 9, ×
        # Row 2: 4, 5, 6, -
        # Row 3: 1, 2, 3, +
        # Row 4: 0 (spans 2), ., =
        
        button_configs = [
            # Row 0
            ('C', 0, 0, self.clear, 1, '#ff9999'),
            ('±', 0, 1, self.plus_minus, 1, '#cccccc'),
            ('%', 0, 2, self.percentage, 1, '#cccccc'),
            ('÷', 0, 3, lambda: self.set_operator('/'), 1, '#ffcc99'),
            
            # Row 1
            ('7', 1, 0, lambda: self.input_number('7'), 1, '#ffffff'),
            ('8', 1, 1, lambda: self.input_number('8'), 1, '#ffffff'),
            ('9', 1, 2, lambda: self.input_number('9'), 1, '#ffffff'),
            ('×', 1, 3, lambda: self.set_operator('*'), 1, '#ffcc99'),
            
            # Row 2
            ('4', 2, 0, lambda: self.input_number('4'), 1, '#ffffff'),
            ('5', 2, 1, lambda: self.input_number('5'), 1, '#ffffff'),
            ('6', 2, 2, lambda: self.input_number('6'), 1, '#ffffff'),
            ('-', 2, 3, lambda: self.set_operator('-'), 1, '#ffcc99'),
            
            # Row 3
            ('1', 3, 0, lambda: self.input_number('1'), 1, '#ffffff'),
            ('2', 3, 1, lambda: self.input_number('2'), 1, '#ffffff'),
            ('3', 3, 2, lambda: self.input_number('3'), 1, '#ffffff'),
            ('+', 3, 3, lambda: self.set_operator('+'), 1, '#ffcc99'),
            
            # Row 4
            ('0', 4, 0, lambda: self.input_number('0'), 2, '#ffffff'),
            ('.', 4, 2, self.input_decimal, 1, '#ffffff'),
            ('=', 4, 3, self.calculate, 1, '#99ccff'),
        ]
        
        # Create buttons
        for text, row, col, command, colspan, color in button_configs:
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=command,
                font=('Arial', 14, 'bold'),
                bg=color,
                relief='raised',
                bd=2
            )
            btn.grid(
                row=row, 
                column=col, 
                columnspan=colspan,
                sticky='nsew', 
                padx=2, 
                pady=2
            )
        
        # Configure grid weights for responsive layout
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
    
    def input_number(self, number):
        """Handle number button input"""
        if self.reset_display:
            self.current_input = ""
            self.reset_display = False
        
        if self.current_input == "0":
            self.current_input = number
        else:
            self.current_input += number
        
        self.update_display()
    
    def input_decimal(self):
        """Handle decimal point input"""
        if self.reset_display:
            self.current_input = "0"
            self.reset_display = False
        
        if '.' not in self.current_input:
            if not self.current_input:
                self.current_input = "0"
            self.current_input += '.'
            self.update_display()
    
    def set_operator(self, op):
        """Handle operator button input"""
        try:
            if self.current_input:
                if self.operator is not None:
                    self.calculate()
                else:
                    self.total = float(self.current_input)
                
                self.operator = op
                self.reset_display = True
        except ValueError:
            self.show_error("Invalid input")
    
    def calculate(self):
        """Perform calculation"""
        try:
            if self.operator is not None and self.current_input:
                current_value = float(self.current_input)
                
                if self.operator == '/' and current_value == 0:
                    self.show_error("Cannot divide by zero")
                    return
                
                self.total = self.operations[self.operator](self.total, current_value)
                self.current_input = self.format_result(self.total)
                self.operator = None
                self.reset_display = True
                self.update_display()
        except (ValueError, ZeroDivisionError) as e:
            self.show_error(f"Error: {str(e)}")
    
    def clear(self):
        """Clear calculator state"""
        self.current_input = "0"
        self.total = 0
        self.operator = None
        self.reset_display = False
        self.update_display()
    
    def plus_minus(self):
        """Toggle sign of current number"""
        if self.current_input and self.current_input != "0":
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display()
    
    def percentage(self):
        """Convert current number to percentage"""
        try:
            if self.current_input:
                value = float(self.current_input) / 100
                self.current_input = self.format_result(value)
                self.update_display()
        except ValueError:
            self.show_error("Invalid input for percentage")
    
    def format_result(self, value):
        """Format result for display"""
        if value == int(value):
            return str(int(value))
        else:
            # Round to 10 decimal places to avoid floating point precision issues
            return f"{value:.10g}"
    
    def update_display(self):
        """Update the calculator display"""
        display_text = self.current_input if self.current_input else "0"
        self.display_var.set(display_text)
    
    def show_error(self, message):
        """Show error message and reset calculator"""
        messagebox.showerror("Error", message)
        self.clear()
    
    def run(self):
        """Start the calculator application"""
        self.root.mainloop()

def main():
    """Main function to run the calculator"""
    calculator = Calculator()
    calculator.run()

if __name__ == "__main__":
    main()
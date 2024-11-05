import tkinter as tk

class QWERTYKeyboard:
    # Constants for key sizes and spacing
    KEY_WIDTH = 50
    KEY_HEIGHT = 50
    KEY_SPACING = 5

    # QWERTY keyboard layout
    keyboard_layout = [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        ["Z", "X", "C", "V", "B", "N", "M"]
    ]

    # Special widths for certain keys
    special_keys = {
        "Backspace": 2 * KEY_WIDTH + KEY_SPACING,
        "Tab": 1.5 * KEY_WIDTH + KEY_SPACING,
        "Caps": 1.5 * KEY_WIDTH + KEY_SPACING,
        "Enter": 1.75 * KEY_WIDTH + KEY_SPACING,
        "Shift": 2.25 * KEY_WIDTH + KEY_SPACING,
        "Space": 5 * KEY_WIDTH + 4 * KEY_SPACING
    }

    def __init__(self, root, parent, x_start, y_start):
        self.root = root
        self.parent = parent
        self.canvas = tk.Canvas(self.parent, width=800, height=300, bg="white")
        self.canvas.pack()
        
        # Starting position for the keyboard layout
        self.x_start, self.y_start = x_start, y_start

        # Dictionary to keep track of rectangles by label
        self.key_rects = {}

        # Draw the keyboard
        self.draw_keyboard()

        # Bind key press and release events
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)

    def draw_keyboard(self):
        # Draw keys for each row
        self.draw_row(self.keyboard_layout[0], self.x_start, self.y_start)
        self.draw_row(self.keyboard_layout[1], self.x_start + 0.75 * (self.KEY_WIDTH + self.KEY_SPACING), 
                      self.y_start + self.KEY_HEIGHT + self.KEY_SPACING)
        self.draw_row(self.keyboard_layout[2], self.x_start + 1.5 * (self.KEY_WIDTH + self.KEY_SPACING), 
                      self.y_start + 2 * (self.KEY_HEIGHT + self.KEY_SPACING))

        # Add special keys
        self.draw_special_keys()

    def draw_row(self, row, x_start, y):
        x = x_start
        for key in row:
            self.draw_key(x, y, self.KEY_WIDTH, self.KEY_HEIGHT, key)
            x += self.KEY_WIDTH + self.KEY_SPACING

    def draw_key(self, x, y, width, height, label):
        rect = self.canvas.create_rectangle(x, y, x + width, y + height, fill="lightgrey")
        self.canvas.create_text(x + width / 2, y + height / 2, text=label, font=("Arial", 16))
        
        # Store the rectangle ID with the label for easy lookup
        self.key_rects[label] = rect

    def draw_special_keys(self):
        # Special key positions relative to x_start, y_start
        special_key_positions = {
            "Backspace": (self.x_start + 10 * (self.KEY_WIDTH + self.KEY_SPACING), self.y_start),
            "Tab": (self.x_start - 0.75 * (self.KEY_WIDTH + self.KEY_SPACING), 
                    self.y_start + self.KEY_HEIGHT + self.KEY_SPACING),
            "Caps": (self.x_start - 1.5 * (self.KEY_WIDTH + self.KEY_SPACING), 
                     self.y_start + 2 * (self.KEY_HEIGHT + self.KEY_SPACING)),
            "Enter": (self.x_start + 9 * (self.KEY_WIDTH + self.KEY_SPACING), 
                      self.y_start + 2 * (self.KEY_HEIGHT + self.KEY_SPACING)),
            "Shift": (self.x_start - 1.75 * (self.KEY_WIDTH + self.KEY_SPACING), 
                      self.y_start + 3 * (self.KEY_HEIGHT + self.KEY_SPACING)),
            "Space": (self.x_start + 2.5 * (self.KEY_WIDTH + self.KEY_SPACING), 
                      self.y_start + 4 * (self.KEY_HEIGHT + self.KEY_SPACING))
        }

        for key, (x, y) in special_key_positions.items():
            width = self.special_keys[key]
            self.draw_key(x, y, width, self.KEY_HEIGHT, key)

    def highlight_key(self, label):
        # Change the color of the rectangle associated with the given label to red
        if label in self.key_rects:
            rect_id = self.key_rects[label]
            self.canvas.itemconfig(rect_id, fill="red")

    def reset_key(self, label):
        # Reset the color of the key to lightgrey
        if label in self.key_rects:
            rect_id = self.key_rects[label]
            self.canvas.itemconfig(rect_id, fill="lightgrey")

    def on_key_press(self, event):
        # Convert the event key to uppercase to match the labels
        label = event.keysym.upper()

        # Highlight the pressed key if it exists on the keyboard
        if label in self.key_rects:
            self.highlight_key(label)

    def on_key_release(self, event):
        # Convert the event key to uppercase to match the labels
        label = event.keysym.upper()

        # Reset the key color when it's released
        if label in self.key_rects:
            self.reset_key(label)

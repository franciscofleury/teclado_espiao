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

    def __init__(self, root):
        self.root = root
        self.root.title("QWERTY Keyboard")
        self.canvas = tk.Canvas(root, width=800, height=300, bg="white")
        self.canvas.pack()
        
        # Starting position for the keyboard layout
        self.x_start, self.y_start = 50, 50

        # Draw the keyboard
        self.draw_keyboard()

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
        self.canvas.create_rectangle(x, y, x + width, y + height, fill="lightgrey")
        self.canvas.create_text(x + width / 2, y + height / 2, text=label, font=("Arial", 16))

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


# Initialize the tkinter window and the QWERTYKeyboard
root = tk.Tk()
keyboard = QWERTYKeyboard(root)
root.mainloop()

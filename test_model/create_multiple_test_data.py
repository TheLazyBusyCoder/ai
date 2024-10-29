import tkinter as tk
import json
import os

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Create data app")
        self.no_of_file = 0

        # Create a smaller canvas
        self.grid_size = 10
        self.cell_size = 30  # Size of each cell in pixels
        self.canvas = tk.Canvas(root, bg='white', width=self.cell_size * self.grid_size, height=self.cell_size * self.grid_size)
        self.canvas.pack()

        self.filename_label = tk.Label(root, text="Enter Letter:")
        self.filename_label.pack()
        
        self.filename_entry = tk.Entry(root)
        self.filename_entry.pack()

        self.fill_label = tk.Label(root, text="Enter grid data:")
        self.fill_label.pack()

        self.fill_entry = tk.Entry(root, width=35)  # Single line input for grid
        self.fill_entry.pack()

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_canvas)
        self.reset_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(root, text="Save", command=self.save_canvas)
        self.save_button.pack(side=tk.LEFT)

        self.fill_button = tk.Button(root, text="Fill Canvas", command=self.fill_canvas)
        self.fill_button.pack(side=tk.LEFT)

        # Bind mouse events for drawing
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-1>", self.draw)  # Added to draw on click

        # Initialize grid
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Draw the grid overlay
        self.draw_grid()

    def draw_grid(self):
        """Draw grid lines on the canvas for better visualization."""
        for i in range(self.grid_size + 1):
            # Vertical lines
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.cell_size * self.grid_size, fill='lightgray')
            # Horizontal lines
            self.canvas.create_line(0, i * self.cell_size, self.cell_size * self.grid_size, i * self.cell_size, fill='lightgray')

    def draw(self, event):
        # Calculate the grid cell
        x, y = event.x // self.cell_size, event.y // self.cell_size

        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            self.grid[y][x] = 1  # Mark the cell as white
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size, (x + 1) * self.cell_size, (y + 1) * self.cell_size, fill='black', outline='black')

    def fill_canvas(self):
        """Fill the canvas based on the input grid data."""
        try:
            input_data = self.fill_entry.get().strip()  # Get the text from the entry
            grid_data = eval(input_data)  # Convert the string representation to an actual list
            
            if len(grid_data) != self.grid_size or any(len(row) != self.grid_size for row in grid_data):
                raise ValueError("Input must be a 10x10 array.")

            # Clear the canvas and set the grid based on the input data
            self.reset_canvas()
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    if grid_data[y][x] == 1:
                        self.draw_cell(x, y)

        except Exception as e:
            print("Error:", e)

    def draw_cell(self, x, y):
        """Draw a single cell on the canvas."""
        self.grid[y][x] = 1  # Mark the cell as filled
        self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size, (x + 1) * self.cell_size, (y + 1) * self.cell_size, fill='black', outline='black')

    def reset_canvas(self):
        # Clear the canvas
        self.canvas.delete("all")
        # Reset the grid
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        # Redraw the grid
        self.draw_grid()

    def save_canvas(self):
        self.no_of_file += 1
        filename = self.filename_entry.get().strip()
        if not filename:
            return
            
        file_path = "input.json"
        new_data = [row[:] for row in self.grid]
        data_out = {
            "answer": filename,
            "array": new_data
        }

        # Read existing data, if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []
        
        existing_data.append(data_out)

        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=2)
        self.reset_canvas()

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

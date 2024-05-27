import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageDraw, ImageTk

class ImageHighlighter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Highlighter")
        self.canvas = tk.Canvas(root)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.image_path = None
        self.image = None
        self.tk_image = None
        self.highlighted_coords = []
        self.resize_ratio = (1, 1)

        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT)

        self.highlight_button = tk.Button(root, text="Highlight Coordinates", command=self.highlight_coords)
        self.highlight_button.pack(side=tk.LEFT)

        self.root.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.get_coords)

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.display_image()

    def display_image(self):
        if self.image:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            original_width, original_height = self.image.size
            self.resize_ratio = (canvas_width / original_width, canvas_height / original_height)
            resized_image = self.image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_resize(self, event):
        if self.image:
            self.display_image()

    def highlight_coords(self):
        if not self.image:
            return
        
        coords_str = simpledialog.askstring("Input", "Enter coordinates (x1,y1 x2,y2 ...):")
        if coords_str:
            coords = coords_str.split()
            for coord in coords:
                x, y = map(int, coord.split(','))
                self.highlighted_coords.append((x, y))

            self.apply_highlights()

    def apply_highlights(self):
        draw = ImageDraw.Draw(self.image)
        for x, y in self.highlighted_coords:
            original_x = int(x / self.resize_ratio[0])
            original_y = int(y / self.resize_ratio[1])
            draw.rectangle([original_x, original_y, original_x + 16, original_y + 16], outline="red", width=2)
        self.display_image()

    def get_coords(self, event):
        x = int(self.canvas.canvasx(event.x) / self.resize_ratio[0])
        y = int(self.canvas.canvasy(event.y) / self.resize_ratio[1])
        print(f"Clicked at: ({x}, {y})")
        self.highlighted_coords.append((x, y))
        self.apply_highlights()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageHighlighter(root)
    root.mainloop()

import tkinter as tk

class ResizableFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.start_resize)
        self.bind("<B1-Motion>", self.perform_resize)

    def start_resize(self, event):
        self._drag_data = {"x": event.x, "y": event.y}

    def perform_resize(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        
        new_width = self.winfo_width() + dx
        new_height = self.winfo_height() + dy

        if new_width > 50 and new_height > 50:  # Đảm bảo kích thước không quá nhỏ
            self.config(width=new_width, height=new_height)
            self._drag_data = {"x": event.x, "y": event.y}

root = tk.Tk()
root.geometry("400x300")

frame = ResizableFrame(root, width=200, height=150, bg="lightblue")
frame.place(x=50, y=50)

root.mainloop()

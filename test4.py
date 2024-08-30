import tkinter as tk
from tkinter import ttk

def focus_on_item(index):
    # Lấy danh sách tất cả các item trong Treeview
    items = tree.get_children()

    # Kiểm tra nếu index hợp lệ
    if 0 <= index < len(items):
        # Lấy ID của item dựa trên index
        item_id = items[index]
        
        # Focus vào item
        
        # Chọn item
        tree.selection_set(item_id)
        
        # Cuộn đến item được chọn (nếu nó không nằm trong tầm nhìn)
        tree.see(item_id)
        
        # Hiển thị thông tin của item
        item_data = tree.item(item_id)
        values = item_data['values']
        print(f"Focused Item ID: {item_id}")
        print(f"Values: {values}")
    else:
        print("Index out of range")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Treeview Example")

# Tạo Treeview
tree = ttk.Treeview(root, columns=('Column 1', 'Column 2', 'Column 3'), show='headings')

# Đặt tiêu đề cho các cột
tree.heading('Column 1', text='Column 1')
tree.heading('Column 2', text='Column 2')
tree.heading('Column 3', text='Column 3')

# Thêm dữ liệu vào Treeview
tree.insert('', 'end', values=('Item 1', 'Value 1', 'More 1'))
tree.insert('', 'end', values=('Item 2', 'Value 2', 'More 2'))
tree.insert('', 'end', values=('Item 3', 'Value 3', 'More 3'))

# Đặt Treeview vào giao diện
tree.pack(fill=tk.BOTH, expand=True)

# Focus vào item có index 1 (item thứ 2)
focus_on_item(1)

# Chạy vòng lặp chính của giao diện
root.mainloop()

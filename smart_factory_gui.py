import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import csv

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("스마트 팩토리 GUI")
        
        self.class_name = self.read_class_name_from_csv('./most_common_values.csv')
        
        self.default_image_path = "./img/normal.png"
        self.current_image_path = self.default_image_path
        self.current_text = "정상"
        self.text_font = ("Helvetica", 48)
        self.text_color = "black"

        self.frame1 = ttk.Frame(self.root, padding="10", width=300, height=400)
        self.frame1.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.frame1.grid_propagate(False)
        self.create_pie_chart()

        self.frame2 = ttk.Frame(self.root, padding="10", width=300, height=400)
        self.frame2.grid(row=0, column=1, rowspan=3, sticky="nsew")
        self.frame2.grid_propagate(False)
        self.display_defect_image()

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=50)
        self.root.columnconfigure(1, weight=1)

        self.root.after(500, self.update_gui)  # 5초마다 update_gui 메서드 호출

        self.root.geometry("1200x600")

    def update_gui(self):
        self.class_name = "broken_door" if self.class_name == "normal_door" else "normal_door"
        self.create_pie_chart()
        self.display_defect_image()
        self.root.after(500, self.update_gui)  # 5초마다 update_gui 메서드 재호출

    def read_class_name_from_csv(self, csv_file_path):
        with open(csv_file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)
            for row in csv_reader:
                self.class_name = row[0]
                print(self.class_name)
                return self.class_name
            
    def create_pie_chart(self):
        data = [30, 20, 15, 10, 5, 20]
        labels = ['A', 'B', 'C', 'D', 'E', 'F']

        fig, ax = plt.subplots()
        ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, master=self.frame1)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def display_defect_image(self):
        for widget in self.frame2.winfo_children():
            widget.destroy()
        
        if self.class_name == "normal_door" or "normal_glass" or "normal_bumper":
            self.current_image_path = "./img/normal.png"
            self.current_text = "정상"
        elif self.class_name == "broken_door":
            self.current_image_path = "./img/broken_door.png"
            self.current_text = "결함 감지: 문 파손"
        elif self.class_name == "broken_glass":
            self.current_image_path = "./img/broken_glass.png"
            self.current_text = "결함 감지: 유리 파손"
        elif self.class_name == "broken_bumper":
            self.current_image_path = "./img/broken_bumper.png"
            self.current_text = "결함 감지: 범퍼 파손"
        
        image = Image.open(self.current_image_path)
        image = ImageTk.PhotoImage(image)

        label_image = ttk.Label(self.frame2, image=image)
        label_image.image = image
        label_image.pack(side="bottom", anchor="center", expand=True, fill="both")

        label_text = ttk.Label(self.frame2, text=self.current_text, font=self.text_font, foreground=self.text_color)
        label_text.pack(side="top")

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()

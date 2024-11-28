###########################################################################

#        #     #                            #
# #      #     # #                        # #
#  #           #  #                      #  #
#  #     #     #   #                    #   #
# #      #     #    #                  #    #
#        #     #     #                #     #
# #      #     #      #              #      #
#  #     #     #       #            #       #
#   #    #     #        #          #        #
#   #    #     #         #        #         #
#   #    #     #          #      #          #
#  #     #     #           #    #           #
# #      #     #            #  #            #
#        #     #             #              #
 
#                    #                    #                            #
# #                 # #                   # #                        # #
#  #               #   #                  #  #                      #  #
#  #              #     #                 #   #                    #   #
# #              #       #                #    #                  #    #
#               #         #               #     #                #     #
# #            #           #              #      #              #      #
#  #          #             #             #       #            #       #
#   #        #################            #        #          #        #
#   #       #                 #           #         #        #         #
#   #      #                   #          #          #      #          #
#  #      #                     #         #           #    #           #
# #      #                       #        #            #  #            #
#       #                         #       #             #              #

'''this.provod@gmail.com Кулебакин Иван Викторович'''
##########################################################################


import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageDraw
import os

from task_1 import train_predict_task_1
from task_2 import train_predict_task_2

class Task1:
    def __init__(self, master):
        self.master = master
        self.master.title("лаба 10. 1 задание")
        self.logs_text = tk.Text(master, width=20, height=10)
        self.logs_text.pack() 
        self.canvas_size = 500
        self.cell_size = 50
        self.scale_factor = 2

        self.canvas = tk.Canvas(self.master, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack()

        self.save_button = tk.Button(self.master, text="Сохранить", command=self.save_image)
        self.save_button.pack()

        self.black_button = tk.Button(self.master, text="Чёрный", command=self.set_black_color)
        self.black_button.pack(side=tk.LEFT, padx=5)

        self.white_button = tk.Button(self.master, text="Белый", command=self.set_white_color)
        self.white_button.pack(side=tk.LEFT, padx=5)

        self.current_color = "black"

        self.canvas.bind("<B1-Motion>", self.paint)

        self.image = Image.new("RGB", (self.canvas_size, self.canvas_size), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.draw_grid()

    def draw_grid(self):
        for i in range(0, self.canvas_size, self.cell_size * self.scale_factor):
            self.canvas.create_line(i, 0, i, self.canvas_size, fill="lightgray")

        for i in range(0, self.canvas_size, self.cell_size * self.scale_factor):
            self.canvas.create_line(0, i, self.canvas_size, i, fill="lightgray")

    def paint(self, event):
        x1 = (event.x // (self.cell_size * self.scale_factor)) * (self.cell_size * self.scale_factor)
        y1 = (event.y // (self.cell_size * self.scale_factor)) * (self.cell_size * self.scale_factor)
        x2 = x1 + (self.cell_size * self.scale_factor)
        y2 = y1 + (self.cell_size * self.scale_factor)

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.current_color, outline=self.current_color)
        self.draw.rectangle([x1, y1, x2, y2], fill=self.current_color)

    def set_black_color(self):
        self.current_color = "black"

    def set_white_color(self):
        self.current_color = "white"

    def save_image(self):
        os.makedirs('pic', exist_ok=True)

        self.image.save("pic/drawing.png")
        image_path = "pic/drawing.png"
        image = Image.open(image_path)

        new_width = 5
        new_height = 5

        resized_image = image.resize((new_width, new_height))

        resized_image.save("pic/resized_image.jpg")
        image_path = 'pic/drawing.png'
        if os.path.isfile(image_path):
            try:
                os.remove(image_path)
                print(f"Изображение '{image_path}' было успешно удалено.")
            except Exception as e:
                print(f"Произошла ошибка при попытке удалить файл: {e}")
        else:
            print(f"Файл '{image_path}' не найден.")

        predict, logs = train_predict_task_1()
        self.logs_text.insert(tk.END, f"Логи: {logs}\n")

        self.logs_text.insert(tk.END, f"Предсказание: {predict}\n")

class Task2:
    def __init__(self, master):
        self.master = master
        self.master.title("лаба 10. 2 задание")
        self.logs_text = tk.Text(master, width=30, height=15)
        self.logs_text.pack() 
        
        self.cell_size = 30
        self.canvas_size = self.cell_size * 10
        self.scale_factor = 1

        self.canvas = tk.Canvas(self.master, width=self.canvas_size * self.scale_factor, height=self.canvas_size * self.scale_factor, bg="white")
        self.canvas.pack()

        self.save_button = tk.Button(self.master, text="Сохранить", command=self.save_image)
        self.save_button.pack()

        self.black_button = tk.Button(self.master, text="Чёрный", command=self.set_black_color)
        self.black_button.pack(side=tk.LEFT, padx=5)

        self.white_button = tk.Button(self.master, text="Белый", command=self.set_white_color)
        self.white_button.pack(side=tk.LEFT, padx=5)

        self.current_color = "black"

        self.canvas.bind("<B1-Motion>", self.paint)

        self.image = Image.new("RGB", (self.canvas_size, self.canvas_size), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.draw_grid()

    def draw_grid(self):
        for i in range(0, self.canvas_size, self.cell_size * self.scale_factor):
            self.canvas.create_line(i, 0, i, self.canvas_size, fill="lightgray")

        for i in range(0, self.canvas_size, self.cell_size * self.scale_factor):
            self.canvas.create_line(0, i, self.canvas_size, i, fill="lightgray")

    def paint(self, event):
        x1 = (event.x // (self.cell_size * self.scale_factor)) * (self.cell_size * self.scale_factor)
        y1 = (event.y // (self.cell_size * self.scale_factor)) * (self.cell_size * self.scale_factor)
        x2 = x1 + (self.cell_size * self.scale_factor)
        y2 = y1 + (self.cell_size * self.scale_factor)

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.current_color, outline=self.current_color)
        self.draw.rectangle([x1, y1, x2, y2], fill=self.current_color)

    def set_black_color(self):
        self.current_color = "black"

    def set_white_color(self):
        self.current_color = "white"

    def save_image(self):

        os.makedirs('pic', exist_ok=True)
        scaled_image = self.image.resize((int(self.canvas_size * self.scale_factor), int(self.canvas_size * self.scale_factor)))

        scaled_image.save("pic/drawing_10.png")
        image_path = "pic/drawing_10.png"
        image = Image.open(image_path)

        new_width = 10
        new_height = 10

        resized_image = image.resize((new_width, new_height))

        resized_image.save("pic/resized_image_10.jpg")
        image_path = 'pic/drawing_10.png'

        predict, logs = train_predict_task_2()
        self.logs_text.insert(tk.END, f"Логи: {logs}\n")

        self.logs_text.insert(tk.END, f"Предсказание: {predict}\n")
        
class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("BimBam 10 лаба")
        self.master.geometry('500x500')
        
        self.open_drawing_app_button = tk.Button(self.master, text="1 задание", command=self.open_task_1)
        self.open_drawing_app_button.pack(pady=20)
        
        self.open_drawing_app_button = tk.Button(self.master, text="2 задание", command=self.open_task_2)
        self.open_drawing_app_button.pack(pady=20)

    def open_task_1(self):
        new_window = Toplevel(self.master)
        Task1(new_window)
        
    def open_task_2(self):
        new_window = Toplevel(self.master)
        Task2(new_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

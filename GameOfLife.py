import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

def rainbow_color(C, a):
    r = int(a * 255 * (1 + np.sin(C)) / 2)
    g = int(a * 255 * (1 + np.sin(C + 2 * np.pi / 3)) / 2)
    b = int(a * 255 * (1 + np.sin(C + 4 * np.pi / 3)) / 2)

    return r, g, b

class GameOfLifeUI:
    def __init__(self, root):
        # Инициализация окна
        self.root = root
        self.root.title('Game of Life')
        self.root.geometry('900x750')
        
        # Главное поле в окне
        control_frame = tk.Frame(root, bg='lightgrey', pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Инициализация графика
        self.fig = Figure(figsize=(9, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Интеграция графика в окно
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Инициализация игры
        self.game = GameOfLife(100, 100)
        self.paused = False
        self.interval = 100

        # Кнопки управления
        tk.Button(control_frame, text='Play', command=self.play, width=10).pack(side=tk.LEFT,padx=5)
        tk.Button(control_frame, text='Pause', command=self.pause, width=10).pack(side=tk.LEFT,padx=5)
        tk.Button(control_frame, text='Reset', command=self.reset, width=10).pack(side=tk.LEFT,padx=5)

        # Выбор цвета
        tk.Label(control_frame, text='Color').pack(side=tk.LEFT, padx=5)
        self.color_value = tk.DoubleVar(value=1.5)
        color_slider = ttk.Scale(
            control_frame,
            from_=0.0,
            to=(2 * np.pi),
            variable=self.color_value,
            orient=tk.HORIZONTAL,
            length=200,
        )
        color_slider.pack(side=tk.LEFT, padx=5)

        # Выбор интенсивности
        self.alpha_value = tk.DoubleVar(value=0)
        alpha_slider = ttk.Scale(
            control_frame,
            from_=0.0,
            to=1.0,
            variable=self.alpha_value,
            orient=tk.HORIZONTAL,
            length=50,
        )
        alpha_slider.pack(side=tk.LEFT, padx=5)

        # Запуск анимации
        self.anim = FuncAnimation(
            self.fig,
            self.animate,
            interval=100,
            repeat=True,
            blit=False
        )
        self.canvas.draw()

    def play(self):
        self.paused = False

    def pause(self):
        self.paused = True

    def reset(self):
        self.game = GameOfLife(100, 100)

    def animate(self, frame):
        if not self.paused:
            self.game.step()

        Color = float(self.color_value.get())
        a = float(self.alpha_value.get())
        r, g, b = rainbow_color(Color, a)

        h, w = self.game.field.shape
        rgb = np.ones((h, w, 3), dtype=int) * 255
        mask = (self.game.field == 1)
        rgb[mask] = [r, g, b]

        # Очистка и рисование заново
        self.ax.clear()
        self.ax.imshow(
            rgb,
            interpolation="nearest"
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_title(f"Generation: {self.game.generation}")

        self.canvas.draw()
        return []


class GameOfLife:
    def __init__(self, height, width):
        self.field = np.random.randint(0, 2, size=(height, width))
        self.generation = 0

    def checkAlive(self):
        # Матрица числа соседей
        neighbours = np.zeros(self.field.shape, dtype = int)

        # Подсчёт соседей смещением
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                neighbours += np.roll(np.roll(self.field, dx, axis=0), dy, axis=1)

        return neighbours

    def step(self):
        # Матрица соседей
        neighbours = self.checkAlive()
        
        # Живые клетки на текущем шаге
        alive = (self.field == 1)
        # Рождающиеся клетки на следующем шаге
        birth = (neighbours == 3) & (~alive)
        # Выживающие клетки с предыдущего хода
        survive = np.isin(neighbours, (2, 3)) & alive

        # Преобразование карты
        self.field = (birth | survive).astype(int)
        self.generation += 1

if __name__ == '__main__':
    root = tk.Tk()
    app = GameOfLifeUI(root)
    root.mainloop()
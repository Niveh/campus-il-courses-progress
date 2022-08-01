import tkinter as tk

FONT = "Helvetica 14"

root = tk.Tk()

img = tk.PhotoImage(file="task_6_1_3_image.png")
img_displayed = False


def show_image():
    global img_displayed
    if not img_displayed:
        tk.Label(root, image=img).pack()
        img_displayed = True


def init_gui():
    question = tk.Label(text="What is my favorite video?", font=FONT)
    question.pack()

    button = tk.Button(text="Click here to find out!",
                       command=show_image)
    button.pack()


def main():
    init_gui()

    root.mainloop()


if __name__ == "__main__":
    main()

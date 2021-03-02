import tkinter as tk

def handle_keypress(event):
    """Print the character associated to the key pressed"""
    print(event.char)

def handle_click(event):
    print("The button was clicked!")

window = tk.Tk()

button = tk.Button(master=window, text="Click me!")
button.grid(row=0, column=0, sticky="nsew")

button.bind("<Button-1>", handle_click)

window.bind("<Key>", handle_keypress)

window.mainloop()
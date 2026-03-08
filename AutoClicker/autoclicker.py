import customtkinter as ctk
import threading
import time
import random
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Listener

# ─────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

running = False
exit_requested = False
mouse = Controller()

# ─────────────────────────────
def clicker_thread():
    global running

    cps = cps_slider.get()
    click_button = Button.left if click_type.get() == "left" else Button.right

    while running and not exit_requested:

        if randomize_var.get():
            cps_now = random.uniform(cps * 0.8, cps * 1.2)
        else:
            cps_now = cps

        delay = 1.0 / cps_now
        mouse.click(click_button, 1)
        time.sleep(delay)

# ─────────────────────────────
def toggle_clicker():
    global running

    if not running:
        running = True
        toggle_button.configure(text="STOP")
        status_label.configure(text="RUNNING", text_color="#00ff9c")

        thread = threading.Thread(target=clicker_thread, daemon=True)
        thread.start()

    else:
        running = False
        toggle_button.configure(text="START")
        status_label.configure(text="STOPPED", text_color="#ff4d4d")

# ─────────────────────────────
def update_cps(value):
    cps_label.configure(text=f"{int(value)} CPS")

# ─────────────────────────────
def on_press(key):
    global exit_requested

    try:
        if getattr(key, "char", None) == "k":
            app.after(0, toggle_clicker)

        if key == Key.esc:
            exit_requested = True
            app.after(0, app.quit)

    except:
        pass

# ─────────────────────────────
# APP WINDOW
app = ctk.CTk()
app.title("Auto Clicker")
app.geometry("420x360")
app.resizable(False, False)

# ─────────────────────────────
title = ctk.CTkLabel(app, text="Auto Clicker", font=("Segoe UI", 24, "bold"))
title.pack(pady=20)

status_label = ctk.CTkLabel(app, text="STOPPED", text_color="#ff4d4d", font=("Segoe UI", 14))
status_label.pack(pady=5)

# ─────────────────────────────
cps_slider = ctk.CTkSlider(app, from_=1, to=50, command=update_cps)
cps_slider.set(25)
cps_slider.pack(pady=15, padx=40, fill="x")

cps_label = ctk.CTkLabel(app, text="25 CPS")
cps_label.pack()

# ─────────────────────────────
click_type = ctk.StringVar(value="left")

click_frame = ctk.CTkFrame(app)
click_frame.pack(pady=15)

left_btn = ctk.CTkRadioButton(click_frame, text="Left Click", variable=click_type, value="left")
left_btn.grid(row=0, column=0, padx=20, pady=10)

right_btn = ctk.CTkRadioButton(click_frame, text="Right Click", variable=click_type, value="right")
right_btn.grid(row=0, column=1, padx=20, pady=10)

# ─────────────────────────────
randomize_var = ctk.BooleanVar()

random_checkbox = ctk.CTkCheckBox(
    app,
    text="Randomize CPS (Human-like)",
    variable=randomize_var
)
random_checkbox.pack(pady=10)

# ─────────────────────────────
toggle_button = ctk.CTkButton(app, text="START", command=toggle_clicker, width=200, height=40)
toggle_button.pack(pady=20)

hotkey_label = ctk.CTkLabel(app, text="K = Toggle  |  ESC = Quit", font=("Segoe UI", 10))
hotkey_label.pack()

# ─────────────────────────────
listener = Listener(on_press=on_press)
listener.start()

app.mainloop()

exit_requested = True
listener.stop()
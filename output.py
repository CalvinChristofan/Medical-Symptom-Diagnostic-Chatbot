from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage, Label, Frame, Toplevel, IntVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
import tkinter as tk
from matplotlib.colors import to_hex
import textwrap
import json
import subprocess

# Set up file paths (Note : Please change all path correspond with directory in your computer)
JSON_PATH = "output_data.json"
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("outputasset")
MAIN_PYTHON_PATH = "main.py"

colors = {
    "bg": "#222222",
    "tooltip_bg": "#333533",
    "tooltip_fg": "#C8FACC",
    "header": "#2E3440",
    "accent": "#5DADEC",
    "text": "#ECEFF4",
    "text_light": "#A3BE8C",
    "hover": "#81A1C1",
    "star_hover": "#BF616A",
}

with open(JSON_PATH, "r") as file:
    diseases = json.load(file)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = tk.Tk()
window.geometry("1536x864")
window.configure(bg=colors["bg"])
window.title("Diagno - Medical Diagnostic Bot")

disease_df = pd.DataFrame(diseases).T
disease_df["similarity_percentage"] = [float(x) for x in disease_df["similarity"]]
wrapped_names = [textwrap.fill(name, width=13) for name in disease_df.index]
palette = sns.light_palette("#29A745", n_colors=200, reverse=True)
bar_colors = [to_hex(palette[int(similarity * 2)]) for similarity in disease_df["similarity_percentage"]]

canvas = Canvas(
    window,
    bg=colors["bg"],
    height=864,
    width=1536,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(
    946.0,
    1138.0,
    image=image_image_1
)

chart_frame = Canvas(window, bg=colors["bg"])
chart_frame.place(x=40, y=100, width=650, height=500)

fig = Figure(figsize=(6, 5), dpi=100, facecolor=colors["bg"])
ax = fig.add_subplot()

sns.barplot(
    y=wrapped_names,  
    x="similarity_percentage",
    data=disease_df,
    palette=bar_colors,
    ax=ax,
)

ax.set_facecolor(colors["bg"])
ax.tick_params(colors="#FFFFFF", labelsize=12)
ax.set_xlabel("Similarity (%)", color="#FFFFFF", fontsize=14)
ax.set_title("Top Diseases", color="#FFFFFF", fontsize=16)
ax.set_xlim(0, 100)
fig.subplots_adjust(left=0.25, right=0.95)

chart_canvas = FigureCanvasTkAgg(fig, chart_frame)
chart_canvas_widget = chart_canvas.get_tk_widget()
chart_canvas_widget.pack()

bar_mapping = []
for rect, disease in zip(ax.patches, disease_df.index):
    bar_mapping.append({"rect": rect, "disease": disease})

tooltip = Label(chart_canvas_widget, bg=colors["tooltip_bg"], fg=colors["tooltip_fg"], font=("Inter", 12), relief="solid", bd=1)
tooltip.place_forget()

def show_tooltip(event):
    canvas_coords = chart_canvas_widget.winfo_pointerxy()
    canvas_x, canvas_y = canvas_coords[0], canvas_coords[1]

    for bar in bar_mapping:
        rect = bar["rect"]
        bbox = rect.get_window_extent(fig.canvas.get_renderer())
        left, bottom, right, top = bbox.x0, bbox.y0, bbox.x1, bbox.y1

        if left <= event.x <= right and bottom <= event.y <= top:
            disease = bar["disease"]
            similarity = float(diseases[disease]["similarity"])
            tooltip.config(text=f"{disease}: {similarity:.1f}%")
            tooltip.place(x=canvas_x, y=canvas_y - 100)
            return

    tooltip.place_forget()

def on_bar_click(event):
    for bar in bar_mapping:
        rect = bar["rect"]
        if rect.contains(event)[0]:
            selected_disease = bar["disease"]
            description = diseases[selected_disease]["description"]
            symptoms = diseases[selected_disease]["symptoms"].split(", ")
            solution = diseases[selected_disease]["solution"].split(". ")

            description_box.config(state="normal")
            symptoms_box.config(state="normal")
            solution_box.config(state="normal")

            description_box.delete("1.0", "end")
            symptoms_box.delete("1.0", "end")
            solution_box.delete("1.0", "end")

            description_box.insert("1.0", description)

            for symptom in symptoms:
                symptoms_box.insert("end", f"• {symptom}\n")

            for treatment in solution:
                solution_box.insert("end", f"• {treatment.strip()}\n")
            
            description_box.config(state="disabled")
            symptoms_box.config(state="disabled")
            solution_box.config(state="disabled")
            break

chart_canvas.mpl_connect("motion_notify_event", show_tooltip)
fig.canvas.mpl_connect("button_press_event", on_bar_click)

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
canvas.create_image(
    1112.0,
    174.0,
    image=image_image_4
)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
canvas.create_image(
    1303.0,
    524.0,
    image=image_image_3
)

image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
canvas.create_image(
    920.0,
    524.0,
    image=image_image_5
)

canvas.create_text(
    785.0,
    85.0,
    anchor="nw",
    text="Description",
    fill="#FFFFFF",
    font=("Inter Bold", 20 * -1)
)

description_box = Text(
    window,
    bg="#222222",
    fg="#FFFFFF",
    wrap="word",
    font=("Inter", 14),
    bd=0,
    padx=10,
    pady=10
)
description_box.place(x=770.0, y=118.0, width=683.0, height=138.0)
description_box.insert("1.0", "Click a disease bar to view the description.")
description_box.config(state="disabled")

canvas.create_text(
    785.0,
    340.0,
    anchor="nw",
    text="Symptoms",
    fill="#FFFFFF",
    font=("Inter Bold", 20 * -1)
)

symptoms_box = Text(
    window,
    bg="#222222",
    fg="#FFFFFF",
    wrap="word",
    font=("Inter", 14),
    bd=0,
    padx=10,
    pady=10
)
symptoms_box.place(x=768.0, y=375.0, width=303.0, height=327.0)
symptoms_box.insert("1.0", "Click a disease bar to view the symptoms.")
symptoms_box.config(state="disabled")

canvas.create_text(
    1169.0,
    340.0,
    anchor="nw",
    text="Solution",
    fill="#FFFFFF",
    font=("Inter Bold", 20 * -1)
)

solution_box = Text(
    window,
    bg="#222222",
    fg="#FFFFFF",
    wrap="word",
    font=("Inter", 14),
    bd=0,
    padx=10,
    pady=10
)
solution_box.place(x=1151.0, y=375.0, width=303.0, height=327.0)
solution_box.insert("1.0", "Click a disease bar to view the solution.")
solution_box.config(state="disabled")

footer = Frame(window, bg=colors["header"], height=50)
footer.pack(side="bottom", fill="x")

footer_label = Label(
    footer, text="Medical Diagnostic Bot © 2024", bg=colors["header"], fg=colors["text_light"], font=("Inter", 12)
)
footer_label.pack(pady=10)

def open_rating_window():
    rate_window = Toplevel()
    rate_window.title("Rate Us")
    rate_window.configure(bg=colors["bg"])

    title_label = Label(rate_window, text="Rate Us", font=("Inter Bold", 16), bg=colors["bg"], fg=colors["text"])
    title_label.pack(pady=10)

    rating_var = IntVar()
    rating_var.set(0)

    def select_star(star):
        rating_var.set(star)
        for i in range(1, 6):
            stars[i - 1]["text"] = "★" if i <= star else "☆"

    def hover_star(button, enter):
        button["bg"] = colors["star_hover"] if enter else colors["accent"]

    stars = []
    stars_frame = Frame(rate_window, bg=colors["bg"])
    stars_frame.pack(pady=10)
    for i in range(1, 6):
        star_button = Button(
            stars_frame, text="☆", font=("Arial", 24), bg=colors["accent"], fg="white", relief="flat",
            command=lambda i=i: select_star(i)
        )
        star_button.pack(side="left", padx=5)
        stars.append(star_button)

        star_button.bind("<Enter>", lambda e, b=star_button: hover_star(b, True))
        star_button.bind("<Leave>", lambda e, b=star_button: hover_star(b, False))

    feedback_label = Label(
        rate_window, text="Leave your feedback:", bg=colors["bg"], fg=colors["text"], font=("Inter", 12)
    )
    feedback_label.pack(pady=10)

    feedback_box = Text(rate_window, height=5, width=40, wrap="word", font=("Inter", 12), padx=10, pady=10)
    feedback_box.pack()

    def submit_feedback():
        rating = rating_var.get()
        feedback = feedback_box.get("1.0", "end").strip()
        if rating > 0 or feedback:
            print(f"Rating: {rating} stars\nFeedback: {feedback}")
            rate_window.destroy()
        else:
            print("No rating or feedback given.")

    submit_button = Button(
        rate_window, text="Submit", bg=colors["accent"], fg="white", font=("Inter Bold", 14), relief="flat",
        command=submit_feedback
    )
    submit_button.pack(pady=20)

    submit_button.bind("<Enter>", lambda e: submit_button.config(bg=colors["hover"]))
    submit_button.bind("<Leave>", lambda e: submit_button.config(bg=colors["accent"]))

rate_button = Button(
    window, text="Rate Us", bg="#29A745", fg="white", font=("Inter Bold", 14), relief="flat",
    command=open_rating_window
)
rate_button.place(relx=0.95, rely=0.95, anchor="se")


def go_back():
    print("Back button clicked. Returning to the previous page.")
    
    window.destroy()
        
    subprocess.Popen(["python", MAIN_PYTHON_PATH])


back_button = Button(
    window, text="Back", bg="#29A745", fg="white", font=("Inter Bold", 14), relief="flat",
    command=go_back
)
back_button.place(relx=0.05, rely=0.95, anchor="sw")


window.resizable(True, True)
window.mainloop()

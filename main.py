import json
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage, Scrollbar, Frame
from tkinter.ttk import Scrollbar, Style
from backend_preprocessing import preprocess_input,predict

# Set up file paths (Note : Please change all path correspond with directory in your computer)
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("mainasset")
JSON_PATH = "output_data.json"
OUTPUT_PYTHON_PATH = "output.py"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

full_text = "What can I help you with?"
current_text = ""
index = 0


def type_text():
    global index, current_text
    if index < len(full_text):
        current_text += full_text[index]
        canvas.itemconfigure(animated_text, text=current_text)
        index += 1
        window.after(50, type_text)


#User Input, Preprocess, Predict, Save to json, close main.py, and run output.py
def handle_send():
    user_input = input_box.get("1.0", "end-1c").strip()  
    if user_input:
        print(f"User input: {user_input}")
        input_data = preprocess_input(user_input)
        predictions = predict(input_data)
        
        predictions =  {k: v for k, v in predictions.items()}
        
        with open(JSON_PATH, "w") as file:
            json.dump(predictions, file, indent= 4)  # Save predictions to a JSON file
       
        window.destroy()
        subprocess.Popen(["python", OUTPUT_PYTHON_PATH]) 


window = tk.Tk()
window.geometry("1536x864")
window.title("Diagno - Medical Diagnostic Bot")
window.configure(bg="#000000")

canvas = Canvas(
    window,
    bg="#000000",
    height=864,
    width=1536,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)


image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
canvas.create_image(
    782.0,
    446.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
canvas.create_image(
    782.0,  
    1000.0,  
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
canvas.create_image(
    820.0,  
    235.0,  
    image=image_image_3
)

animated_text = canvas.create_text(
    416.0,
    269.0,
    anchor="nw",
    text="",
    fill="#E5E5E5",
    font=("Inter SemiBold", 54 * -1)
)
window.after(200, type_text)  

canvas.create_text(
    598.0,
    209.0,
    anchor="nw",
    text="Hi, I’m",
    fill="#E5E5E5",
    font=("Inter Bold", 40 * -1)
)

canvas.create_text(
    741.0,
    209.0,
    anchor="nw",
    text="Diagno",
    fill="#E5E5E5",
    font=("Inter Bold", 40 * -1)
)

style = Style()
style.theme_use("clam")  
style.configure(
    "Custom.Vertical.TScrollbar",
    background="#4D4D4D",  
    troughcolor="#2A2A2A",  
    bordercolor="#2A2A2A",  
    arrowcolor="#FFFFFF",  
    relief="flat",  
)

input_frame = Frame(window, bg="#000000")
input_frame.place(x=375, y=390)  

input_box = Text(
    input_frame,
    width=50,
    height=3,  
    wrap="word",
    font=("Inter Medium", 18),
    bg="#2A2A2A",
    fg="#FFFFFF",
    highlightbackground="#4D4D4D",
    highlightthickness=1,
    relief="flat",  
    insertbackground="#FFFFFF",  
)

input_box.grid(row=0, column=0, sticky="nsew")  

scrollbar = Scrollbar(
    input_frame,
    orient="vertical",
    command=input_box.yview,
    style="Custom.Vertical.TScrollbar", 
)

scrollbar.grid(row=0, column=1, sticky="ns")  

input_box.config(yscrollcommand=scrollbar.set)

input_frame.grid_rowconfigure(0, weight=1)
input_frame.grid_columnconfigure(0, weight=1)

style.map("Custom.Vertical.TScrollbar", 
    background=[("disabled", "#4D4D4D")],  
    arrowcolor=[("disabled", "#4D4D4D")],  
    troughcolor=[("disabled", "#2A2A2A")], 
)

send_button = Button(
    window,
    text="➤",
    width=5,
    height=2,
    bg="#097F4D",
    activebackground="#4B6C7E",
    fg="white",
    font=("Inter Medium", 18),
    command=handle_send
)
send_button.place(x=1050, y=398)  

def animate_description(item_id, target_y, step=5, delay=10):
    current_coords = canvas.coords(item_id)
    if current_coords[1] > target_y:  
        canvas.move(item_id, 0, -step)  
        window.after(delay, animate_description, item_id, target_y, step, delay)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
desc1_image = canvas.create_image(
    472.0,
    800.0, 
    image=image_image_5
)

desc1_text1 = canvas.create_text(
    390.5,
    800.0,  
    anchor="nw",
    text="Similarity Calculation",
    fill="#E5E5E5",
    font=("Inter Medium", 16 * -1)
)

desc1_text2 = canvas.create_text(
    360.0,
    850.0, 
    anchor="nw",
    text="Quickly analyze and compare patterns to identify relationships and trends with precision.",
    width=200,
    fill="#E5E5E5",
    font=("Inter Light", 14 * -1)
)


animate_description(desc1_image, 521.0)  
animate_description(desc1_text1, 538.0)  
animate_description(desc1_text2, 580.0)  

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
desc2_image = canvas.create_image(
    738.833, 
    800.0,  
    image=image_image_7
)

desc2_text1 = canvas.create_text(
    639.0,
    800.0,  
    anchor="nw",
    text="Identifying 300+ diseases",
    fill="#E5E5E5",
    font=("Inter Medium", 16 * -1)
)

desc2_text2 = canvas.create_text(
    629.0,
    850.0,  
    anchor="nw",
    text="Harness advanced algorithms to accurately recognize over 300 diseases based on input data.",
    width=200,
    fill="#E5E5E5",
    font=("Inter Light", 14 * -1)
)

animate_description(desc2_image, 519.833)  
animate_description(desc2_text1, 538.0)  
animate_description(desc2_text2, 580.0) 


image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
desc3_image = canvas.create_image(
    996.667,
    800.0,  
    image=image_image_8
)

desc3_text1 = canvas.create_text(
    930.5,
    800.0,  
    anchor="nw",
    text="Instant Diagnosis",
    fill="#E5E5E5",
    font=("Inter Medium", 16 * -1)
)

desc3_text2 = canvas.create_text(
    896.0,
    850.0,  
    anchor="nw",
    text="Deliver real-time diagnostic results for timely and informed decision-making.",
    width=200,
    fill="#E5E5E5",
    font=("Inter Light", 14 * -1)
)

animate_description(desc3_image, 520.0)  
animate_description(desc3_text1, 538.0)  
animate_description(desc3_text2, 580.0)  

window.resizable(True, True)
window.mainloop()

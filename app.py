import customtkinter as ctk
from transformers import AutoTokenizer
import random
from PIL import Image, ImageTk
from customtkinter import CTkImage

# Setup CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def get_text_color(bg_hex):
    r = int(bg_hex[1:3], 16)
    g = int(bg_hex[3:5], 16)
    b = int(bg_hex[5:7], 16)
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    return "black" if luma > 150 else "white"

def count_and_highlight_tokens():
    text_display.configure(state="normal")
    text_display.delete("1.0", "end")

    raw_text = text_input.get("1.0", "end-1c")  # Keeps final \n
    if not raw_text.strip():
        output_label.configure(text="0")
        char_label.configure(text="0")
        return

    text_display.insert("1.0", raw_text)

    encoded = tokenizer.encode_plus(raw_text, return_offsets_mapping=True, add_special_tokens=False)
    tokens = tokenizer.convert_ids_to_tokens(encoded["input_ids"])
    offsets = encoded["offset_mapping"]

    output_label.configure(text=f"{len(tokens)}")
    char_label.configure(text=f"{len(raw_text)}")

    for idx, ((start, end), token) in enumerate(zip(offsets, tokens)):
        if end <= len(raw_text):
            start_idx = f"1.0+{start}c"
            end_idx = f"1.0+{end}c"
            tag_name = f"token{idx}"
            bg_color = random_color()
            fg_color = get_text_color(bg_color)
            text_display.tag_add(tag_name, start_idx, end_idx)
            text_display.tag_config(tag_name, background=bg_color, foreground=fg_color)

    text_display.configure(state="disabled")

# App setup
app = ctk.CTk()
app.title("Tokenizer Playground")
app.geometry("900x700")
app.resizable(False, False)

# Load PNG image with aspect ratio maintained
image_path = "icon.png"  # Make sure the file exists
img = Image.open(image_path)

# Set maximum height (e.g. 64px) and calculate proportional width
max_height = 64
w_percent = (max_height / float(img.height))
new_width = int((float(img.width) * float(w_percent)))
img = img.resize((new_width, max_height), Image.LANCZOS)

# img_ctk = ImageTk.PhotoImage(img)
img_ctk = ImageTk.PhotoImage(img)

# Title with image
header_frame = ctk.CTkFrame(app, fg_color="transparent")
header_frame.pack(pady=(20, 10))

img_label = ctk.CTkLabel(header_frame, image=img_ctk, text="")
img_label.pack(side="left", padx=(0, 10))

title_label = ctk.CTkLabel(header_frame, text="Tokenizer Playground", font=ctk.CTkFont(size=35, weight="bold"))
title_label.pack(side="left")


header_frame = ctk.CTkFrame(app, fg_color="transparent")
header_frame.pack(pady=(0, 10))

# Subtitle
subtitle_label = ctk.CTkLabel(header_frame, text="Using BERT Tokenizer (bert-base-uncased)", font=ctk.CTkFont(size=14, weight="normal"))
subtitle_label.pack(side="left", padx=(10, 0))

# Input frame
input_frame = ctk.CTkFrame(app, fg_color="transparent")
input_frame.pack(pady=10, padx=20, fill="both")

ctk.CTkLabel(input_frame, text="Enter text:").pack(anchor="w", pady=5, padx=5)
text_input = ctk.CTkTextbox(input_frame, height=150)
text_input.pack(padx=5, pady=5, fill="x")

ctk.CTkButton(app, text="Analyze", command=count_and_highlight_tokens).pack(pady=10)

# Create a Frame to center the KPIs
kpi_frame = ctk.CTkFrame(app, fg_color="transparent")
kpi_frame.pack(pady=20, padx=20, anchor="center")

# Create a frame that contains the two KPIs side by side and center them
kpi_content_frame = ctk.CTkFrame(kpi_frame, fg_color="transparent")
kpi_content_frame.pack(side="top", anchor="center")

# KPI Token
kpi_token_frame = ctk.CTkFrame(kpi_content_frame, fg_color="transparent")
kpi_token_frame.pack(side="left", padx=10)

ctk.CTkLabel(kpi_token_frame, text="TOKENS", font=ctk.CTkFont(size=20, weight="bold")).pack()
output_label = ctk.CTkLabel(kpi_token_frame, text="0", font=ctk.CTkFont(size=25, weight="bold"))
output_label.pack()

# KPI Characters
kpi_char_frame = ctk.CTkFrame(kpi_content_frame, fg_color="transparent")
kpi_char_frame.pack(side="left", padx=10)

ctk.CTkLabel(kpi_char_frame, text="CHARACTERS", font=ctk.CTkFont(size=20, weight="bold")).pack()
char_label = ctk.CTkLabel(kpi_char_frame, text="0", font=ctk.CTkFont(size=25, weight="bold"))
char_label.pack()

ctk.CTkLabel(app, text="Result:").pack(anchor="w", padx=20, pady=(0, 0))
text_display = ctk.CTkTextbox(app, height=250, state="disabled")
text_display.pack(padx=20, pady=(5, 20), fill="x")

app.mainloop()

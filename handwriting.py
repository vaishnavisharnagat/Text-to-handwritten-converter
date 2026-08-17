import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont
import os
import io
import base64


# =========================================================
# FIND WINDOWS FONT
# =========================================================

def get_font(size):

    fonts = [
        r"C:\Windows\Fonts\segoepr.ttf",
        r"C:\Windows\Fonts\segoeprb.ttf",
        r"C:\Windows\Fonts\comic.ttf",
        r"C:\Windows\Fonts\arial.ttf"
    ]

    for font_path in fonts:
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)

    return ImageFont.load_default()


# =========================================================
# FIND DESKTOP
# =========================================================

def get_desktop():

    # Check OneDrive Desktop first
    onedrive_desktop = os.path.join(
        os.path.expanduser("~"),
        "OneDrive",
        "Desktop"
    )

    if os.path.exists(onedrive_desktop):
        return onedrive_desktop

    # Normal Windows Desktop
    normal_desktop = os.path.join(
        os.path.expanduser("~"),
        "Desktop"
    )

    if os.path.exists(normal_desktop):
        return normal_desktop

    # Current folder as final fallback
    return os.getcwd()


# =========================================================
# CONVERT TEXT
# =========================================================

def convert():

    text = text_box.get(
        "1.0",
        tk.END
    ).strip()

    if not text:

        messagebox.showwarning(
            "Warning",
            "Please enter some text first."
        )

        return

    try:

        # =================================================
        # A4 PAGE
        # =================================================

        width = 1240
        height = 1754

        image = Image.new(
            "RGB",
            (width, height),
            "white"
        )

        draw = ImageDraw.Draw(image)

        # =================================================
        # FONT
        # =================================================

        font = get_font(38)

        # =================================================
        # POSITION
        # =================================================

        x = 120
        y = 90

        line_height = 65

        max_width = 1000

        # =================================================
        # NOTEBOOK LINES
        # =================================================

        for line_y in range(
            145,
            height - 50,
            line_height
        ):

            draw.line(
                (
                    70,
                    line_y,
                    width - 70,
                    line_y
                ),
                fill=(210, 220, 230),
                width=2
            )

        # =================================================
        # RED MARGIN
        # =================================================

        draw.line(
            (
                80,
                50,
                80,
                height - 50
            ),
            fill=(230, 150, 150),
            width=2
        )

        # =================================================
        # WRITE TEXT
        # =================================================

        for paragraph in text.split("\n"):

            words = paragraph.split()

            current_line = ""

            for word in words:

                if current_line:

                    test_line = (
                        current_line + " " + word
                    )

                else:

                    test_line = word

                bbox = draw.textbbox(
                    (0, 0),
                    test_line,
                    font=font
                )

                text_width = (
                    bbox[2] - bbox[0]
                )

                if text_width <= max_width:

                    current_line = test_line

                else:

                    if current_line:

                        draw.text(
                            (x, y),
                            current_line,
                            font=font,
                            fill=(20, 40, 110)
                        )

                        y += line_height

                    current_line = word

                if y > height - 100:
                    break

            # Write remaining text
            if current_line and y <= height - 100:

                draw.text(
                    (x, y),
                    current_line,
                    font=font,
                    fill=(20, 40, 110)
                )

                y += line_height

            # Paragraph spacing
            y += 10

            if y > height - 100:
                break

        # =================================================
        # SAVE TO REAL DESKTOP
        # =================================================

        desktop = get_desktop()

        output_file = os.path.join(
            desktop,
            "handwritten_output.png"
        )

        image.save(output_file)

        # =================================================
        # SHOW RESULT
        # =================================================

        show_result(
            image,
            output_file
        )

    except Exception as error:

        messagebox.showerror(
            "Error",
            str(error)
        )


# =========================================================
# SHOW RESULT
# =========================================================

def show_result(image, filename):

    result_window = tk.Toplevel(root)

    result_window.title(
        "Handwriting Output"
    )

    result_window.geometry(
        "800x700"
    )

    # Create preview
    preview = image.copy()

    preview.thumbnail(
        (700, 580)
    )

    # Convert PIL image to Tkinter image
    buffer = io.BytesIO()

    preview.save(
        buffer,
        format="PNG"
    )

    photo = tk.PhotoImage(
        data=base64.b64encode(
            buffer.getvalue()
        )
    )

    image_label = tk.Label(
        result_window,
        image=photo
    )

    image_label.image = photo

    image_label.pack(
        pady=10
    )

    # File location
    info = tk.Label(
        result_window,
        text="Saved successfully!",
        font=("Arial", 13, "bold")
    )

    info.pack(
        pady=5
    )

    location = tk.Label(
        result_window,
        text=filename,
        font=("Arial", 9),
        wraplength=700
    )

    location.pack(
        pady=5
    )


# =========================================================
# CLEAR
# =========================================================

def clear_text():

    text_box.delete(
        "1.0",
        tk.END
    )


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Text to Handwriting Generator"
)

root.geometry(
    "800x600"
)

root.resizable(
    False,
    False
)


# =========================================================
# TITLE
# =========================================================

title = tk.Label(
    root,
    text="✍ Text to Handwriting Generator",
    font=("Arial", 24, "bold")
)

title.pack(
    pady=15
)


# =========================================================
# TEXT BOX
# =========================================================

text_box = tk.Text(
    root,
    width=75,
    height=18,
    font=("Arial", 12),
    wrap=tk.WORD
)

text_box.pack(
    padx=20,
    pady=10
)


# =========================================================
# BUTTONS
# =========================================================

button_frame = tk.Frame(root)

button_frame.pack(
    pady=10
)


convert_button = tk.Button(
    button_frame,
    text="✍ CONVERT",
    font=("Arial", 13, "bold"),
    bg="black",
    fg="white",
    padx=35,
    pady=10,
    command=convert
)

convert_button.pack(
    side=tk.LEFT,
    padx=10
)


clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    font=("Arial", 13),
    padx=35,
    pady=10,
    command=clear_text
)

clear_button.pack(
    side=tk.LEFT,
    padx=10
)


# =========================================================
# FOOTER
# =========================================================

footer = tk.Label(
    root,
    text="No handwriting.ttf required",
    font=("Arial", 9),
    fg="gray"
)

footer.pack(
    pady=5
)


# =========================================================
# START
# =========================================================

root.mainloop()
import tkinter as tk
from tkinter import ttk
import traceback
import io
import contextlib

# ==================================================
# COLOUR THEME
# ==================================================

BG = "#211B18"
PANEL = "#382D26"
INPUT_BG = "#302722"
CARD = "#44362D"
YELLOW = "#F4C928"
WHITE = "#FFFFFF"
MUTED = "#BDB0A5"
GREEN = "#23865C"
RED = "#B84D43"


# ==================================================
# ROUNDED CORNER DESIGN
# ==================================================

def rounded_points(x1, y1, x2, y2, radius=20):

    return [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]


def rounded_panel(parent, height, color):

    panel = tk.Canvas(
        parent,
        height=height,
        bg=BG,
        highlightthickness=0
    )

    shape = panel.create_polygon(
        rounded_points(2, 2, 800, height - 2, 22),
        smooth=True,
        splinesteps=36,
        fill=color,
        outline=color
    )

    content = tk.Frame(panel, bg=color)

    window = panel.create_window(
        18, 14,
        anchor="nw",
        window=content
    )

    def resize(event):

        panel.coords(
            shape,
            *rounded_points(
                2, 2,
                event.width - 2,
                height - 2,
                22
            )
        )

        panel.coords(window, 18, 14)

        panel.itemconfigure(
            window,
            width=max(100, event.width - 36)
        )

    panel.bind("<Configure>", resize)

    return panel, content


# ==================================================
# DEBUGGING ENGINE
# ==================================================

def analyze_code(source):

    if not source.strip():
        return {"status": "empty"}

    output = io.StringIO()

    try:

        compiled = compile(
            source,
            "<user_code>",
            "exec"
        )

        with contextlib.redirect_stdout(output):
            exec(compiled, {"__name__": "__main__"})

        return {
            "status": "success",
            "output": output.getvalue()
        }

    except Exception as error:

        frames = traceback.extract_tb(
            error.__traceback__
        )

        user_frames = [
            frame for frame in frames
            if frame.filename == "<user_code>"
        ]

        line = "Not available"
        faulty = "Not available"

        if isinstance(error, SyntaxError):

            if error.lineno:
                line = str(error.lineno)

            if error.text:
                faulty = error.text.strip()

        elif user_frames:

            frame = user_frames[-1]
            line = str(frame.lineno)

            source_lines = source.splitlines()

            if 1 <= frame.lineno <= len(source_lines):
                faulty = source_lines[
                    frame.lineno - 1
                ].strip()

        error_type = type(error).__name__

        rules = {

            "ZeroDivisionError": (
                "You attempted to divide a number by zero.",
                "Check the denominator before division."
            ),

            "NameError": (
                "A variable or function is not defined.",
                "Check the spelling and define the variable."
            ),

            "TypeError": (
                "You used incompatible data types.",
                "Check and convert the data types."
            ),

            "ValueError": (
                "A function received an invalid value.",
                "Check the input value."
            ),

            "IndexError": (
                "You accessed an invalid list index.",
                "Check the list length and index."
            ),

            "KeyError": (
                "The requested dictionary key does not exist.",
                "Check the key or use get()."
            ),

            "SyntaxError": (
                "Python found invalid syntax.",
                "Check brackets, colons and quotation marks."
            ),

            "IndentationError": (
                "Your code has incorrect indentation.",
                "Use consistent four-space indentation."
            ),

            "ModuleNotFoundError": (
                "Python cannot find the requested module.",
                "Install the required module."
            ),

            "FileNotFoundError": (
                "The requested file does not exist.",
                "Check the filename and file path."
            ),

            "AttributeError": (
                "The object does not have this attribute.",
                "Check the object and attribute name."
            )
        }

        explanation, solution = rules.get(
            error_type,
            (
                "An unexpected error occurred.",
                "Inspect the traceback and check your code."
            )
        )

        return {
            "status": "error",
            "error": error_type,
            "message": str(error),
            "line": line,
            "faulty": faulty,
            "explanation": explanation,
            "solution": solution,
            "traceback": traceback.format_exc(),
            "output": output.getvalue()
        }


# ==================================================
# MAIN WINDOW
# ==================================================

root = tk.Tk()

root.title("Debugging Assistant")
root.geometry("1000x900")
root.minsize(750, 650)

root.configure(bg=BG)


# ==================================================
# HEADER
# ==================================================

header = tk.Frame(
    root,
    bg=BG
)

header.pack(
    fill="x",
    padx=35,
    pady=(25, 15)
)

tk.Label(
    header,
    text="✦ DEBUGGING ASSISTANT",
    font=("Arial", 23, "bold"),
    bg=BG,
    fg=YELLOW
).pack(side="left")

tk.Label(
    header,
    text="● SYSTEM ACTIVE",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg="#54D69A"
).pack(side="right")


# ==================================================
# FLOATING INPUT CARD
# ==================================================

input_shadow = tk.Frame(
    root,
    bg="#171210"
)

input_shadow.pack(
    fill="x",
    padx=29,
    pady=(12, 0)
)

input_panel, input_content = rounded_panel(
    input_shadow,
    280,
    PANEL
)

input_panel.pack(
    fill="x",
    padx=(0, 4),
    pady=(0, 5)
)


# Input heading

tk.Label(
    input_content,
    text="✦  PASTE YOUR PYTHON CODE",
    font=("Arial", 13, "bold"),
    bg=PANEL,
    fg=YELLOW
).pack(
    anchor="w",
    pady=(7, 12)
)


# Code editor background

editor_frame = tk.Frame(
    input_content,
    bg=INPUT_BG,
    padx=12,
    pady=10
)

editor_frame.pack(
    fill="x",
    pady=(0, 10)
)

code_input = tk.Text(
    editor_frame,
    height=8,
    font=("Consolas", 12),
    bg=INPUT_BG,
    fg=WHITE,
    insertbackground=YELLOW,
    selectbackground="#66502A",
    relief="flat",
    borderwidth=0,
    wrap="none"
)

code_input.pack(
    fill="both",
    expand=True
)


tk.Label(
    input_content,
    text="Paste your code and click ANALYZE CODE",
    font=("Arial", 9),
    bg=PANEL,
    fg=MUTED
).pack(anchor="w")


# ==================================================
# BUTTONS
# ==================================================

button_frame = tk.Frame(
    root,
    bg=BG
)

button_frame.pack(
    fill="x",
    padx=30,
    pady=18
)


def make_button(text, command, color):

    return tk.Button(
        button_frame,
        text=text,
        command=command,
        font=("Arial", 10, "bold"),
        bg=color,
        fg=BG if color == YELLOW else WHITE,
        activebackground=color,
        activeforeground=BG,
        relief="flat",
        bd=0,
        padx=20,
        pady=12,
        cursor="hand2"
    )


# ==================================================
# REPORT HEADING
# ==================================================

report_heading = tk.Frame(
    root,
    bg=BG
)

report_heading.pack(
    fill="x",
    padx=35,
    pady=(5, 12)
)

tk.Label(
    report_heading,
    text="DEBUGGING REPORT",
    font=("Arial", 19, "bold"),
    bg=BG,
    fg=WHITE
).pack(side="left")

tk.Label(
    report_heading,
    text="LIVE ANALYSIS",
    font=("Arial", 9, "bold"),
    bg=BG,
    fg="#54D69A"
).pack(side="right")


# ==================================================
# CUSTOM SCROLLBAR
# ==================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Custom.Vertical.TScrollbar",
    background="#705A49",
    troughcolor=BG,
    bordercolor=BG,
    arrowcolor=YELLOW,
    darkcolor="#705A49",
    lightcolor="#705A49",
    width=10
)

style.map(
    "Custom.Vertical.TScrollbar",
    background=[
        ("active", YELLOW)
    ]
)


report_area = tk.Frame(
    root,
    bg=BG
)

report_area.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 15)
)

canvas = tk.Canvas(
    report_area,
    bg=BG,
    highlightthickness=0
)

scrollbar = ttk.Scrollbar(
    report_area,
    orient="vertical",
    command=canvas.yview,
    style="Custom.Vertical.TScrollbar"
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y",
    padx=(5, 0)
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

report_frame = tk.Frame(
    canvas,
    bg=BG
)

window_id = canvas.create_window(
    (0, 0),
    window=report_frame,
    anchor="nw"
)


def update_scroll(event=None):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )

    canvas.itemconfigure(
        window_id,
        width=canvas.winfo_width()
    )


report_frame.bind(
    "<Configure>",
    update_scroll
)

canvas.bind(
    "<Configure>",
    update_scroll
)


# Mouse wheel scrolling

def mouse_scroll(event):

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    mouse_scroll
)


# ==================================================
# ROUNDED REPORT CARDS
# ==================================================

def add_report_card(title, content, color=CARD):

    content = str(content)

    height = max(
        95,
        min(230, 75 + (len(content) // 75) * 20)
    )

    card, inner = rounded_panel(
        report_frame,
        height,
        color
    )

    card.pack(
        fill="x",
        padx=10,
        pady=7
    )

    tk.Label(
        inner,
        text=title,
        font=("Arial", 11, "bold"),
        bg=color,
        fg="#D49B6F"
    ).pack(
        anchor="w",
        pady=(5, 8)
    )

    tk.Label(
        inner,
        text=content,
        font=("Arial", 11),
        bg=color,
        fg=WHITE,
        justify="left",
        anchor="w",
        wraplength=750
    ).pack(
        anchor="w",
        fill="x"
    )


# ==================================================
# DISPLAY REPORT
# ==================================================

def show_report(data):

    for widget in report_frame.winfo_children():
        widget.destroy()

    if data["status"] == "empty":

        add_report_card(
            "INPUT REQUIRED",
            "Please paste your Python code first."
        )

        return

    if data["status"] == "success":

        add_report_card(
            "✓ CODE EXECUTED SUCCESSFULLY",
            "No errors detected. Your program ran successfully.",
            GREEN
        )

        add_report_card(
            "PROGRAM OUTPUT",
            data["output"] or "No output generated."
        )

        return

    # Error detected

    add_report_card(
        "● ERROR DETECTED",
        data["error"] + "\n\n" + data["message"],
        RED
    )

    add_report_card(
        "ERROR LOCATION",
        "Line: " + data["line"]
    )

    add_report_card(
        "FAULTY CODE",
        data["faulty"]
    )

    add_report_card(
        "ERROR EXPLANATION",
        data["explanation"]
    )

    add_report_card(
        "SUGGESTED SOLUTION",
        data["solution"]
    )

    if data["output"]:

        add_report_card(
            "OUTPUT BEFORE ERROR",
            data["output"]
        )

    add_report_card(
        "COMPLETE STACK TRACE",
        data["traceback"]
    )

    add_report_card(
        "✓ ANALYSIS COMPLETED",
        "Your code has been analysed successfully.",
        GREEN
    )

    canvas.yview_moveto(0)


# ==================================================
# BUTTON FUNCTIONS
# ==================================================

def run_debugger():

    source = code_input.get(
        "1.0",
        "end-1c"
    )

    analyze_button.config(
        state="disabled",
        text="ANALYZING..."
    )

    root.update_idletasks()

    try:

        result = analyze_code(source)
        show_report(result)

    finally:

        analyze_button.config(
            state="normal",
            text="ANALYZE CODE"
        )


def clear_all():

    code_input.delete(
        "1.0",
        tk.END
    )

    for widget in report_frame.winfo_children():
        widget.destroy()

    add_report_card(
        "READY TO DEBUG",
        "Paste your Python code above. Your debugging report will appear here."
    )


def load_sample():

    clear_all()

    code_input.insert(
        "1.0",
        "a = 10\n"
        "b = 0\n"
        "result = a / b\n"
        "print(result)"
    )


# ==================================================
# BUTTON PLACEMENT
# ==================================================

analyze_button = make_button(
    "✦ ANALYZE CODE",
    run_debugger,
    YELLOW
)

analyze_button.pack(
    side="left",
    padx=5
)

make_button(
    "LOAD SAMPLE",
    load_sample,
    PANEL
).pack(
    side="left",
    padx=5
)

make_button(
    "CLEAR",
    clear_all,
    PANEL
).pack(
    side="left",
    padx=5
)


# ==================================================
# START APPLICATION
# ==================================================

clear_all()

root.mainloop()
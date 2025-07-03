import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from data_processor import process_data
import threading

def on_file_drop(event, status_label) -> None:
    file_path = event.data.strip('{}')

    if not file_path.endswith('.xlsx'):
        status_label.config(text="Error: Only .xlsx files accepted.")
        return

    out_dir = filedialog.askdirectory(
        title="Select folder to save output files",
        mustexist=True
    )

    if not out_dir:
        status_label.config(text="Cancelled: No output folder chosen.", fg="orange")
        return

    status_label.config(text="Processing file...")

    def process():
        try:
            process_data(file_path, out_dir)
            status_label.after(0, lambda: status_label.config(
                text="Files generated successfully.", fg="#2ecc71"
            ))
        except ValueError as e:
            status_label.after(0, lambda e=e: status_label.config(
                text=f"Error: {e}", fg="#e74c3c"
            ))

    threading.Thread(target=process, daemon=True).start()


def start_app() -> None:
    # Set up the root window
    root = TkinterDnD.Tk()
    root.title("PA Formatter")
    root.geometry("400x200")

    label = tk.Label(root, text="Drag and drop a .xlsx file below:")
    label.pack(pady=10)

    drop_area = tk.Label(root, text="Drop file here", relief="ridge", width=40, height=4)
    drop_area.pack()

    # noinspection PyUnresolvedReferences
    drop_area.drop_target_register(DND_FILES)
    # noinspection PyUnresolvedReferences
    drop_area.dnd_bind(
        '<<Drop>>',
        lambda event: on_file_drop(event, status_label)
    )

    status_label = tk.Label(root, text="", fg="#a29bfe")
    status_label.pack(pady=10)

    root.mainloop()
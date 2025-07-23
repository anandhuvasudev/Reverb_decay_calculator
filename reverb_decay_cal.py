# delay_calculator.py (Complete Corrected Version)

import customtkinter as ctk
import tkinter as tk

# --- Data for Note Calculations ---
# ("Display Name", multiplier_vs_quarter_note)
# A quarter note (1/4) is our baseline (1.0) because it equals one beat.
NOTE_VALUES = [
    ("Whole Note (1/1)", 4.0),
    ("Dotted Half (1/2d)", 3.0),
    ("Half Note (1/2)", 2.0),
    ("Dotted Quarter (1/4d)", 1.5),
    ("Quarter Note (1/4)", 1.0),
    ("Quarter Note Triplet (1/4t)", 2/3),
    ("Dotted Eighth (1/8d)", 0.75),
    ("Eighth Note (1/8)", 0.5),
    ("Eighth Note Triplet (1/8t)", 1/3),
    ("Dotted Sixteenth (1/16d)", 0.375),
    ("Sixteenth Note (1/16)", 0.25),
    ("Sixteenth Note Triplet (1/16t)", 1/6),
    ("Thirty-Second Note (1/32)", 0.125),
    ("Sixty-Fourth Note (1/64)", 0.0625),
]

class DelayCalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("BPM to Delay & Pre-Delay Calculator")
        self.geometry("520x680")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # --- Theme Setup ---
        ctk.set_appearance_mode("Dark") # "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")

        self.result_widgets = []

        # --- Create and Place Widgets ---
        self._create_widgets()
        
        # --- Initial Calculation ---
        self.update_calculations()

    def _create_widgets(self):
        # --- Title Frame ---
        title_frame = ctk.CTkFrame(self, corner_radius=10)
        title_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        title_label = ctk.CTkLabel(title_frame, text="Delay Time Calculator", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(padx=10, pady=10)

        # --- Input Frame ---
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        bpm_label = ctk.CTkLabel(input_frame, text="BPM:", font=ctk.CTkFont(size=14))
        bpm_label.grid(row=0, column=0, padx=(20, 10), pady=15)

        self.bpm_entry = ctk.CTkEntry(input_frame, width=100, font=ctk.CTkFont(size=14))
        self.bpm_entry.grid(row=0, column=1, padx=0, pady=15, sticky="w")
        self.bpm_entry.insert(0, "120")
        # Bind the update function to any key release in the entry box
        self.bpm_entry.bind("<KeyRelease>", self.update_calculations)

        theme_label = ctk.CTkLabel(input_frame, text="Theme:", font=ctk.CTkFont(size=14))
        theme_label.grid(row=0, column=2, padx=(20, 10), pady=15)
        
        self.theme_menu = ctk.CTkOptionMenu(input_frame, values=["Dark", "Light", "System"],
                                            command=ctk.set_appearance_mode)
        self.theme_menu.grid(row=0, column=3, padx=(0, 20), pady=15)

        # --- Results Frame (Scrollable) ---
        scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Calculated Times")
        scrollable_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        scrollable_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # --- Table Headers ---
        headers = ["Note Value", "Delay (ms)", "Frequency (Hz)"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(scrollable_frame, text=header, font=ctk.CTkFont(weight="bold"))
            # --- THIS IS THE CORRECTED LINE ---
            # Using "ew" (east-west) to center horizontally instead of "center".
            header_label.grid(row=0, column=i, padx=5, pady=5, sticky="w" if i==0 else "ew")
        
        # Separator
        separator = ctk.CTkFrame(scrollable_frame, height=2, fg_color="gray50")
        separator.grid(row=1, column=0, columnspan=4, padx=5, pady=(0, 10), sticky="ew")

        # --- Create result rows ---
        for i, (note_name, _) in enumerate(NOTE_VALUES, start=2):
            # Note Name Label
            name_label = ctk.CTkLabel(scrollable_frame, text=note_name, anchor="w")
            name_label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            # Delay (ms) Label
            ms_label = ctk.CTkLabel(scrollable_frame, text="--", anchor="center")
            ms_label.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            
            # Frequency (Hz) Label
            hz_label = ctk.CTkLabel(scrollable_frame, text="--", anchor="center")
            hz_label.grid(row=i, column=2, padx=5, pady=5, sticky="ew")

            # Copy Button
            copy_button = ctk.CTkButton(scrollable_frame, text="Copy", width=60,
                                       command=lambda l=ms_label: self.copy_to_clipboard(l.cget("text")))
            copy_button.grid(row=i, column=3, padx=(5, 10), pady=5)
            
            # Store widgets to update them later
            self.result_widgets.append((name_label, ms_label, hz_label, copy_button))


    def update_calculations(self, event=None):
        """Gets BPM from entry, calculates all values, and updates the UI."""
        try:
            bpm = float(self.bpm_entry.get())
            if bpm <= 0:
                raise ValueError("BPM must be positive")
        except (ValueError, TypeError):
            # If input is not a valid number, clear all results
            for _, ms_label, hz_label, copy_button in self.result_widgets:
                ms_label.configure(text="--")
                hz_label.configure(text="--")
                copy_button.configure(state="disabled")
            return

        # Time for one beat (a quarter note) in milliseconds
        quarter_note_ms = 60000.0 / bpm

        # Update each row in the results table
        for i, (_, multiplier) in enumerate(NOTE_VALUES):
            _, ms_label, hz_label, copy_button = self.result_widgets[i]
            
            delay_ms = quarter_note_ms * multiplier
            
            # Calculate frequency, handle division by zero
            frequency_hz = 1000.0 / delay_ms if delay_ms > 0 else 0
            
            ms_label.configure(text=f"{delay_ms:.2f}")
            hz_label.configure(text=f"{frequency_hz:.2f}")
            copy_button.configure(state="normal")


    def copy_to_clipboard(self, text_to_copy):
        """Copies the given text to the system clipboard."""
        if text_to_copy == "--": return
        
        self.clipboard_clear()
        self.clipboard_append(text_to_copy)
        # Optional: Provide user feedback
        print(f"Copied '{text_to_copy}' to clipboard.")
        
        # Find the button that was clicked to provide visual feedback
        for _, ms_label, _, button in self.result_widgets:
            if ms_label.cget("text") == text_to_copy:
                original_text = button.cget("text")
                original_color = button.cget("fg_color")
                button.configure(text="Copied!", fg_color="green")
                self.after(1500, lambda b=button, t=original_text, c=original_color: b.configure(text=t, fg_color=c))
                break


if __name__ == "__main__":
    app = DelayCalculatorApp()
    app.mainloop()
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageGrab
import pillow_avif
from tkinterdnd2 import DND_FILES, Tk
import io

# --- GUI Application Class ---

class AVIFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live AVIF Converter")
        self.root.minsize(500, 600) # Set a minimum size for the window

        self.input_image_path = None
        self.original_pil_image = None
        self.photo_image = None

        # Debounce job IDs for performance
        self.slider_debounce_id = None
        self.resize_debounce_id = None
        
        # Track last known container size to prevent feedback loops
        self.last_container_size = (0, 0)

        self.setup_ui()
        self.setup_bindings()

    def setup_ui(self):
        # The main layout is now two frames: a top one that expands, and a bottom one that doesn't.
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # This frame will hold the image and expand with the window
        self.preview_frame = tk.Frame(main_frame, bg="lightgrey")
        self.preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.preview_label = tk.Label(
            self.preview_frame, text="Drag & Drop an Image File Here\nor\nUse 'Select Image' Button\nor\nPaste an Image with Ctrl+V",
            bg="lightgrey", font=("Helvetica", 12), wraplength=450, justify="center"
        )
        self.preview_label.pack(expand=True)

        # This frame holds all the controls at the bottom and does not expand vertically
        controls_frame = tk.Frame(main_frame)
        controls_frame.pack(fill="x", padx=10, pady=(0, 10))

        # --- Quality Slider ---
        quality_frame = tk.Frame(controls_frame)
        tk.Label(quality_frame, text="AVIF Quality:", font=("Helvetica", 10)).pack(side="left", padx=(0, 10))
        self.quality_var = tk.IntVar(value=50)
        self.quality_slider = ttk.Scale(
            quality_frame, from_=0, to=100, orient="horizontal", variable=self.quality_var,
            command=self.on_slider_move
        )
        self.quality_slider.pack(side="left", expand=True, fill="x")
        self.quality_label = tk.Label(quality_frame, text="50", font=("Helvetica", 10, "bold"), width=3)
        self.quality_label.pack(side="left")
        quality_frame.pack(fill="x", pady=5)

        # --- Buttons (Restored "Select Image") ---
        button_frame = tk.Frame(controls_frame)
        tk.Button(button_frame, text="Select Image", command=self.select_file).pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(button_frame, text="Save AVIF File", command=self.run_final_save, font=("Helvetica", 10, "bold"), bg="#4CAF50", fg="white").pack(side="left", expand=True, fill="x", padx=5)
        button_frame.pack(fill="x", pady=5)
        
        # --- Status Bar ---
        self.status_var = tk.StringVar(value="Ready. Load an image to begin.")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w", bd=1, padx=5)
        self.status_bar.pack(side="bottom", fill="x")

    def setup_bindings(self):
        # Drag and Drop bindings
        self.preview_frame.drop_target_register(DND_FILES)
        self.preview_label.drop_target_register(DND_FILES)
        self.preview_frame.dnd_bind('<<Drop>>', self.handle_drop)
        self.preview_label.dnd_bind('<<Drop>>', self.handle_drop)

        # Paste binding
        self.root.bind('<Control-v>', self.handle_paste)

        # Window resize binding - only bind to the root window
        self.root.bind('<Configure>', self.on_window_resize)

    # --- Event Handlers with Debouncing ---

    def on_slider_move(self, value):
        self.quality_label.config(text=f"{int(float(value))}")
        if self.slider_debounce_id:
            self.root.after_cancel(self.slider_debounce_id)
        self.slider_debounce_id = self.root.after(250, lambda: self.update_display(force_update=True))

    def on_window_resize(self, event=None):
        # Only respond to root window resize events to prevent feedback loops
        if event and event.widget != self.root:
            return
            
        if self.resize_debounce_id:
            self.root.after_cancel(self.resize_debounce_id)
        self.resize_debounce_id = self.root.after(250, self.update_display)

    # --- Core Display Logic ---

    def update_display(self, force_update=False):
        if not self.original_pil_image:
            return

        # Force update the display to get accurate dimensions
        self.root.update_idletasks()
        
        # Get current container dimensions
        container_w = self.preview_frame.winfo_width()
        container_h = self.preview_frame.winfo_height()
        
        # Don't try to calculate if the window is not drawn yet
        if container_w <= 1 or container_h <= 1:
            return
            
        # Check if container size has actually changed significantly to prevent micro-adjustments
        # Skip this check if force_update is True (e.g., quality slider changes)
        if not force_update:
            size_change_threshold = 5  # pixels
            if (abs(container_w - self.last_container_size[0]) < size_change_threshold and 
                abs(container_h - self.last_container_size[1]) < size_change_threshold and
                self.photo_image is not None):  # Skip if we already have an image displayed
                return
            
        self.last_container_size = (container_w, container_h)

        # 1. Convert to AVIF in-memory to get artifacts
        try:
            quality = self.quality_var.get()
            buffer = io.BytesIO()
            self.original_pil_image.save(buffer, format="AVIF", quality=quality, effort=1) # Fastest effort for UI
            compressed_size_kb = len(buffer.getvalue()) / 1024
            buffer.seek(0)
            avif_decoded_image = Image.open(buffer)
        except Exception as e:
            self.update_status(f"Error during preview conversion: {e}", "red")
            return

        # 2. Calculate the correct display size and scale
        original_w, original_h = avif_decoded_image.size

        # Subtract some padding to ensure image fits comfortably in container
        available_w = container_w - 20  # Leave some margin
        available_h = container_h - 20

        # Calculate scale ratio to fit image inside available space
        w_ratio = available_w / original_w
        h_ratio = available_h / original_h
        scale_ratio = min(w_ratio, h_ratio)

        # If image is smaller than container, display at 100% (unless 100% is still too big)
        if scale_ratio > 1.0:
            scale_ratio = 1.0

        # Ensure minimum size for very small scale ratios
        if scale_ratio < 0.1:
            scale_ratio = 0.1

        display_w = max(1, int(original_w * scale_ratio))
        display_h = max(1, int(original_h * scale_ratio))
        display_percent = int(scale_ratio * 100)

        # 3. Resize and display the image
        try:
            # Use LANCZOS for high-quality resizing
            resized_image = avif_decoded_image.resize((display_w, display_h), Image.Resampling.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(resized_image)
            self.preview_label.config(image=self.photo_image, text="")
            self.preview_label.config(bg=self.preview_frame.cget('bg'))
            self.update_status(f"Previewing at {display_percent}% ({compressed_size_kb:.1f} KB). Quality: {quality}", "green")
        except Exception as e:
            self.update_status(f"Error displaying image: {e}", "red")

    # --- Loading Methods ---

    def load_image_from_path(self, filepath):
        self.input_image_path = filepath
        try:
            self.original_pil_image = Image.open(filepath)
            if self.original_pil_image.mode != "RGB":
                self.original_pil_image = self.original_pil_image.convert("RGB")
            # Reset the container size tracking when loading new image
            self.last_container_size = (0, 0)
            # Trigger the first display update
            self.root.after(100, lambda: self.update_display(force_update=True))  # Small delay to ensure UI is ready
        except Exception as e:
            self.update_status(f"Error loading file: {e}", "red")
            self.original_pil_image = None
            
    def load_image_from_object(self, image_obj):
        self.input_image_path = None # Pasted images have no source path initially
        self.original_pil_image = image_obj
        if self.original_pil_image.mode != "RGB":
            self.original_pil_image = self.original_pil_image.convert("RGB")
        # Reset the container size tracking when loading new image
        self.last_container_size = (0, 0)
        self.root.after(100, lambda: self.update_display(force_update=True))  # Small delay to ensure UI is ready

    def select_file(self):
        filetypes = [("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")]
        filepath = filedialog.askopenfilename(title="Select an Image", filetypes=filetypes)
        if filepath:
            self.load_image_from_path(filepath)

    def handle_drop(self, event):
        filepath = event.data.strip('{}')
        if os.path.isfile(filepath):
            self.load_image_from_path(filepath)

    def handle_paste(self, event=None):
        try:
            image = ImageGrab.grabclipboard()
            if isinstance(image, Image.Image):
                self.load_image_from_object(image)
        except Exception:
            pass

    # --- Final Save ---

    def run_final_save(self):
        if not self.original_pil_image:
            messagebox.showerror("Error", "No image is loaded.")
            return

        # For pasted images, we must ask for a final save location
        save_path = filedialog.asksaveasfilename(
            title="Save AVIF File As...",
            defaultextension=".avif",
            filetypes=[("AVIF Image", "*.avif")]
        )
        if not save_path:
            self.update_status("Save cancelled.", "orange")
            return
            
        try:
            self.update_status("Saving final image...", "blue")
            self.root.update_idletasks()
            # Save the original image with higher effort for better compression
            self.original_pil_image.save(save_path, format="AVIF", quality=self.quality_var.get(), effort=4)
            messagebox.showinfo("Success", f"Image successfully saved as:\n{save_path}")
            self.update_status(f"✅ Final file saved successfully!", "green")
        except Exception as e:
            messagebox.showerror("Conversion Failed", str(e))
            self.update_status(f"❌ Save failed.", "red")
            
    def update_status(self, text, color="black"):
        self.status_var.set(text)
        self.status_bar.config(fg=color)

if __name__ == "__main__":
    root = Tk()
    app = AVIFConverterApp(root)
    root.mainloop()

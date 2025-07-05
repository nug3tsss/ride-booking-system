from customtkinter import *
import threading
import time
import random
from PIL import Image
from setup.env_setup import create_virtualenv, install_requirements

class LoadingScreen(CTk):
    """A loading screen for the Gethub application that simulates setup progress."""

    def __init__(self, on_complete_callback):
        super().__init__()
        self.title("Launching Gethub")
        self.geometry("900x600")
        self.callback = on_complete_callback
        self.configure(fg_color=("#FFFFFF", "#191D1A"))  # Set light and dark mode colors

        # Logo and appearance
        logo_path = (
            "assets/icons/logo-dark--transparent.png"
            if get_appearance_mode().lower() == "dark"
            else "assets/icons/logo-light--transparent.png"
        )
        self.logo_img = CTkImage(
            light_image=Image.open(logo_path),
            dark_image=Image.open(logo_path),
            size=(150, 150)
        )

        # Center frame
        self.center_frame = CTkFrame(self, fg_color="transparent")
        self.center_frame.pack(expand=True)

        CTkLabel(self.center_frame, image=self.logo_img, text="").pack(pady=(0, 10))
        CTkLabel(self.center_frame, text="Gethub", font=("Arial Bold", 32)).pack(pady=(0, 30))

        self.label = CTkLabel(self.center_frame, text="Initializing...")
        self.label.pack(pady=(0, 15))

        # Progress bar + %
        self.progress_frame = CTkFrame(self.center_frame, fg_color="transparent")
        self.progress_frame.pack()

        self.progress = CTkProgressBar(self.progress_frame, width=500)
        self.progress.set(0)
        self.progress.pack(side=LEFT, pady=10)

        self.percent_label = CTkLabel(self.progress_frame, text="0%")
        self.percent_label.pack(side=LEFT, padx=10)

        self.after(100, lambda: threading.Thread(target=self.run_setup).start())

    # This method updates the progress bar smoothly to the target percentage
    def update_progress(self, target_percent, status):
        """Increments the progress bar smoothly up to target_percent."""
        current = int(self.progress.get() * 100)
        while current < target_percent:
            current += random.randint(1, 3)
            current = min(current, target_percent)
            self.progress.set(current / 100)
            self.percent_label.configure(text=f"{current}%")
            self.label.configure(text=status)
            time.sleep(random.uniform(0.05, 0.15))

    # This method runs the setup process in a separate thread
    def run_setup(self):
        try:
            # Phase 1: Fake loading
            self.update_progress(40, "Preparing resources...")

            # Phase 2: Real virtualenv setup
            self.label.configure(text="Creating virtual environment...")
            create_virtualenv()
            self.update_progress(60, "Installing dependencies...")

            install_requirements()
            self.update_progress(80, "Finishing up...")

            # Phase 3: Wrap-up
            self.update_progress(100, "Launching Gethub...")
            time.sleep(0.4)

            self.after(100, self.finish_loading)
        except Exception as e:
            self.label.configure(text=f"Error: {e}")
            print(f"[Loader ERROR] {e}")
            self.progress.set(1)

    # This method is called when the loading is complete
    def finish_loading(self):
        try:
            self.after_cancel_all()
        except:
            pass
        self.withdraw()
        self.update()
        self.destroy()
        self.callback()

    # This method cancels all scheduled 'after' callbacks to prevent memory leaks
    def after_cancel_all(self):
        try:
            for cb_id in self.tk.call('after', 'info'):
                try:
                    self.after_cancel(cb_id)
                except:
                    pass
        except:
            pass

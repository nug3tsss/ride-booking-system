from customtkinter import *
# from database.db_handler import get_connection
# from tkinter import filedialog


class ProfilePage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.pack(fill="both", expand=True)

        # Add content to the profile page
        self.label = CTkLabel(self, text="Welcome to the Profile Page!")
        self.label.pack(pady=20)

        # CTkButton(self, text="Change Profile Picture", command=self.upload_picture).pack(pady=10)

    # def upload_picture(self):
    #     file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")])
    #     if file_path:
    #         conn = get_connection()
    #         conn.execute("UPDATE users SET profile_pic = ? WHERE id = ?", (file_path, self.app.current_user["user_id"]))
    #         conn.commit()
    #         conn.close()
    #         messagebox.showinfo("Success", "Profile picture updated.")
    #         self.app.current_user["profile_pic"] = file_path
    #         self.app.navbar.render_nav()
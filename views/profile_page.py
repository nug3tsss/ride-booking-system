from customtkinter import *
from tkinter import messagebox, filedialog
from database.db_handler import get_connection
from utils.session_manager import save_session
import os
from PIL import Image, ImageDraw, ImageOps

class ProfilePage(CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.user = app.current_user
        c = app.styles.colors
        f = app.styles
        self.new_profile_path = None
        self.reset_picture_flag = False
        self.editing_field_active = False
        self.has_unsaved_changes = False

        self.grid_columnconfigure(0, weight=1)
        CTkLabel(self, text="My Profile", font=f.font_h2).pack(pady=(20, 10))

        self.card = CTkFrame(self, fg_color=c["profile_card"], corner_radius=12)
        self.card.pack(padx=20, pady=10, ipady=50)

        self.card.grid_columnconfigure(0, weight=1)
        self.card.grid_columnconfigure(1, weight=2)
        self.card.grid_columnconfigure(2, weight=1)

        self.create_profile_image_section()
        self.create_field("First Name", "first_name", row=2)
        self.create_field("Last Name", "last_name", row=3)
        self.create_field("Username", "username", row=4)
        self.create_password_button(row=5)

        btn_frame = CTkFrame(self.card, fg_color="transparent")
        btn_frame.grid(row=6, column=0, columnspan=3, pady=(20, 5))

        save_icon = CTkImage(light_image=Image.open("assets/icons/save_icon-dark.png"), dark_image=Image.open("assets/icons/save_icon-dark.png"), size=(16, 16))
        cancel_icon = CTkImage(light_image=Image.open("assets/icons/cancel_icon-dark.png"), dark_image=Image.open("assets/icons/cancel_icon-dark.png"), size=(16, 16))

        self.save_btn = CTkButton(btn_frame, text="Save Changes", fg_color=c["button_disable"], state=DISABLED,
                                  image=save_icon, compound="left", command=self.save_all_changes)
        self.save_btn.pack(side="left", padx=10)

        self.cancel_btn = CTkButton(btn_frame, text="Cancel", fg_color=c["button_disable"], state=DISABLED,
                                    image=cancel_icon, compound="left", command=self.cancel_all_changes)
        self.cancel_btn.pack(side="left", padx=10)

        self.delete_icon = CTkImage(light_image=Image.open("assets/icons/delete_icon-dark.png"), dark_image=Image.open("assets/icons/delete_icon-dark.png"), size=(16, 16))
        CTkButton(self.card, text="Delete Account", fg_color=c["button_danger"], hover_color=c["button_danger_hover"],
                  image=self.delete_icon, compound="left", command=self.confirm_delete
                  ).grid(row=7, column=0, columnspan=3, pady=10)

    def create_profile_image_section(self):
        c = self.app.styles.colors
        self.img_label = CTkLabel(self.card, text="")
        self.img_label.grid(row=0, column=0, columnspan=3, pady=(35, 10))
        self.display_profile_image(self.user.get("profile_pic"))

        btn_frame = CTkFrame(self.card, fg_color="transparent")
        btn_frame.grid(row=1, column=0, columnspan=3, pady=(0, 20))

        change_icon = CTkImage(light_image=Image.open("assets/icons/change_icon-dark.png"), dark_image=Image.open("assets/icons/change_icon-dark.png"), size=(16, 16))
        remove_icon = CTkImage(light_image=Image.open("assets/icons/remove_icon-dark.png"), dark_image=Image.open("assets/icons/remove_icon-dark.png"), size=(16, 16))

        CTkButton(btn_frame, fg_color=c["green"], hover_color=c["green_hover"], text="Change Photo", image=change_icon, compound="left",
                  command=self.change_picture).pack(side="left", padx=5)

        CTkButton(btn_frame, fg_color=c["green"], hover_color=c["green_hover"], text="Remove Photo", image=remove_icon, compound="left",
                  command=self.remove_picture).pack(side="left", padx=5)

    def display_profile_image(self, img_path):
        try:
            target_size = (100, 100)

            image = Image.open(img_path or "assets/user/profile.png").convert("RGBA")

            # Center horizontally, shift up vertically to preserve heads/faces
            image = ImageOps.fit(image, target_size, method=Image.LANCZOS, centering=(0.5, 0.3))

            rounded = Image.new("RGBA", target_size, (0, 0, 0, 0))
            mask = Image.new("L", target_size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, *target_size), radius=20, fill=255)
            rounded.paste(image, (0, 0), mask)

            self.profile_image = CTkImage(light_image=rounded, size=target_size)
            self.img_label.configure(image=self.profile_image, text="")

        except:
            self.img_label.configure(text="[No Image]", image=None)



    def create_field(self, label, attr, row):
        c = self.app.styles.colors
        CTkLabel(self.card, text=f"{label}:", text_color="white", width=90, anchor="e").grid(row=row, column=0, sticky="e", padx=(25, 5), pady=2)

        var = StringVar(value=self.user.get(attr, ""))
        label_widget = CTkLabel(self.card, width=140, text_color="white" ,textvariable=var, anchor="w")
        label_widget.grid(row=row, column=1, padx=(5, 5), sticky="w")

        entry_widget = CTkEntry(self.card)
        entry_widget.insert(0, var.get())
        entry_widget.grid(row=row, column=1, padx=(5, 5), sticky="w")
        entry_widget.grid_remove()

        edit_icon = CTkImage(light_image=Image.open("assets/icons/edit_icon-dark.png"), dark_image=Image.open("assets/icons/edit_icon-dark.png"), size=(16, 16))
        edit_btn = CTkButton(self.card, fg_color=c["green"], hover_color=c["green_hover"], text="Edit", text_color="white", width=80, image=edit_icon, compound="left",
                             command=lambda: self.toggle_field(attr))
        edit_btn.grid(row=row, column=2, padx=(5, 0), sticky="w")

        setattr(self, f"var_{attr}", var)
        setattr(self, f"label_{attr}", label_widget)
        setattr(self, f"entry_{attr}", entry_widget)

    def toggle_field(self, attr):
        c = self.app.styles.colors

        entry = getattr(self, f"entry_{attr}")
        label = getattr(self, f"label_{attr}")
        var = getattr(self, f"var_{attr}")

        self.editing_field_active = True

        label.grid_remove()
        entry.delete(0, END)
        entry.insert(0, var.get())
        entry.grid()
        entry.focus()
        entry.bind("<FocusOut>", lambda e: self.on_focus_out(attr))
        entry.bind("<KeyRelease>", lambda e: self.check_changes())
        self.cancel_btn.configure(state=NORMAL, fg_color=c["green"])

    def on_focus_out(self, attr):
        entry = getattr(self, f"entry_{attr}")
        label = getattr(self, f"label_{attr}")
        var = getattr(self, f"var_{attr}")
        edited = entry.get().strip()
        var.set(edited)
        entry.grid_remove()
        label.grid()

        self.editing_field_active = any(
            getattr(self, f"entry_{a}").winfo_ismapped()
            for a in ["first_name", "last_name", "username"]
        )

        self.check_changes()

    def create_password_button(self, row):
        c = self.app.styles.colors
        CTkLabel(self.card, text="Password:", text_color="white", width=90, anchor="e").grid(row=row, column=0, sticky="e", padx=(0, 5), pady=4)
        CTkLabel(self.card, text="********", text_color="white", anchor="w").grid(row=row, column=1, padx=(5, 5), sticky="w")
        CTkButton(self.card, width=100, fg_color=c["green"], hover_color=c["green_hover"], text="Change", image=CTkImage(light_image=Image.open("assets/icons/password_icon-dark.png"), dark_image=Image.open("assets/icons/password_icon-dark.png"), size=(16, 16)),
                  compound="left", command=self.show_password_popup).grid(row=row, column=2, padx=(5, 50), sticky="w")

    def show_password_popup(self):
        c = self.app.styles.colors
        popup = CTkToplevel(self)
        popup.title("Change Password")
        popup.geometry("300x350")
        popup.grab_set()
        popup.focus_force()
        popup.attributes("-topmost", True)

        CTkLabel(popup, text="Enter Old Password").pack(pady=(20, 5))
        old_pw = CTkEntry(popup, show="*")
        old_pw.pack(pady=5)

        CTkLabel(popup, text="Enter New Password").pack(pady=5)
        new_pw = CTkEntry(popup, show="*")
        new_pw.pack(pady=5)

        CTkLabel(popup, text="Confirm New Password").pack(pady=5)
        confirm_pw = CTkEntry(popup, show="*")
        confirm_pw.pack(pady=5)

        show_pw_var = BooleanVar(value=False)

        def toggle_pw():
            show = "" if show_pw_var.get() else "*"
            old_pw.configure(show=show)
            new_pw.configure(show=show)
            confirm_pw.configure(show=show)

        CTkSwitch(popup, text="Show Password", variable=show_pw_var, command=toggle_pw).pack(pady=5)

        def change_pw():
            old = old_pw.get()
            new = new_pw.get()
            confirm = confirm_pw.get()

            if not old or not new or not confirm:
                messagebox.showerror("Error", "All fields required.", parent=popup)
                return

            if old != self.user.get("password"):
                messagebox.showerror("Error", "Old password is incorrect.", parent=popup)
                return

            if len(new) < 8:
                messagebox.showerror("Error", "New password must be at least 8 characters.", parent=popup)
                return

            if new != confirm:
                messagebox.showerror("Error", "New passwords do not match.", parent=popup)
                return

            conn = get_connection()
            with conn:
                conn.execute("UPDATE users SET password=? WHERE id=?", (new, self.user["user_id"]))
            self.user["password"] = new
            save_session(self.user)
            messagebox.showinfo("Success", "Password updated.", parent=popup)
            popup.destroy()
            self.has_unsaved_changes = True
            self.check_changes()

        CTkButton(popup, fg_color=c["green"], hover_color=c["green_hover"], text="Save Password", command=change_pw).pack(pady=10)

    def remove_picture(self):
        self.new_profile_path = None
        self.reset_picture_flag = True
        self.display_profile_image("assets/user/profile.png")
        self.check_changes()

    def change_picture(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if filepath:
            self.open_crop_popup(filepath)

            # self.new_profile_path = filepath
            # self.reset_picture_flag = False
            # self.display_profile_image(filepath)
            # self.check_changes()

    def open_crop_popup(self, filepath):
        from PIL import ImageTk  # Needed for displaying in Canvas

        popup = CTkToplevel(self)
        popup.title("Crop Photo")
        popup.geometry("400x450")
        popup.grab_set()
        popup.focus_force()

        img = Image.open(filepath)
        original = img.copy()
        img.thumbnail((300, 300))
        tk_img = ImageTk.PhotoImage(img)
        popup.tk_img = tk_img 
        img_width, img_height = tk_img.width(), tk_img.height()
        canvas = CTkCanvas(popup, width=img_width, height=img_height)
        canvas.pack(pady=10)
        canvas_img = canvas.create_image(0, 0, anchor="nw", image=tk_img)

        crop_box = [50, 50, 250, 250]
        rect = canvas.create_rectangle(*crop_box, outline="cyan", width=2)

        def on_drag(event):
            x, y = event.x, event.y
            size = crop_box[2] - crop_box[0]
            # Keep it square and within bounds
            x = max(0, min(x, 300 - size))
            y = max(0, min(y, 300 - size))
            crop_box[0], crop_box[1] = x, y
            crop_box[2], crop_box[3] = x + size, y + size
            canvas.coords(rect, *crop_box)

        canvas.bind("<B1-Motion>", on_drag)

        def apply_crop():
            # Scale crop box back to original image dimensions
            scale_x = original.width / img.width
            scale_y = original.height / img.height
            left = int(crop_box[0] * scale_x)
            upper = int(crop_box[1] * scale_y)
            right = int(crop_box[2] * scale_x)
            lower = int(crop_box[3] * scale_y)
            cropped = original.crop((left, upper, right, lower))
            self.new_profile_path = filepath  # we can replace this with the cropped path if saved
            self.cropped_profile_image = cropped  # keep it for saving
            self.reset_picture_flag = False
            self.display_profile_image_from_object(cropped)
            self.check_changes()
            popup.destroy()

        CTkButton(popup, text="Crop & Use Photo", command=apply_crop).pack(pady=5)
        CTkButton(popup, text="Cancel", command=popup.destroy).pack(pady=5)

    def display_profile_image_from_object(self, pil_image):
        try:
            target_size = (100, 100)
            image = pil_image.convert("RGBA")
            image = ImageOps.fit(image, target_size, method=Image.LANCZOS, centering=(0.5, 0.3))

            rounded = Image.new("RGBA", target_size, (0, 0, 0, 0))
            mask = Image.new("L", target_size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, *target_size), radius=20, fill=255)
            rounded.paste(image, (0, 0), mask)

            self.profile_image = CTkImage(light_image=rounded, size=target_size)
            self.img_label.configure(image=self.profile_image, text="")
        except:
            self.img_label.configure(text="[No Image]", image=None)


    def check_changes(self):
        c = self.app.styles.colors
        changed = False
        for attr in ["first_name", "last_name", "username"]:
            entry = getattr(self, f"entry_{attr}")
            new_val = entry.get().strip()
            if new_val != self.user.get(attr, ""):
                changed = True
                break

        if self.new_profile_path or self.reset_picture_flag:
            changed = True

        self.has_unsaved_changes = changed

        self.save_btn.configure(state=NORMAL if changed else DISABLED,
                                fg_color=c["green"] if changed else c["button_disable"])

        self.cancel_btn.configure(state=NORMAL if changed or self.editing_field_active else DISABLED,
                                  fg_color=c["green"] if changed or self.editing_field_active else c["button_disable"])

    def save_all_changes(self):
        updated_data = {}
        conn = get_connection()
        cur = conn.cursor()

        for attr in ["first_name", "last_name", "username"]:
            entry = getattr(self, f"entry_{attr}")
            new_val = entry.get().strip()
            if not new_val:
                messagebox.showerror("Error", f"{attr.replace('_', ' ').title()} cannot be empty.")
                return
            if attr == "username":
                cur.execute("SELECT id FROM users WHERE username = ? COLLATE BINARY AND id != ?", (new_val, self.user["user_id"]))
                if cur.fetchone():
                    messagebox.showerror("Error", "Username already taken.")
                    return
            if new_val != self.user.get(attr):
                updated_data[attr] = new_val
                self.user[attr] = new_val

        if self.new_profile_path:
            dest_path = os.path.join("assets", "icons", f"user_{self.user['user_id']}_profile.png")
            if hasattr(self, "cropped_profile_image"):
                self.cropped_profile_image.save(dest_path)
            else:
                Image.open(self.new_profile_path).save(dest_path)
            updated_data["profile_pic"] = dest_path
            self.user["profile_pic"] = dest_path
        elif self.reset_picture_flag:
            default_path = os.path.join("assets", "icons", "user", "profile.png")
            updated_data["profile_pic"] = default_path
            self.user["profile_pic"] = default_path

        if updated_data:
            sql = ", ".join(f"{k}=?" for k in updated_data)
            cur.execute(f"UPDATE users SET {sql} WHERE id = ?", list(updated_data.values()) + [self.user["user_id"]])
            conn.commit()
            save_session(self.user)
            self.app.navbar.render_nav()
            messagebox.showinfo("Saved", "Changes have been saved.")

        conn.close()
        self.refresh_labels()

    def refresh_labels(self):
        c = self.app.styles.colors
        for attr in ["first_name", "last_name", "username"]:
            var = getattr(self, f"var_{attr}")
            var.set(self.user.get(attr, ""))
            label = getattr(self, f"label_{attr}")
            entry = getattr(self, f"entry_{attr}")
            entry.grid_remove()
            label.grid()

        self.new_profile_path = None
        self.reset_picture_flag = False
        self.editing_field_active = False
        self.has_unsaved_changes = False

        self.display_profile_image(self.user.get("profile_pic"))
        self.save_btn.configure(state=DISABLED, fg_color=c["button_disable"])
        self.cancel_btn.configure(state=DISABLED, fg_color=c["button_disable"])

    def cancel_all_changes(self):
        self.refresh_labels()

    def confirm_delete(self):
        c = self.app.styles.colors
        confirm = CTkToplevel(self)
        confirm.title("Confirm Delete")
        confirm.geometry("400x140")
        confirm.grab_set()
        confirm.focus_force()
        confirm.attributes("-topmost", True)

        CTkLabel(confirm, text="Are you sure you want to delete your account?", wraplength=340, justify="center").pack(pady=(20, 10))

        btn_frame = CTkFrame(confirm, fg_color="transparent")
        btn_frame.pack(pady=10)

        CTkButton(btn_frame, text="Yes", fg_color=c["button_danger"], hover_color=c["button_danger_hover"],
                  command=lambda: self.delete_account(confirm)).pack(side="left", padx=10)
        CTkButton(btn_frame, text="Cancel", fg_color=c["green"], hover_color=c["green_hover"], command=confirm.destroy).pack(side="left", padx=10)

    def delete_account(self, popup):
        conn = get_connection()
        with conn:
            conn.execute("DELETE FROM users WHERE id = ?", (self.user["user_id"],))
        popup.destroy()
        self.app.logout()
        messagebox.showinfo("Deleted", "Account deleted successfully.")

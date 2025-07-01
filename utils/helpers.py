def create_nav_button(self, text, page, column):
    CTkButton(self, text=text, font=self.styles.nav_font,
              command=lambda: self.app.show_page(page),
              fg_color="transparent", text_color="white",
              hover_color=self.styles.hover_color, corner_radius=0
              ).grid(row=0, column=column, padx=5, sticky="nsew")
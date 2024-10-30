import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry('800x600')
        self.title('Youtube Video/Audio Downloader')
        ctk.set_appearance_mode("light")

    def index(self):
        self.index_page = IndexPage(self)
        self.index_page.pack(fill='both', expand=True, padx=20, pady=20)
        self.index_page.create_page()

class IndexPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

    def create_page(self):
        # page frame
        self.frame_container = ctk.CTkFrame(self)
        self.frame_container.pack(fill='both', expand=True)
        # Widgets
        self.test_label = ctk.CTkLabel(self.frame_container, text='text', font=('times new roman', 30, 'bold'))
        self.test_label.place(relx=0.5, rely=0.5, anchor='center')



if __name__ == '__main__':
    app = App()
    app.index()
    app.mainloop()
import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry('800x600')
        self.title('Youtube Video/Audio Downloader')
        ctk.set_appearance_mode("light")

    def index(self):
        self.index_page = IndexPage(self)
        self.index_page.pack(fill='both', expand=True)
        self.index_page.create_page()

class IndexPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

    def create_page(self):
        # Frame Container
        self.frame_container = ctk.CTkFrame(self, fg_color='#B8B8DC', corner_radius=0, border_color='#B8B8DC')
        self.frame_container.pack(fill='both', expand=True)
        # Widgets
        # Title Label
        self.label_title = ctk.CTkLabel(self.frame_container, text='Youtube Downloader', font=('Times', 20, 'bold'))
        self.label_title.place(relx=0.5, rely=0.05, relwidth=1, relheight=0.1, anchor='center')
        # URL Entry
        self.label_url = ctk.CTkLabel(self.frame_container, text='URL:', font=('Times', 14, 'bold'))
        self.label_url.place(relx=0.1, rely=0.15, relwidth=0.2, relheight=0.06, anchor='center')
        self.entry_url = ctk.CTkEntry(self.frame_container, font=('Times', 14, 'bold'))
        self.entry_url.place(relx=0.4, rely=0.15, relwidth=0.55, relheight=0.06, anchor='center')
        self.button_mp3 = ctk.CTkButton(self.frame_container, text='(.mp3)', font=('Times', 14, 'bold'), command=self.download_mp3)
        self.button_mp3.place(relx=0.75, rely=0.15, relwidth=0.08, relheight=0.06, anchor='center')
        self.button_mp4 = ctk.CTkButton(self.frame_container, text='(.mp4)', font=('Times', 14, 'bold'), command=self.download_mp4)
        self.button_mp4.place(relx=0.85, rely=0.15, relwidth=0.08, relheight=0.06, anchor='center')

    def download_mp3(self):
        self.url = self.entry_url.get()
        print(self.url)

    def download_mp4(self):
        pass



if __name__ == '__main__':
    app = App()
    app.index()
    app.mainloop()
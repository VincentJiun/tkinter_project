import customtkinter as ctk
import threading
from pytubefix import YouTube
import re

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry('1024x600')
        self.title('Youtube Video/Audio Downloader')
        self.resizable(False, False)
        self.iconbitmap('icon.ico')
        ctk.set_appearance_mode("light")

    def index(self):
        self.index_page = IndexPage(self)
        self.index_page.pack(fill='both', expand=True)
        self.index_page.create_page()

class IndexPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.selected_resolution = ctk.StringVar(value="Highest")  # 預設選擇720p

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
        self.button_mp3 = ctk.CTkButton(self.frame_container, text='(.mp3)', font=('Times', 14, 'bold'), command=self.start_download_mp3)
        self.button_mp3.place(relx=0.75, rely=0.15, relwidth=0.08, relheight=0.06, anchor='center')
        self.button_mp4 = ctk.CTkButton(self.frame_container, text='(.mp4)', font=('Times', 14, 'bold'), command=self.start_download_mp4)
        self.button_mp4.place(relx=0.85, rely=0.15, relwidth=0.08, relheight=0.06, anchor='center')
        self.progress_bar = ctk.CTkProgressBar(self.frame_container)
        self.progress_bar.place(relx=0.5, rely=0.35, relwidth=0.3, relheight=0.03, anchor='center')
        self.progress_bar.set(0)
        self.label_percentage = ctk.CTkLabel(self.frame_container, text='', font=('Times', 14, 'bold'))
        self.label_percentage.place(relx=0.7, rely=0.35, relwidth=0.1, relheight=0.06, anchor='center')
        self.label_progress = ctk.CTkLabel(self.frame_container, text='', font=('Times', 14, 'bold'))
        self.label_progress.place(relx=0.5, rely=0.45, relwidth=0.8, relheight=0.06, anchor='center')
        # Resolution Checkboxes
        self.label_resolution = ctk.CTkLabel(self.frame_container, text='畫質:', font=('標楷體', 16, 'bold'))
        self.label_resolution.place(relx=0.2, rely=0.25, relwidth=0.05, relheight=0.06, anchor='center')
        self.video_h = ctk.CTkRadioButton(self.frame_container, text='最高', variable=self.selected_resolution, value="Highest", font=('標楷體', 16, 'bold'), radiobutton_width=16, radiobutton_height=16)
        self.video_h.place(relx=0.3, rely=0.25, relwidth=0.1, relheight=0.06, anchor='center')
        self.video_2160 = ctk.CTkRadioButton(self.frame_container, text='2160p', variable=self.selected_resolution, value="2160p", font=('Time', 16, 'bold'), radiobutton_width=16, radiobutton_height=16)
        self.video_2160.place(relx=0.4, rely=0.25, relwidth=0.1, relheight=0.06, anchor='center')
        self.video_1440 = ctk.CTkRadioButton(self.frame_container, text='1440p', variable=self.selected_resolution, value="1440p", font=('Time', 16, 'bold'), radiobutton_width=16, radiobutton_height=16)
        self.video_1440.place(relx=0.5, rely=0.25, relwidth=0.1, relheight=0.06, anchor='center')
        self.video_1080 = ctk.CTkRadioButton(self.frame_container, text='1080p', variable=self.selected_resolution, value="1080p", font=('Time', 16, 'bold'), radiobutton_width=16, radiobutton_height=16)
        self.video_1080.place(relx=0.6, rely=0.25, relwidth=0.1, relheight=0.06, anchor='center')
        self.video_720 = ctk.CTkRadioButton(self.frame_container, text='720p', variable=self.selected_resolution, value="720p", font=('Time', 16, 'bold'), radiobutton_width=16, radiobutton_height=16)
        self.video_720.place(relx=0.7, rely=0.25, relwidth=0.1, relheight=0.06, anchor='center')
        self.video_360 = ctk.CTkRadioButton(self.frame_container, text='360p', variable=self.selected_resolution, value="360p", font=('Time', 16, 'bold'), radiobutton_width=16, radiobutton_height=16)
        self.video_360.place(relx=0.8, rely=0.25, relwidth=0.1, relheight=0.06, anchor='center')

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        byte_downloaded = total_size-bytes_remaining
        persentage_of_compeletion = byte_downloaded/total_size * 100
        self.label_percentage.configure(text = f'{persentage_of_compeletion:.2f}%')
        self.label_percentage.update()
        # update the progress bar
        self.progress_bar.set(persentage_of_compeletion*0.01)
    
    def start_download_mp3(self):
        # 啟動下載 MP3 的線程
        threading.Thread(target=self.download_mp3, daemon=True).start()
    
    def download_mp3(self):
        self.url = self.entry_url.get()
        try:
            self.yt = YouTube(self.url, on_progress_callback=self.on_progress)
            self.progress_bar.set(0)
            self.label_percentage.configure(text = '0%')
            self.button_mp4.configure(state='disabled')
            self.button_mp3.configure(state='disabled')
            self.yt_title = re.sub(r'[\\/*?:"<>|]', "", self.yt.title)
            self.label_progress.configure(text=f'{self.yt_title}.mp3 下載中...', text_color='black')
            self.yt_streams = self.yt.streams.get_audio_only()
            self.yt_streams.download(output_path='./download/Audio', filename=f'{self.yt_title}.mp3')
            self.label_progress.configure(text='下載完成!', text_color='black')
            self.button_mp4.configure(state='normal')
            self.button_mp3.configure(state='normal')

        except Exception as e:
            self.label_progress.configure(text='請輸入正確的網址...!!!', text_color='red')

    def start_download_mp4(self):
        threading.Thread(target=self.download_mp4, daemon=True).start()

    def download_mp4(self):
        self.url = self.entry_url.get()
        resolution = self.selected_resolution.get()
        try:
            self.yt = YouTube(self.url, on_progress_callback=self.on_progress)
            self.progress_bar.set(0)
            self.label_percentage.configure(text = '0%')
            self.button_mp4.configure(state='disabled')
            self.button_mp3.configure(state='disabled')
            self.yt_title = re.sub(r'[\\/*?:"<>|]', "", self.yt.title)
            if resolution == 'Highest':
                self.label_progress.configure(text=f'{self.yt_title}.mp4 下載中...', text_color='black')
                self.yt_streams = self.yt.streams.get_highest_resolution()
                self.yt_streams.download(output_path='./download/Video', filename=f'{self.yt_title}.mp4')
                self.label_progress.configure(text='下載完成!', text_color='black')
                self.button_mp4.configure(state='normal')
                self.button_mp3.configure(state='normal')
            else:
                self.label_progress.configure(text=f'{self.yt_title}_({resolution}).mp4 下載中...', text_color='black')
                self.yt_streams = self.yt.streams.filter(res=resolution, file_extension='mp4')
                if self.yt_streams != None:
                    self.yt_streams[0].download(output_path='./download/Video', filename=f'{self.yt_title}_({resolution}).mp4')
                    self.label_progress.configure(text='下載完成!', text_color='black')
                    self.button_mp4.configure(state='normal')
                    self.button_mp3.configure(state='normal')
                else:
                    self.label_progress.configure(text='請選擇其他畫質，或最高畫質!', text_color='red')
                    self.button_mp4.configure(state='normal')
                    self.button_mp3.configure(state='normal')

        except Exception as e:
            self.label_progress.configure(text='請輸入正確的網址...!!!', text_color='red')



if __name__ == '__main__':
    app = App()
    app.index()
    app.mainloop()
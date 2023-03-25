import os
from config import Configuration
from printer import Printer

class FolderFiles:
    r_video_path = Configuration.tmdb_video_folder_path
    r_subtitle_path = Configuration.tmdb_subtitle_folder_path
    
    
    def __init__(self) -> None:
        self.printer = Printer()
    
    def ReadVideoFolder(self):
        self.printer.success("Reading Video Folder.")
        path = self.r_video_path
        self.__PathNotFound__(path)
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        return folders

    def ReadEpisodesInVideoFolder(self, tmdb_id):
        self.printer.success("Reading Episode in Video Folder.")
        path = os.path.join(self.r_video_path, tmdb_id)
        self.__PathNotFound__(path)
        all_files = os.listdir(path)

        # Filter the list to include only files (not directories)
        file_list = [f for f in all_files if os.path.isfile(os.path.join(path, f))]
        return file_list
        

    def ReadSubtitleFolder(self, tmdb_id):
        path = os.path.join(self.r_subtitle_path, tmdb_id)
        self.__PathNotFound__(path)
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        return folders
    

    def ReadSubtitleInSubFolder(self, tmdb_id, sub_key, t_id):
        self.printer.success("Reading subtitle Folder.")
        path = os.path.join(self.r_subtitle_path, tmdb_id, sub_key)
        self.__PathNotFound__(path)
        all_files = os.listdir(path)

        # Filter the list to include only files (not directories)
        file_list = [f for f in all_files if os.path.isfile(os.path.join(path, f)) and t_id in f]
        return file_list

    def __PathNotFound__ (self, path):
        if not os.path.exists(path):
            self.printer.danger(f"path not found.")
            self.printer.info(path)
            exit()
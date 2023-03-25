import boto3
import os
from printer import Printer
from config import Configuration
from tqdm.auto import tqdm
import urllib.parse

class MyBucket:
    printer = None
    r_video_path = Configuration.tmdb_video_folder_path
    r_subtitle_path = Configuration.tmdb_subtitle_folder_path

    def __init__(self) -> None:
        self.printer = Printer()    
        self.sub_bucket = boto3.client(
            's3', 
            aws_access_key_id=Configuration.aws_access_key_id, 
            aws_secret_access_key=Configuration.aws_secret_access_key,
            region_name=Configuration.sub_region_name,
            endpoint_url=Configuration.sub_endpoint_url
        )

        self.ep_bucket = boto3.client(
            's3', 
            aws_access_key_id=Configuration.aws_access_key_id, 
            aws_secret_access_key=Configuration.aws_secret_access_key,
            region_name=Configuration.ep_region_name,
            endpoint_url=Configuration.ep_endpoint_url
        )

        self.sub_bucket_name = Configuration.sub_bucket_name
        self.ep_bucket_name = Configuration.ep_bucket_name

    def uploadSubitle(self, e_id, key, tmdb_id, sub_key, file_name, new_name):
        upload_file_path = os.path.join(self.r_subtitle_path, tmdb_id, sub_key, file_name)
        object_name = f'{e_id}/' + new_name  + '.' + file_name.split('.')[-1]

        self.sub_bucket.upload_file(upload_file_path,  self.sub_bucket_name, object_name, ExtraArgs={'ACL': 'public-read'})
        return object_name.split('/', 1)[1]


    def uploadEpisode(self, e_id, key, tmdb_id, file_name, new_name):
        self.printer.info(f'Uploading episde {key}')
        upload_file_path = os.path.join(self.r_video_path, tmdb_id, file_name)
        object_name = f'movie/{e_id}/' + new_name  + '.' + file_name.split('.')[-1]

        # Get the size of the file
        file_size = os.path.getsize(upload_file_path)
    
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="Progress :", bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}') as pbar:
            self.ep_bucket.upload_file(upload_file_path,  self.ep_bucket_name, object_name, Callback=lambda bytes_uploaded: pbar.update(bytes_uploaded), ExtraArgs={'ACL': 'public-read'})
            
        self.printer.subInfo('Uploaded')# f"{file_name} uploaded to {self.ep_bucket_name}/{object_name}")
        return f"{Configuration.ep_endpoint_url}/{self.ep_bucket_name}/{f'movie/{e_id}/' + urllib.parse.quote(new_name  + '.' + file_name.split('.')[-1])}"

    
        
        


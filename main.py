from readFoderFiles import FolderFiles
from printer import Printer
from db import Database
from upload import MyBucket

def main():

    printer = Printer()
    folder_files = FolderFiles()
    myDb = Database()
    bucket = MyBucket()

    printer.success("Starting Script")

    video_folders = folder_files.ReadVideoFolder()
    for video_folder in video_folders:
        if video_folder.isdigit():
            title_name = myDb.getTitle(video_folder)
            if title_name == None:
                    printer.danger(f'title not found.')
                    printer.info(f'tmdb: {video_folder}')
                    exit()

            episode_files = folder_files.ReadEpisodesInVideoFolder(video_folder)
            for expisode in episode_files:
                updates = {'wasabi_url_2':None, 'subtitle_link':[]}
                t_id = expisode.split('.')[0]

                # find episode
                episode_data = myDb.getEpisode(t_id)
                if episode_data == None:
                    printer.danger(f'episode not found.')
                    printer.info(f'id: {t_id}')
                    printer.info(f'tmdb: {video_folder}')
                    exit()

                updates['wasabi_url_2'] = bucket.uploadEpisode(episode_data['_id'], episode_data['key'], video_folder, expisode, f'{title_name} {episode_data["key"]}')

                subtitle_folders = folder_files.ReadSubtitleFolder(video_folder)
                for subtitle_folder in subtitle_folders:
                    sub_key = subtitle_folder
                    subtitles = folder_files.ReadSubtitleInSubFolder(video_folder, sub_key, t_id)
                    printer.info(f'Uploading subtitle {episode_data["key"]}')

                    # print(title_name)
                    # print(episode_data["key"])
                    # print(sub_key)
                    for subtitle in subtitles:
                        new_name = f'{title_name} {episode_data["key"]}-{sub_key}'
                        link = bucket.uploadSubitle(episode_data['_id'], episode_data['key'], video_folder, sub_key, subtitle, new_name)
                        updates['subtitle_link'].append({
                            'file_link': link,
                            'language': sub_key
                        })

                myDb.updateEpisode(episode_data['_id'], updates)
        else:
            continue

if __name__ == "__main__":
    main()
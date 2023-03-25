from config import Configuration
from ssh_pymongo import MongoSession
from bson import ObjectId
from config import Configuration
import os
from printer import Printer

class Database:
    db_client = None
    database = None
    title_collection = None
    episode_details_collection = None
    printer = None
    ssh_key_file=None

    def __init__(self):
        self.ssh_key_file = os.path.join(os.path.dirname(__file__),Configuration.ssh_file_path)
        self.printer = Printer()

    def startDb(self):
        self.db_client = MongoSession(host=Configuration.light_sail_ip, user=Configuration.light_sail_user,key=self.ssh_key_file)
        self.db_client.start()
        self.database = self.db_client.connection[Configuration.db]
        self.title_collection = self.database[Configuration.title_collection]
        self.episode_details_collection = self.database[Configuration.episode_details_collection]
    
    def stopDb(self):
        self.db_client.stop()
    
    def getTitle(self, tmdb_id):
        try:
            self.startDb()
            print('\n')
            self.printer.info(f'Fetching Title : {tmdb_id}')
            pointer = self.title_collection.find({'$and': [
                {'tmdb_show_id': int(tmdb_id)}
            ]}, {
                '_id': 1, 
                'imdb_id': 1, 
                'tmdb_show_id': 1,
                'title_display_name':1
            }).sort([('releaseDate', -1)])
        except Exception as error:
            self.printer.danger('Failed to fetch titles form db')
            print(error)
            exit()
        else:
            data = []

            for x in pointer:
                title = ''
                for i in x['title_display_name']:
                    if i['language'] == 'en':
                        title = i['title']
                
                x['title_display_name'] = title
                data.append(x)
                break
            
            self.stopDb()
            if len(data) == 0:
                return None
            else:
                return data[0]['title_display_name']
            
            
        
    def getEpisode(self, e_id:str):
        try:
            self.startDb()
            self.printer.subInfo(f'Fetching data for Episode: {e_id}')
            pointer = self.episode_details_collection.find({'_id' : ObjectId(e_id)})
        except Exception as error:
            self.printer.danger(f'Failed to fetch episode form db _id {e_id}')
            print(error)
            exit()
        else:
            data = []

            for x in pointer:
                if 'season' not in x or 'episode' not in x:
                    continue

                s_no = str(x['season']).zfill(2)
                e_no = str(x['episode']).zfill(2)

                data.append({'key':f'S{s_no}E{e_no}', "_id":x['_id']})
                break
            
            self.stopDb()
            if len(data) == 0:
                return None
            else:
                return data[0]
    

    def updateIsTaken(self, _id:ObjectId):
        try:
            self.startDb()
            self.title_collection.update_one({'_id': ObjectId(_id)}, {'$set': {'is_taken':1}},  upsert=True)
            self.stopDb()
        except Exception as error:
            self.printer.danger(f'Failed to upate isTaken for document_id {_id}')
            print(error)
            exit()

    def updateEpisode(self, _id:ObjectId, updates):
        try:
            self.startDb()
            self.episode_details_collection.update_one({'_id': ObjectId(_id)}, {'$set': updates},  upsert=True)
            self.stopDb()
        except Exception as error:
            self.printer.danger(f'Failed to upate isTaken for document_id {_id}')
            print(error)
            exit()

import pathlib
import mutagen
import json_utils
from icecream import ic

class MediaData():
    def __init__(self):
        self.db_utils = json_utils.JsonUtils()


    def find_files(self, path):
        #TODO: add a try incase a probule with file
        json_list = list()
        plib = pathlib.Path(path)
        for item in plib.glob('**/*'):
            file_data = self.get_data(item)
            if file_data != None:
                json_list.append(file_data)
        self.db_utils.write_db(json_list)

            
    def get_data(self, filepath):
        song_dict = dict()
        if filepath.is_file():
            data_type = mutagen.File(filepath)
            
            if isinstance(data_type ,mutagen.mp3.MP3):
                tag = data_type.tags
                return self._mp3_file(tag, filepath, song_dict, data_type)

            if isinstance(data_type, mutagen.flac.FLAC):
                tag = data_type.tags
                return self._flac_file(tag,filepath, song_dict, data_type)

        else:
            return None
            
    def _mp3_file(self, tag,filepath, song_dict, data_type):
        # TODO: add try for key value error
        # add to list of missing tags that have not being added

        song_dict["file_path"] = str(filepath) 
        song_dict["file_type"] = "Mp3"
        song_dict["title"] = str(tag["TIT2"])
        song_dict["artist"] = str(tag["TPE1"])
        song_dict["album"] = str(tag["TALB"])
        song_dict["year"] = str(tag["TDRC"])
        song_dict["track_num"] = str(tag["TRCK"])
        song_dict["genres"] = str(tag["TCON"])
        song_dict["length"] = str(data_type.info.length)
                
        if data_type.info.channels == 1:
            song_dict["channels"] = "Mono"
        elif data_type.info.channels == 2:
            song_dict["channels"] = "Stereo"
        else:
            song_dict["channels"] = "Unknow"

        song_dict["bitrate"] = str(data_type.info.bitrate)
        song_dict["sample_rate"] = str(data_type.info.sample_rate)
        song_dict["encoder"] = str(data_type.info.encoder_info)

        return song_dict
        
    def _flac_file(self, tag,filepath, song_dict, data_type):
               # TODO: add try for key value err
               # add to list of missing tags that have not being added

        song_dict["file_path"] = str(filepath)
        song_dict["file_type"] = "Flac"
        song_dict["title"] = str(tag["TITLE"])
        song_dict["artist"] = str(tag["ARTIST"])
        song_dict["album"] = str(tag["ALBUM"])
        song_dict["year"] = str(tag["DATE"])
        song_dict["track_num"] = str(tag["TRACKNUMBER"])
        song_dict["genres"] = "unknow"
        song_dict["length"] = str(data_type.info.length) 

        if data_type.info.channels == 1:
            song_dict["channels"] = "Mono"
        elif data_type.info.channels == 2:
            song_dict["channels"] = "Stereo"
        else:
            song_dict["channels"] = "Unknow"

        song_dict["bitrate"] = str(data_type.info.bitrate)
        song_dict["sample_rate"] = str(data_type.info.sample_rate)
        song_dict["encoder"] = "Flac"

        return song_dict



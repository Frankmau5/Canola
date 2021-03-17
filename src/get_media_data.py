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
        data_type = None
        if filepath.is_file():
            try:
                data_type = mutagen.File(filepath)
            except mutagen.mp3.HeaderNotFoundError as hnf:
                print(filepath)
                print(str(hnf))
            
            if isinstance(data_type ,mutagen.mp3.MP3):
                tag = data_type.tags
                return self._mp3_file(tag, filepath, song_dict, data_type)

            if isinstance(data_type, mutagen.flac.FLAC):
                tag = data_type.tags
                return self._flac_file(tag,filepath, song_dict, data_type)

        else:
            return None
            
    def _mp3_file(self, tag,filepath, song_dict, data_type):
        # TODO: for error add to list of missing tags that have not being added
        try:
            print(filepath)
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
        except KeyError as kerror:
            print(str(filepath))
            print(str(kerror))
        except ValueError as ve:
            print(filepath)
            print(str(ve))
        
    def _flac_file(self, tag,filepath, song_dict, data_type):
               # TODO: add try for key value err
               # add to list of missing tags that have not being added

        song_dict["file_path"] = str(filepath)
        song_dict["file_type"] = "Flac"
        song_dict["title"] = self.clean_flac_tag(str(tag["TITLE"]))
        song_dict["artist"] = self.clean_flac_tag(str(tag["ARTIST"]))
        song_dict["album"] = self.clean_flac_tag(str(tag["ALBUM"]))
        song_dict["year"] = self.clean_flac_tag(str(tag["DATE"]))
        song_dict["track_num"] = self.clean_flac_tag(str(tag["TRACKNUMBER"]))
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

# Helper funcs
# t == Tag

    def clean_flac_tag(self, t):
        return self._remove_quotes(self._remove_brackets(t))

    def _remove_quotes(self, t):
        if t[0] == "'" and t[-1] == "'":
            s = t[:-1]
            s = s[1:]
            return s
        return t

    def _remove_brackets(self,t):
        if t[0] == "[" and t[-1] == "]":
            s = t[:-1]
            s = s[1:]
            return s
        return t

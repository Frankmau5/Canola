"""Media data """
import pathlib
import mutagen
from icecream import ic
import json_utils

class MediaData():
    """MediaData is the main backend obj\n
     """
    def __init__(self):
        self.db_utils = json_utils.JsonUtils()
        self.data_missing = list() # show user @ end of mk_db to let the user choses what to do
        """List of filepaths for files that have missing metadata """
        self.damage_files = list() # ask user if there want to delete files
        """List of filepaths for files that are damage in some way"""
    def find_files(self, path):
        #TODO: add a try incase a probule with file
        """Main method to get metadata from files and write data to json db\n
        Loops thought filesystem starting at path var"""
        json_list = list()
        plib = pathlib.Path(path)
        for item in plib.glob('**/*'):
            file_data = self.get_data(item)
            if file_data is not None:
                json_list.append(file_data)
        self.db_utils.write_db(json_list)

    def get_data(self, filepath):
        """Get metadata from file (e.g media tag and file metadata)\n
        Supported file types: mp3 and flac\n
        returns None (Error happend) or dict"""
        song_dict = dict()
        data_type = None
        if filepath.is_file():
            try:
                data_type = mutagen.File(filepath)
            except mutagen.mp3.HeaderNotFoundError as hnf:
                ic(filepath)
                ic(str(hnf))
                self.damage_files.append(filepath)
            if isinstance(data_type ,mutagen.mp3.MP3):
                tag = data_type.tags
                record = self._mp3_file(tag, filepath, song_dict, data_type)
                if record is not None:
                    return record

            if isinstance(data_type, mutagen.flac.FLAC):
                tag = data_type.tags
                record = self._flac_file(tag,filepath, song_dict, data_type)
                if record is not None:
                    return record
        return None
    def _mp3_file(self, tag, filepath, song_dict, data_type):
        """Inner method gets metedata for mp3 files\n
        return None (Error happened) or dict"""
        try:
            song_dict["file_path"] = str(filepath) 
            song_dict["file_type"] = "Mp3"
            keys = tag.keys()

            if "TIT2" in keys and tag["TIT2"] is not None:
                song_dict["title"] = str(tag["TIT2"])
            else:
                song_dict["title"] = "Unknow"
                self.data_missing.append(filepath) 
                return None
            
            if "TPE1" in keys and tag["TPE1"] is not None:
                song_dict["artist"] = str(tag["TPE1"])
            else:
                song_dict["artist"] = "Unknow"
                self.data_missing.append(filepath)
                return None 

            if "TALB" in keys and tag["TALB"] is not None:
                song_dict["album"] = str(tag["TALB"])
            else:
                song_dict["album"] = "Unknow"
                self.data_missing.append(filepath) 
                return None 
            
            if "TDRC" in keys and tag["TDRC"] is not None:
                song_dict["year"] = str(tag["TDRC"])
            else:
                song_dict["year"] = "Unknow"
            
            if "TRCK" in keys and tag["TRCK"] is not None:
                song_dict["track_num"] = str(tag["TRCK"])
            else:
                song_dict["track_num"] = "Unknow"

            if "TCON" in keys and tag["TCON"] is not None:
                song_dict["genres"] = str(tag["TCON"])
            else:
                song_dict["genres"] = "Unknow"

            song_dict["length"] = str(data_type.info.length)    
            if data_type.info.channels == 1:
                song_dict["channels"] = "Mono"
            elif data_type.info.channels == 2:
                song_dict["channels"] = "Stereo"
            else:
                song_dict["channels"] = "Unknow"

            song_dict["bitrate"] = str(data_type.info.bitrate)
            song_dict["sample_rate"] = str(data_type.info.sample_rate)
            song_dict["filesize"] = str(pathlib.Path(filepath).stat().st_size)

            return song_dict
        except KeyError as kerror:
            ic(str(filepath))
            ic(str(kerror))
            return None
        except ValueError as val_err:
            ic(filepath)
            ic(str(val_err))
            return None
 
    def _flac_file(self, tag,filepath, song_dict, data_type):
               # TODO: add try for KeyError, ValueError errors
        """Inner method gets metedata for mp3 files\n
        return None (Error happened) or dict"""
        keys = tag.keys() 

        song_dict["file_path"] = str(filepath)
        song_dict["file_type"] = "Flac"

        if "TITLE" in keys and tag["TITLE"] is not None:
            song_dict["title"] = clean_flac_tag(str(tag["TITLE"]))
        else:
            self.data_missing.append(filepath) 
            return None 
        
        if "ARTIST" in keys and tag["ARTIST"] is not None:
            song_dict["artist"] = clean_flac_tag(str(tag["ARTIST"]))
        else:
            self.data_missing.append(filepath) 
            return None 
        
        if "ALBUM" in keys and tag["ALBUM"] is not None:
            song_dict["album"] = clean_flac_tag(str(tag["ALBUM"]))
        else:
            self.data_missing.append(filepath) 
            return None 
        
        if "DATE" in keys and tag["DATE"] is not None:
            song_dict["year"] = clean_flac_tag(str(tag["DATE"]))
        else:
            song_dict["year"] = "Unknow" 

        if "TRACKNUMBER" in keys and tag["TRACKNUMBER"] is not None:
            song_dict["track_num"] = clean_flac_tag(str(tag["TRACKNUMBER"]))
        else:
            song_dict["track_num"] = "Unknow" 

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
        song_dict["filesize"] = str(pathlib.Path(filepath).stat().st_size)
        
        return song_dict

def clean_flac_tag(tag):
    """Removes chars from flac tags\n
    Note: This was needed due to flac tag had extra chars (e.g ['NAME'])\n
    Method calls two inner methods. "_remove_quotes" & "_remove_brackets"\n
    returns str"""
    return remove_quotes(remove_brackets(tag))

def remove_quotes(tag):
    """Removes quotes"""
    if tag[0] == "'" and tag[-1] == "'":
        temp = tag[:-1]
        temp = tag[1:]
        return temp
    return tag

def remove_brackets(tag):
    """Remove brackets """
    if tag[0] == "[" and tag[-1] == "]":
        temp = tag[:-1]
        temp = temp[1:]
        return temp
    return tag

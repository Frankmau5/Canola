"""Holds json functions or object """
from platform import system
import pathlib
import simplejson
from icecream import ic

def db_path():
    """function to set path for the canola_db json file for windows or liunx"""
    if system() == "Linux":
        j_file = pathlib.Path("~/.canola_db.json")
        j_file = j_file.expanduser()
        return pathlib.Path(j_file)
    if system() == "Windows":
        j_file = pathlib.Path(pathlib.Path.home()).joinpath("myDocument").joinpath("canola_db.json")
        return j_file
    return None

class JsonUtils():
    """A Class that has methods to interact with json data """

    def __init__(self):
        self.db_filepath = db_path()
        """Var with json file path \n
        type = pathlib.Path"""
        self.json = simplejson
        self.hide_reco_path = pathlib.Path("/home/knrf/.canola_hide.json")

# get_media_data
    def db_exist(self):
        """Method to see if canola_db json file exist\n
        Returns True or False """
        return self.db_filepath.exists()

    def write_db(self, db_dict):
        """Method to turn db (python list or python dict) into a json obj
        and then saves json obj to canola_db json file\n
        """
        data = self.json.dumps(db_dict)
        if not self.db_exist():
            f_open = open(self.db_filepath, mode='x')
            f_open.close()

        with open(self.db_filepath, mode='w') as f_open:
            f_open.write(data)

    def load_json(self):
        """Method to load json data from canola_db json file\n
        Returns an empty list or a list with dict(s) inside"""
        if self.db_exist():
            json_obj = None
            with open(self.db_filepath) as f_open:
                json_obj = self.json.load(f_open)
            return json_obj
        return list()

# recommend
    def load_json_with_fopen(self, f_open):
        return self.json.load(f_open)

    def write_recommened_db(self, path, db_dict):
        reco_path = pathlib.Path(path)
        data = self.json.dumps(db_dict)
        if not reco_path.exists():
            f_open = open(reco_path, mode='x')
            f_open.close()
        with open(reco_path, mode='w') as f_open:
            f_open.write(data)

    def write_hide_reco_db(self, db_dict):
        if self.hide_reco_path.exists():
            with open(self.hide_reco_path) as f_open:
                json = self.load_json_with_fopen(f_open)
                #error here json error with adding list together
                for item in json:
                    db_dict.append(item)
            
            with open(self.hide_reco_path, mode="w") as f_open:
                data = self.json.dumps(db_dict)
                f_open.write(data)
        else:
            data = self.json.dumps(db_dict)
            with open(self.hide_reco_path, mode='w') as f_open:
                f_open.write(data)




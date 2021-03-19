import simplejson
import pathlib
from platform import system
from icecream import ic

class JsonUtils():
    """A Class that has methods to interact with json data """

    def __init__(self):
        self.db_filepath = self._db_path()
        """Var with json file path \n
        type = pathlib.Path"""
        
        self.json = simplejson    

    def _db_path(self):
        """Method to set path for the canola_db json file for windows or liunx"""
        if system() == "Linux":
            p = pathlib.Path("~/.canola_db.json")
            p = p.expanduser()
            return pathlib.Path(p)
        else:
            p = pathlib.Path(pathlib.Path.home()).joinpath("myDocument").joinpath("canola_db.json")
            return p
    
    def db_exist(self):
        """Method to see if canola_db json file exist\n
        Returns True or False """
        return self.db_filepath.exists()

    def write_db(self, db):
        """Method to turn db (python list or python dict) into a json obj and then saves json obj to canola_db json file\n
        """
        data = self.json.dumps(db)
        if self.db_exist() == False:
            f = open(self.db_filepath, mode='x')
            f.close()

        with open(self.db_filepath, mode='w') as f:
            f.write(data)

    def load_json(self):
        """Method to load json data from canola_db json file\n
        Returns an empty list or a list with dict(s) inside"""
        if self.db_exist():
            json_obj = None
            with open(self.db_filepath) as f:
                json_obj = self.json.load(f)
            return json_obj
        else:
            return list()

import simplejson
import pathlib
from platform import system
from icecream import ic

class JsonUtils():
    def __init__(self):
        self.db_filepath = self.db_path()
        self.json = simplejson    

    def db_path(self):
        if system() == "Linux":
            p = pathlib.Path("~/.canola_db.json")
            p = p.expanduser()
            return pathlib.Path(p)
        else:
            p = pathlib.Path(pathlib.Path.home()).joinpath("myDocument").joinpath("canola_db.json")
            return p
    
    def db_exist(self):
        return self.db_filepath.exists()

    def write_db(self, db):
        data = self.json.dumps(db)
        if self.db_exist() == False:
            f = open(self.db_filepath, mode='x')
            f.close()

        with open(self.db_filepath, mode='w') as f:
            f.write(data)

    def load_json(self):
        json_obj = None
        with open(self.db_filepath) as f:
            json_obj = self.json.load(f)
        return json_obj

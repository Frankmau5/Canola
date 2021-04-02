import pathlib

# Error handleing need 
# logginf is needed

class Recommended:
    def __init__(self, db_utils):
        self.json_file_path = "/home/knrf/Documents/music-data/"
        self.db_path = "/home/knrf/.recommended.json"
        self.db_utils = db_utils

    def mk_reco_datebase(self, artist_list):
        # Note need to change this to open a url not a file 
        # when webserver is set up
        reco = list()
        for artist in artist_list:
            path = self.json_file_path + artist + ".json"
            try:
                with open(path) as f_open:
                    json_obj = self.db_utils.load_json_with_fopen(f_open)
                    reco.append(json_obj)
            except Exception as e:
                pass
                #print(str(e))
        self.db_utils.write_recommened_db(self.db_path,reco)

    def load_db(self):
        db_file = pathlib.Path(self.db_path)
        if db_file.exists():
            with open(self.db_path) as f_open:
                return self.db_utils.load_json_with_fopen(f_open)
        else:
            return None
        

    

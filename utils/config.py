import yaml as y

class Config:

    @staticmethod
    def read_config(file): 
        read_file = str(file) #Convert the file path to a string
        with open(read_file, mode='r') as f: #Open the file
            data = y.safe_load(f) #Load the file
        return data #Return the file data

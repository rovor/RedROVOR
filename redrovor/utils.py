import os

def ensure_dir(path):
    #first see if it is exists
    if os.path.exists(path):
        #now if it is a dir return successfully
        if os.path.isdir(path):
            return
        else:
            #a non-directory file, throw an error
            raise ValueError('Path to non-directory')
    else:
        #attempt to create the path
        os.makedirs(path)
        

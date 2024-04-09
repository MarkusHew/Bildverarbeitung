"""
@data:      path_handling.py
@author:    Jannis Mathiuet
@versions:  ver 0.0.0 - 31.03.2024
@desc: 
    file to handle paths, e.g. get current working directory, edit a directory path
    
"""
import os

# =============================================================================
# PUBLIC FUNCTIONS
# =============================================================================
def getAbsDir(**kwargs):
    remove = kwargs.get('remove', None)
    # pathfile = os.path.abspath(__file__)
    path = os.getcwd()
    path = _removePathEndings(path, remove)
    return path

def editDir(path, foldername, **kwargs) :
    remove = kwargs.get('remove', None)
    add = kwargs.get('add', None)

    newpath = _removePathEndings(path, remove)
    if foldername.startswith("\\") is False:
        foldername = "\\" + foldername
    newpath = path + foldername
    return newpath


# =============================================================================
# PRIVATE FUNCTIONS
# =============================================================================
def _removePathEndings(path, cntremove):
    if cntremove is None:
        return path
    try: 
        cntremove = int(cntremove)
    except RuntimeError as error: 
        print(error)
        print("cntremove must be an integer")
    
    if cntremove < 0 :
        raise Exception(f"The number should be higher than 0. ({cntremove=})")
    
    for i in range(cntremove): 
        path, ending = os.path.split(path)
        newpath = path
    #print(newpath)
    
    return newpath

'''
# =============================================================================
# TESTING
# =============================================================================
def main():
    path = getAbsDir(remove=1)
    print(path)
    path = editDir(path, "out",)
    print(path)
    
if __name__ == "__main__" :
    main()
'''
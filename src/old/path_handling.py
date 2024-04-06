"""
@data:      path_handling.py
@author:    Jannis Mathiuet
@versions:  ver 0.0.0 - 31.03.2024 - Jannis Mathiuet
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

def editDir(path, *folders, **kwargs) :
    remove = kwargs.get('remove', None)
    # add = kwargs.get('add', None)

    newpath = _removePathEndings(path, remove)
     
    folderpath = ""
    for folder in folders : 
        folderpath = os.path.join(folderpath, folder)
    newpath = os.path.join(path, folderpath)
    if (os.path.exists(newpath)) is False: 
        print(f"\nThis path does not exist! Try another one. \n{newpath = }\n")
        return ""
    return newpath

def chooseFile(path: str, **kwargs) :
    # kwargs list
    ftype = kwargs.get('ftype', None) # file type
    fname = kwargs.get('fname', None) # file name
    # depth = kwargs.get('depth', 0)
    dircs = kwargs.get('dircs', [""]) 
    
    # select path
    newpath = path
    for dirc in dircs :    
        newpath = os.path.join(newpath, dirc)
    if (os.path.exists(newpath)) is False: 
        print(f"\nThis path does not exist! Try another one. \n{newpath = }\n")
    
    
    d_limiter = 0
    for (root, dirs, files) in os.walk(path):
        if ftype is None : 
            print(f"Directory ({len(dirs)}): {dirs} ")
            print(f"Files     ({len(files)}): {files} ")

        if ftype and fname is type(str): 
            for file in files:
                if (ftype.endswith(file)):
                    if (fname in file):
                        print(file)            
        if d_limiter == 0: 
            break
        d_limiter += 1
            # for f in file:
            #     f.conta
            #     for ftype in f:
            #         for fname in f:
            #         if fname is None: 
            #             print(f)
            #         if k_ele is element: 
            #             filepath = os.path.join(newpath, f)
            #             return filepath
            #         k_ele += 1
    return path
    

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
    # print(newpath)
    
    return newpath


# =============================================================================
# TESTING
# =============================================================================
def main():
    path = getAbsDir(remove=1)
    print(path)
    # path = editDir(path, "out",)
    # print(path)
    chooseFile(path, dircs=["in", "test"])
    
if __name__ == "__main__" :
    main()

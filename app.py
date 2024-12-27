from os import listdir, path, walk
from os.path import isdir
from pathlib import Path
import zipfile

class Finder(object):
    max_depth: int = 4

    @classmethod
    def get_all_projects(cls, path: str, typ: str, depth: int = 0) -> list[tuple]:
        if depth > cls.max_depth:
            return [] #exit early when reached max_depth
        """
        projects tuple scheme: (type: str, path: str, isCompressed: bool)
        """
        projects: list[tuple] = []
        for i in listdir(path): #i is either folder or file
            if isdir(path + "/" + i): #i is folder
                """android studio app detection"""
                if typ == "mobilne" and i == "gradle" :
                    projects.append( ("mobilne", path, False) )
                else: 
                    subprojects = cls.get_all_projects(path + '/' + i, typ, depth + 1)
                    if subprojects:
                        projects.extend(subprojects)
            else: #i is file
                """angular project detection"""
                if typ == "webowe" and i == "angular.json":
                    projects.append( ("angular", path, False) )

                    """wpf app project detection"""
                elif typ == "desktopowe" and i == "MainWindow.xaml":
                    projects.append( ("wpf", path, False) )

        return projects
    
# def zipdir(directory: str, zipname: str):
#     zf = zipfile.ZipFile(zipname, "w")
#     for dirname, subdirs, files in walk(directory):
#         zf.write(dirname)
#         for filename in files:
#             zf.write(path.join(dirname, filename))
#     zf.close()

#https://stackoverflow.com/questions/13118029/deleting-folders-in-python-recursively
def rmdir(dir: str | Path):
    directory = Path(dir)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()

#https://stackoverflow.com/a/1855122
""" turns multiple directories into a zip file and removes them after """
def zipdirs(directories: list[str], zipname: str):
    zf = zipfile.ZipFile(zipname, "w")
    for directory in directories:
        for dirname, subdirs, files in walk(directory):
            zf.write(dirname)
            for filename in files:
                zf.write(path.join(dirname, filename))
    zf.close()
    for directory in directories:
        rmdir(directory)

#https://www.geeksforgeeks.org/working-zip-files-python/
""" extracts the directories where they been from zip file and removes it after """
def unzip(filename: str):
    with zipfile.ZipFile("gex.zip", 'r') as zip: 
        zip.extractall() 

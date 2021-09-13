import shutil
import json
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile 


dict = {}
with open("tileData.json",'r') as tileData:
    
    dict = json.load(tileData)


def formatPath(path):
    """Formats a path gotten from the open_file() function so that it can be used in the importFile() function \n
       Keyword arguments: \n
       path -- the string to be formatted
    """
    temp = str(path)
    temp = temp.replace("<_io.TextIOWrapper name='",'')
    temp = temp.replace("' mode='r' encoding='cp1252'>",'')
    return temp


def importFile(oPath,type):
    """Imports the file from the given path to the given new path \n
        Keyword arguments: \n
        oPath -- original path of the file given as a raw string \n
        nPath -- new path of the file given as a raw string \n
    """
    nPath = f"data/graphics/{type}.png"
    rOPath = r"{}".format(oPath)
    shutil.move(rOPath,nPath)
    return nPath

ws = Tk()
ws.title('PythonGuides')
ws.geometry('400x200') 
Path = "ABC"
def openFile():
    file = askopenfile(mode='r', filetypes=[('Image Files', '*png')])
    if file is not None:
        global Path 
        Path= formatPath(file)





typeLabel = Label(ws,text='new type: ')
typeLabel.grid(row=0)

fileLabel = Label(ws,text="Image file: ")
fileLabel.grid(row=1)

typeEntry = Entry(ws)
typeEntry.grid(row=0,column=1)

fileEntry = Button(
        ws,
        text='file to import',
        command=lambda: openFile())
fileEntry.grid(row=1,column=1)

def save(type,path):
    dict["type"].append(type)
    path = importFile(path,type)
    dict["path"].append(path)
    print(dict)

    with open("tileData.json",'w') as tileData:
        json.dump(dict,tileData)
    ws.quit()


enter = Button(
    ws,
    text="submit",
    command=lambda:save(typeEntry.get(),Path)
)
enter.grid(row=2,)




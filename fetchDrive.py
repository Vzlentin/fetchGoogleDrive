import os, sys, getopt

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
  
def listFolder(parent):
    output=[]
    subfolders = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()

    for sub in subfolders:
        output.append({
            "title":sub["title"], 
            "files":drive.ListFile({'q': "'%s' in parents and trashed=false" % sub["id"]}).GetList()
            })

    return output

def downloadAndStore(input, root):
    for i, subfolder in enumerate(input):
        if os.getcwd() is not root:
            os.chdir(root)
            
        destination = os.path.join(root, subfolder["title"])
        os.mkdir(destination)
        os.chdir(destination)

        print("\n Actually writing in %s" % destination)
        
        for f in subfolder["files"]:
            f.GetContentFile(f["title"])

def usage():
    print("Usage:")
    print("\tfetchDrive.py -i <folder id> [-d <download directory>]")

def main(argv):
    root_directory = os.getcwd()
    parent_id = ''

    try:
        opts, args = getopt.getopt(argv,'i:d:h', ["directory="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == "-i":
            parent_id = a
        elif o == "-d":
            root_directory = a
        elif o == "-h":
            usage()
        else:
            assert False, "unhandled option"

    if parent_id is not '':
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth() 
        drive = GoogleDrive(gauth)

        if not os.path.exists(root_directory):
            os.makedirs(root_directory)

        tree = listFolder(parent_id)
        downloadAndStore(tree, root_directory)

if __name__ == "__main__":
    main(sys.argv[1:])
import tarfile
import os

class TarFile():

    def __init__(self,frompath,topath,logpath="../logs/unzip_logs"):

        self.file = open(logpath, 'a')
        self.frompath=frompath                      # Opening file's path
        self.topath=topath                          # Path to open file
        self.logpath=logpath                        # Log file path
        self.tar = tarfile.open(self.frompath)
        self.tarsize=float(os.path.getsize(frompath)/100.0)


    def info(self,tarmember):

        self.file.write(tarmember.name+"\n")                    # Cikarilan dosyanin isminin log belgesine kayidi

    def extract(self):

        a=os.path.split(self.frompath)                          # Source path spliting
        self.topath=self.topath+"/"+a[1]                        # Destination path + source file's name
        os.mkdir(self.topath)                                   # Make a new dir to destiation path
                                                                # that name is same the source file

        self.file.write(a[1] + " \t\textracted to\t\t " + self.topath + "\n")  # Archive file log
        for member in self.tar.getmembers() :                                  # Arşivdeki her bir dosya için
            self.tar.extract(member,self.topath)                               # belirtilen yere çıkar
            self.info(member)                                                  # loglari kaydet

        self.file.write(100*"-"+"\n\n")





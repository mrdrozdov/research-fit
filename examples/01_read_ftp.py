import ftplib

ftp = ftplib.FTP()
ftp.connect("ftp.ncbi.nlm.nih.gov")
ftp.login()
ftp.cwd('/pubmed/baseline/')
ls = []
ftp.retrlines('MLSD', ls.append)
for entry in ls:
    print(entry)
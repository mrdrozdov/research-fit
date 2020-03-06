import ftplib
import os
import pubmed_parser as pmp
from tqdm import tqdm


url = 'ftp.ncbi.nlm.nih.gov'
dirname = '/pubmed/baseline/'
downloaddir = './data/raw/pubmed_baseline'


def download_file(dl_from, dl_to):
    with open(dl_to, 'wb') as f:
        ftp.retrbinary('RETR {}'.format(dl_from), f.write)


# Login.
ftp = ftplib.FTP()
ftp.connect(url)
ftp.login()
ftp.cwd(dirname)

# Read file data.
entry_lst = []
ftp.retrlines('MLSD', entry_lst.append)

# Download files.
for entry in tqdm(entry_lst):
    parts = entry.split()
    if len(parts) != 2:
        continue
    filename = parts[1]
    if not filename.endswith('.gz'):
        continue
    dl_from = os.path.join(dirname, filename)
    dl_to = os.path.join(downloaddir, filename)
    if os.path.exists(dl_to):
        continue
    download_file(dl_from, dl_to)

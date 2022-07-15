import os
import sys

os.system(f"{sys.executable} -m pip install paramiko")
import paramiko


def upload_file_to_sftp(directory, file_name, content):
    hostname = os.environ["CA_SFTP_SERVER"]
    username = os.environ["CA_SFTP_USER"]
    password = os.environ["CA_SFTP_PASS"]
    transport = paramiko.Transport((hostname, int(22)))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.chdir(directory)
    f = sftp.file(file_name, "w")
    f.write(content)
    f.flush()
    f.close()
    sftp.close()

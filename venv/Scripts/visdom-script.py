#!C:\Users\omnitrix\PycharmProjects\IC_Secu\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'visdom==0.1.8.8','console_scripts','visdom'
__requires__ = 'visdom==0.1.8.8'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('visdom==0.1.8.8', 'console_scripts', 'visdom')()
    )

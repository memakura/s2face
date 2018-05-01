# coding=utf-8

import sys
import json
import os
from cx_Freeze import setup, Executable

# --- for resolving KeyError: 'TCL_LIBRARY' ---
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')
# ------


name = "s2face"
version = "0.2"
description = 'Offline Face Detector'
author = 'Hiroaki Kawashima'
url ='https://github.com/memakura/s2face'

# 変更しない
upgrade_code = '{9D6BDE76-10D7-4123-B444-54252E8F975F}'

# ----------------------------------------------------------------
# セットアップ
# ----------------------------------------------------------------
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "s2face",                    # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]s2face.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     "TARGETDIR",              # WkDir
    )
    ]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}

build_exe_options = {"packages": ['asyncio', 'idna', 'numpy.core.multiarray'],
                    "excludes": [],
                    "includes": [],
                    "include_files": ['images/','00scratch/', 'haarcascades/']
}
#                    "compressed": True
# Add 'idna' package to resolve ImportError: cannot import name 'idnadata'

bdist_msi_options = {'upgrade_code': upgrade_code,
                    'add_to_path': False,
                    'data': msi_data
}

options = {
    'build_exe': build_exe_options,
    'bdist_msi': bdist_msi_options
}

# exeの情報
base = None #'Win32GUI' if sys.platform == 'win32' else None
icon = 'images/icon_256x256.ico'

# exe にしたい python ファイルを指定
exe = Executable(script='s2face.py',
                 targetName='s2face.exe',
                 base=base,
                 icon=icon
                 )
#                 copyDependentFiles = True

# セットアップ
setup(name=name,
      version=version,
      author=author,
      url=url,
      description=description,
      options=options,
      executables=[exe]
      )

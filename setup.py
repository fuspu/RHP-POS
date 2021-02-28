#!/usr/bin/env python

import os, sys

# Path to be created
Report_Paths = ['./Docs','./Docs/Closings','./Docs/Statements','./Docs/Inventory','./Docs/Reports']

for path in Report_Paths:
    if not os.path.isdir(path):
        os.mkdir( path, 0o750 )
        if os.path.isdir(path):
            print("Path '{}' is created".format(path))
        else:
            print('Something goes Wrong')
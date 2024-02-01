"""Test configuration for lib files. Appends {cwd}/lib to system path."""

import os
import sys

# Hacking ./lib into the path
sys.path.insert(0, os.path.join(os.getcwd(), "lib"))

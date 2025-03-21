#!/usr/bin/env python3
"""
Convenience script to check architecture violations.
"""

import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.clean_arch.checker import main

if __name__ == "__main__":
    sys.exit(main()) 
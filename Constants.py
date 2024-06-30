"""
Configuration Module for the application
"""

VHDL_CONFIG_NAME = "config"
VHDL_CONFIG_FILE_NAME = "config"
VHDL_BUILD_DIR = "Dir"

VHDL_LIBRARY_NAME = "work"
VHDL_LIBRARIES = """
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
-- use IEEE.fixed_pkg.all;
"""

VHDL_LIBRARY_DECLARATION = f"""
library work;       -- Default package name
use {VHDL_LIBRARY_NAME}.{VHDL_CONFIG_FILE_NAME}.all;
"""
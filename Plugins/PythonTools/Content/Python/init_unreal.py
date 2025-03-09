"""
Initialization script for Unreal Engine Python.
This script is automatically executed when the Python plugin is loaded.
"""

import unreal
import os
import sys

def setup_python_paths():
    """
    Set up additional Python paths for the Unreal Engine Python environment.
    """
    # Get the current project's Content/Python directory
    project_content_dir = unreal.Paths.project_content_dir()
    project_python_dir = os.path.join(project_content_dir, "Python")
    
    # Add the project's Python directory to sys.path if it exists
    if os.path.exists(project_python_dir) and project_python_dir not in sys.path:
        sys.path.append(project_python_dir)
        unreal.log(f"Added project Python path: {project_python_dir}")
    
    # Get the plugin's Python directory
    plugins_dir = unreal.Paths.project_plugins_dir()
    python_tools_dir = os.path.join(plugins_dir, "PythonTools", "Content", "Python")
    
    # Add the plugin's Python directory to sys.path if it exists
    if os.path.exists(python_tools_dir) and python_tools_dir not in sys.path:
        sys.path.append(python_tools_dir)
        unreal.log(f"Added plugin Python path: {python_tools_dir}")

def register_editor_commands():
    """
    Register Python commands in the Unreal Editor.
    """
    # This will be expanded in the future
    pass

def initialize():
    """
    Main initialization function.
    """
    unreal.log("Initializing Python Tools...")
    setup_python_paths()
    register_editor_commands()
    unreal.log("Python Tools initialized successfully!")

# Run initialization
initialize() 
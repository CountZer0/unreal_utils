"""
Startup script for Python Tools in Unreal Engine 5.5.
This script is automatically executed when the editor starts.
"""

import unreal
import os
import sys
import importlib

def setup_python_paths():
    """
    Set up Python paths for the project.
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
    
    # Add the Snippets directory to sys.path
    snippets_dir = os.path.join(unreal.Paths.project_dir(), "Snippets")
    if os.path.exists(snippets_dir) and snippets_dir not in sys.path:
        sys.path.append(snippets_dir)
        unreal.log(f"Added Snippets path: {snippets_dir}")

def register_menu_commands():
    """
    Register Python commands in the editor menus.
    """
    try:
        # Import the editor automation module
        from Snippets.Python import editor_automation
        
        # Define some example commands
        def list_static_meshes():
            from Snippets.Python import asset_management
            static_meshes = asset_management.find_assets_by_class('StaticMesh')
            unreal.log(f"Found {len(static_meshes)} static meshes in the project")
            
            # Show a notification
            unreal.EditorNotification.show_notification(
                unreal.Text(f"Found {len(static_meshes)} static meshes"),
                unreal.EditorNotificationDuration.SHORT
            )
        
        def create_actor_grid():
            from Snippets.Python import level_design
            cubes = level_design.create_grid_of_actors(unreal.StaticMeshActor, 5, 5)
            unreal.log(f"Created a grid of {len(cubes)} actors")
            
            # Show a notification
            unreal.EditorNotification.show_notification(
                unreal.Text(f"Created a grid of {len(cubes)} actors"),
                unreal.EditorNotificationDuration.SHORT
            )
        
        # Register the commands
        editor_automation.register_editor_command("ListStaticMeshes", list_static_meshes, "List all static meshes in the project")
        editor_automation.register_editor_command("CreateActorGrid", create_actor_grid, "Create a 5x5 grid of actors")
        
        # Create menu entries
        editor_automation.create_menu_entry("LevelEditor.MainMenu.Window", "List Static Meshes", list_static_meshes)
        editor_automation.create_menu_entry("LevelEditor.MainMenu.Window", "Create Actor Grid", create_actor_grid)
        
        unreal.log("Registered Python menu commands")
    except Exception as e:
        unreal.log_error(f"Failed to register menu commands: {e}")

def initialize():
    """
    Main initialization function.
    """
    try:
        unreal.log("Initializing Python Tools...")
        
        # Set up Python paths
        setup_python_paths()
        
        # Register menu commands
        register_menu_commands()
        
        unreal.log("Python Tools initialized successfully!")
    except Exception as e:
        unreal.log_error(f"Failed to initialize Python Tools: {e}")

# Run initialization
initialize() 
"""
Editor Automation Utilities for Unreal Engine 5.5

This module provides functions for automating tasks in the Unreal Editor.
"""

import unreal
import os
import sys
import time

def create_editor_utility_widget(widget_name, parent_class=None, destination_path='/Game/EditorUtilities'):
    """
    Create a new Editor Utility Widget.
    
    Args:
        widget_name (str): Name of the widget to create
        parent_class (object): Optional parent class for the widget
        destination_path (str): Path where the widget should be created
        
    Returns:
        object: The created widget blueprint
    """
    # Get the asset tools
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    # Set the parent class for the widget
    if parent_class is None:
        parent_class = unreal.EditorUtilityWidget
    
    # Create the widget blueprint
    widget_factory = unreal.EditorUtilityWidgetBlueprintFactory()
    widget_factory.parent_class = parent_class
    
    # Create the asset
    widget_asset = asset_tools.create_asset(widget_name, destination_path, None, widget_factory)
    
    return widget_asset

def create_editor_utility_blueprint(blueprint_name, destination_path='/Game/EditorUtilities'):
    """
    Create a new Editor Utility Blueprint.
    
    Args:
        blueprint_name (str): Name of the blueprint to create
        destination_path (str): Path where the blueprint should be created
        
    Returns:
        object: The created blueprint
    """
    # Get the asset tools
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    # Create the blueprint
    blueprint_factory = unreal.EditorUtilityBlueprintFactory()
    blueprint_factory.parent_class = unreal.EditorUtilityBlueprint
    
    # Create the asset
    blueprint_asset = asset_tools.create_asset(blueprint_name, destination_path, None, blueprint_factory)
    
    return blueprint_asset

def register_editor_command(command_name, python_callable, description=""):
    """
    Register a Python function as an editor command.
    
    Args:
        command_name (str): Name of the command
        python_callable (callable): Python function to call when the command is executed
        description (str): Description of the command
        
    Returns:
        bool: True if the command was registered successfully
    """
    try:
        # Get the editor subsystem
        editor_subsystem = unreal.get_editor_subsystem(unreal.EditorScriptingUtilities)
        
        # Register the command
        editor_subsystem.register_python_command(
            command_name,
            python_callable,
            description
        )
        
        return True
    except Exception as e:
        unreal.log_error(f"Failed to register editor command: {e}")
        return False

def batch_rename_selected_actors(search_string, replace_string):
    """
    Rename all selected actors in the level editor.
    
    Args:
        search_string (str): String to search for in actor names
        replace_string (str): String to replace with
        
    Returns:
        int: Number of actors renamed
    """
    # Get the editor subsystem
    editor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    
    # Get selected actors
    selected_actors = editor_subsystem.get_selected_level_actors()
    
    renamed_count = 0
    
    for actor in selected_actors:
        actor_name = actor.get_actor_label()
        
        # Check if the actor name contains the search string
        if search_string in actor_name:
            new_name = actor_name.replace(search_string, replace_string)
            
            # Rename the actor
            actor.set_actor_label(new_name)
            renamed_count += 1
    
    return renamed_count

def take_editor_screenshot(filename, resolution_x=1920, resolution_y=1080):
    """
    Take a screenshot of the current editor viewport.
    
    Args:
        filename (str): Path to save the screenshot
        resolution_x (int): Width of the screenshot
        resolution_y (int): Height of the screenshot
        
    Returns:
        bool: True if the screenshot was taken successfully
    """
    try:
        # Get the editor subsystem
        editor_subsystem = unreal.get_editor_subsystem(unreal.EditorLevelLibrary)
        
        # Take the screenshot
        editor_subsystem.take_high_resolution_screenshot(
            resolution_x,
            resolution_y,
            filename
        )
        
        return True
    except Exception as e:
        unreal.log_error(f"Failed to take screenshot: {e}")
        return False

def build_lighting():
    """
    Build lighting for the current level.
    
    Returns:
        bool: True if lighting was built successfully
    """
    try:
        # Get the editor subsystem
        editor_subsystem = unreal.get_editor_subsystem(unreal.EditorLevelLibrary)
        
        # Build lighting
        editor_subsystem.build_lighting()
        
        return True
    except Exception as e:
        unreal.log_error(f"Failed to build lighting: {e}")
        return False

def create_menu_entry(menu_name, entry_name, python_callable):
    """
    Create a menu entry in the editor.
    
    Args:
        menu_name (str): Name of the menu to add the entry to
        entry_name (str): Name of the menu entry
        python_callable (callable): Python function to call when the menu entry is clicked
        
    Returns:
        bool: True if the menu entry was created successfully
    """
    try:
        # Get the tool menus
        tool_menus = unreal.ToolMenus.get()
        
        # Find the menu
        menu = tool_menus.find_menu(menu_name)
        if not menu:
            unreal.log_error(f"Menu not found: {menu_name}")
            return False
        
        # Create a section if it doesn't exist
        section_name = "PythonTools"
        section = menu.find_section(section_name)
        if not section:
            menu.add_section(section_name, unreal.Text("Python Tools"))
        
        # Create the menu entry
        entry = unreal.ToolMenuEntry(
            name=entry_name,
            type=unreal.MultiBlockType.TOOL_BAR_BUTTON,
            label=unreal.Text(entry_name),
            tooltip=unreal.Text(f"Execute {entry_name}"),
            command=unreal.ToolMenuStringCommand(
                type=unreal.ToolMenuStringCommandType.PYTHON,
                custom_type="PythonCommand",
                string=f"import unreal; {python_callable.__module__}.{python_callable.__name__}()"
            )
        )
        
        # Add the entry to the menu
        menu.add_menu_entry(section_name, entry)
        
        # Refresh the menus
        tool_menus.refresh_all_widgets()
        
        return True
    except Exception as e:
        unreal.log_error(f"Failed to create menu entry: {e}")
        return False

def run_automated_tests(test_names=None, timeout_seconds=300):
    """
    Run automated tests in the editor.
    
    Args:
        test_names (list): List of test names to run, or None to run all tests
        timeout_seconds (int): Timeout in seconds
        
    Returns:
        bool: True if all tests passed
    """
    try:
        # Get the automation controller
        automation = unreal.AutomationBlueprintLibrary.get_automation_controller()
        
        # Run the tests
        if test_names:
            for test_name in test_names:
                automation.run_tests(test_name)
        else:
            automation.run_all_tests()
        
        # Wait for tests to complete
        start_time = time.time()
        while automation.is_running_tests():
            time.sleep(0.1)
            if time.time() - start_time > timeout_seconds:
                unreal.log_error("Test timeout exceeded")
                return False
        
        # Check if all tests passed
        return automation.did_all_tests_pass()
    except Exception as e:
        unreal.log_error(f"Failed to run automated tests: {e}")
        return False

# Example usage
if __name__ == "__main__":
    # Register a simple editor command
    def hello_world():
        unreal.log("Hello from Python!")
    
    register_editor_command("HelloWorld", hello_world, "Print a hello message")
    
    # Create a menu entry
    create_menu_entry("LevelEditor.MainMenu.Window", "Hello World", hello_world) 
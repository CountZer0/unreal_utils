# Python in Unreal Engine 5.5

This guide explains how to set up and use Python scripting in Unreal Engine 5.5 with the PythonTools plugin.

## Table of Contents

- [Setup](#setup)
- [Plugin Structure](#plugin-structure)
- [Running Python Scripts](#running-python-scripts)
- [Example Scripts](#example-scripts)
- [Troubleshooting](#troubleshooting)

## Setup

### 1. Enable the Python Plugin

1. Open your Unreal Engine project
2. Go to **Edit > Plugins**
3. Search for "Python"
4. Enable the **Python Editor Script Plugin**
5. Restart the editor

### 2. Install the PythonTools Plugin

1. Copy the `PythonTools` folder from this repository's `Plugins` directory to your project's `Plugins` directory
2. Restart the editor
3. Go to **Edit > Plugins**
4. Search for "Python Tools"
5. Ensure the plugin is enabled

### 3. Create Python Directories

Create the following directories in your project:

- `/Content/Python` - For project-specific Python scripts
- `/Content/Python/startup` - For scripts that should run when the editor starts

## Plugin Structure

The PythonTools plugin consists of:

- **C++ Module** - Provides integration with Unreal Engine
- **Python Scripts** - Example scripts and utilities
- **Editor UI** - Menu entries and buttons for running Python commands

## Running Python Scripts

There are several ways to run Python scripts in Unreal Engine:

### 1. Python Console

1. Go to **Window > Developer Tools > Python Console**
2. Type your Python code directly or use `execfile()` to run a script file

```python
import unreal
unreal.log("Hello from Python!")

# Run a script file
execfile("/Path/To/Your/Script.py")
```

### 2. Editor Buttons

The PythonTools plugin adds a button to the toolbar that runs a sample Python script.

### 3. Startup Scripts

Scripts placed in the `/Content/Python/startup` directory will be executed automatically when the editor starts.

### 4. Command Line

You can run Python scripts from the command line:

```
UE5Editor.exe YourProject.uproject -ExecutePythonScript="C:/Path/To/Your/Script.py"
```

## Example Scripts

The repository includes several example scripts:

### Asset Management

```python
# Import the module
from Snippets.Python import asset_management

# List all static meshes in the project
static_meshes = asset_management.find_assets_by_class('StaticMesh')
unreal.log(f"Found {len(static_meshes)} static meshes")

# Find unused assets
unused = asset_management.find_unused_assets('/Game/MyFolder')
```

### Editor Automation

```python
# Import the module
from Snippets.Python import editor_automation

# Register a simple command
def hello_world():
    unreal.log("Hello from Python!")

editor_automation.register_editor_command("HelloWorld", hello_world, "Print a hello message")

# Create a menu entry
editor_automation.create_menu_entry("LevelEditor.MainMenu.Window", "Hello World", hello_world)
```

### Level Design

```python
# Import the module
from Snippets.Python import level_design

# Create a grid of actors
cubes = level_design.create_grid_of_actors(unreal.StaticMeshActor, 5, 5)

# Create a circle of actors
spheres = level_design.create_circle_of_actors(unreal.StaticMeshActor, 12, 500)
```

## Troubleshooting

### Python Plugin Not Working

1. Ensure the Python Editor Script Plugin is enabled
2. Check the Output Log for any Python-related errors
3. Verify that the correct Python version is installed (UE5.5 uses Python 3.9)

### Scripts Not Found

1. Check that your Python paths are set up correctly
2. The PythonTools plugin automatically adds these paths:
   - `/YourProject/Content/Python`
   - `/YourProject/Plugins/PythonTools/Content/Python`

### Import Errors

1. Make sure the module you're trying to import is in one of the Python paths
2. Check for any syntax errors in your Python files
3. Verify that any required Unreal Engine modules are loaded

### Editor Crashes

1. Check the crash logs for Python-related errors
2. Ensure you're not accessing invalid objects or memory
3. Add try/except blocks to catch exceptions in your code

## Resources

- [Unreal Engine Python API Documentation](https://docs.unrealengine.com/5.5/en-US/PythonAPI/)
- [Python in Unreal Engine](https://docs.unrealengine.com/5.5/en-US/scripting-the-unreal-editor-using-python/)
- [Unreal Engine Python GitHub Repository](https://github.com/EpicGames/UnrealEngine/tree/master/Engine/Plugins/Experimental/PythonScriptPlugin) 
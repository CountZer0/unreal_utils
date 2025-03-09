"""
Asset Management Utilities for Unreal Engine 5.5

This module provides functions for managing assets in Unreal Engine projects.
"""

import unreal
import os

def list_assets(directory_path, recursive=True, include_only_on_disk=False):
    """
    List all assets in a specified directory.
    
    Args:
        directory_path (str): Path to the directory to search, e.g., '/Game/MyFolder'
        recursive (bool): Whether to search subdirectories
        include_only_on_disk (bool): Whether to include only assets that exist on disk
        
    Returns:
        list: List of asset data objects
    """
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    
    # Create a filter for the asset registry
    ar_filter = unreal.ARFilter(
        class_names=['Object'],
        package_paths=[directory_path],
        recursive_paths=recursive,
        include_only_on_disk_assets=include_only_on_disk
    )
    
    # Get all assets that match the filter
    assets = asset_registry.get_assets(ar_filter)
    
    return assets

def find_assets_by_class(asset_class, directory_path='/Game', recursive=True):
    """
    Find all assets of a specific class.
    
    Args:
        asset_class (str): Class name to search for, e.g., 'StaticMesh', 'Material'
        directory_path (str): Path to search in
        recursive (bool): Whether to search subdirectories
        
    Returns:
        list: List of asset data objects
    """
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    
    # Create a filter for the asset registry
    ar_filter = unreal.ARFilter(
        class_names=[asset_class],
        package_paths=[directory_path],
        recursive_paths=recursive
    )
    
    # Get all assets that match the filter
    assets = asset_registry.get_assets(ar_filter)
    
    return assets

def find_unused_assets(directory_path='/Game', recursive=True):
    """
    Find all unused assets in a directory.
    
    Args:
        directory_path (str): Path to search in
        recursive (bool): Whether to search subdirectories
        
    Returns:
        list: List of unused asset data objects
    """
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    
    # Get all assets in the directory
    ar_filter = unreal.ARFilter(
        package_paths=[directory_path],
        recursive_paths=recursive
    )
    
    assets = asset_registry.get_assets(ar_filter)
    unused_assets = []
    
    # Check each asset for references
    for asset in assets:
        # Get dependencies (assets that this asset depends on)
        dependencies = asset_registry.get_dependencies(asset.package_name)
        
        # Get referencers (assets that depend on this asset)
        referencers = asset_registry.get_referencers(asset.package_name)
        
        # If no other assets reference this asset, it's unused
        if len(referencers) == 0:
            unused_assets.append(asset)
    
    return unused_assets

def duplicate_asset(source_asset_path, destination_path, destination_name):
    """
    Duplicate an asset to a new location.
    
    Args:
        source_asset_path (str): Path to the source asset, e.g., '/Game/MyFolder/MyAsset'
        destination_path (str): Path to the destination directory, e.g., '/Game/MyFolder/Subfolder'
        destination_name (str): Name for the duplicated asset
        
    Returns:
        object: The duplicated asset object
    """
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    # Load the source asset
    source_asset = unreal.load_asset(source_asset_path)
    if not source_asset:
        unreal.log_error(f"Failed to load source asset: {source_asset_path}")
        return None
    
    # Duplicate the asset
    duplicated_asset = asset_tools.duplicate_asset(
        destination_name,
        destination_path,
        source_asset
    )
    
    return duplicated_asset

def bulk_rename_assets(directory_path, search_string, replace_string, recursive=True):
    """
    Rename multiple assets by replacing a string in their names.
    
    Args:
        directory_path (str): Path to the directory containing assets to rename
        search_string (str): String to search for in asset names
        replace_string (str): String to replace with
        recursive (bool): Whether to search subdirectories
        
    Returns:
        int: Number of assets renamed
    """
    # Get all assets in the directory
    assets = list_assets(directory_path, recursive)
    
    renamed_count = 0
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    for asset in assets:
        asset_name = asset.asset_name
        
        # Check if the asset name contains the search string
        if search_string in asset_name:
            new_name = asset_name.replace(search_string, replace_string)
            
            # Rename the asset
            package_path = asset.package_path
            package_name = asset.package_name
            object_path = f"{package_path}/{asset_name}"
            
            # Load the asset
            loaded_asset = unreal.load_asset(object_path)
            if loaded_asset:
                # Rename the asset
                asset_tools.rename_asset(loaded_asset, f"{package_path}/{new_name}")
                renamed_count += 1
    
    return renamed_count

def import_asset(filename, destination_path):
    """
    Import an asset from disk into the project.
    
    Args:
        filename (str): Path to the file on disk
        destination_path (str): Path in the content browser to import to
        
    Returns:
        list: Imported asset objects
    """
    if not os.path.exists(filename):
        unreal.log_error(f"File does not exist: {filename}")
        return []
    
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    # Create import task
    task = unreal.AssetImportTask()
    task.filename = filename
    task.destination_path = destination_path
    task.replace_existing = True
    task.automated = True
    task.save = True
    
    # Execute the import task
    asset_tools.import_asset_tasks([task])
    
    return task.imported_object_paths

# Example usage
if __name__ == "__main__":
    # List all static meshes in the project
    static_meshes = find_assets_by_class('StaticMesh')
    unreal.log(f"Found {len(static_meshes)} static meshes in the project")
    
    # Find unused assets in a specific folder
    unused = find_unused_assets('/Game/MyFolder')
    unreal.log(f"Found {len(unused)} unused assets in /Game/MyFolder") 
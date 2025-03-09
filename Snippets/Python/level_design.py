"""
Level Design Utilities for Unreal Engine 5.5

This module provides functions for automating level design tasks in Unreal Engine.
"""

import unreal
import math
import random

def spawn_actor(actor_class, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
    """
    Spawn an actor in the current level.
    
    Args:
        actor_class (class): Class of the actor to spawn
        location (tuple): Location to spawn the actor at (X, Y, Z)
        rotation (tuple): Rotation of the actor (Pitch, Yaw, Roll)
        scale (tuple): Scale of the actor (X, Y, Z)
        
    Returns:
        object: The spawned actor
    """
    # Get the editor subsystem
    editor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    
    # Convert location, rotation, and scale to Unreal types
    location = unreal.Vector(location[0], location[1], location[2])
    rotation = unreal.Rotator(rotation[0], rotation[1], rotation[2])
    scale = unreal.Vector(scale[0], scale[1], scale[2])
    
    # Create a transform
    transform = unreal.Transform(location, rotation, scale)
    
    # Spawn the actor
    actor = editor_subsystem.spawn_actor_from_class(actor_class, location, rotation)
    
    # Set the actor's scale
    if actor:
        actor.set_actor_scale3d(scale)
    
    return actor

def spawn_static_mesh(static_mesh_path, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
    """
    Spawn a static mesh actor in the current level.
    
    Args:
        static_mesh_path (str): Path to the static mesh asset
        location (tuple): Location to spawn the actor at (X, Y, Z)
        rotation (tuple): Rotation of the actor (Pitch, Yaw, Roll)
        scale (tuple): Scale of the actor (X, Y, Z)
        
    Returns:
        object: The spawned static mesh actor
    """
    # Load the static mesh asset
    static_mesh = unreal.load_asset(static_mesh_path)
    if not static_mesh:
        unreal.log_error(f"Failed to load static mesh: {static_mesh_path}")
        return None
    
    # Spawn a static mesh actor
    actor = spawn_actor(unreal.StaticMeshActor, location, rotation, scale)
    
    # Set the static mesh
    if actor:
        actor.static_mesh_component.set_static_mesh(static_mesh)
    
    return actor

def create_grid_of_actors(actor_class, rows, columns, spacing_x=100, spacing_y=100, start_location=(0, 0, 0)):
    """
    Create a grid of actors in the current level.
    
    Args:
        actor_class (class): Class of the actor to spawn
        rows (int): Number of rows in the grid
        columns (int): Number of columns in the grid
        spacing_x (float): Spacing between actors in the X direction
        spacing_y (float): Spacing between actors in the Y direction
        start_location (tuple): Starting location for the grid (X, Y, Z)
        
    Returns:
        list: List of spawned actors
    """
    actors = []
    
    for row in range(rows):
        for col in range(columns):
            # Calculate the location for this actor
            x = start_location[0] + col * spacing_x
            y = start_location[1] + row * spacing_y
            z = start_location[2]
            
            # Spawn the actor
            actor = spawn_actor(actor_class, (x, y, z))
            
            if actor:
                actors.append(actor)
    
    return actors

def create_circle_of_actors(actor_class, num_actors, radius, center_location=(0, 0, 0), face_center=True):
    """
    Create a circle of actors in the current level.
    
    Args:
        actor_class (class): Class of the actor to spawn
        num_actors (int): Number of actors in the circle
        radius (float): Radius of the circle
        center_location (tuple): Center location for the circle (X, Y, Z)
        face_center (bool): Whether the actors should face the center
        
    Returns:
        list: List of spawned actors
    """
    actors = []
    
    for i in range(num_actors):
        # Calculate the angle for this actor
        angle = 2 * math.pi * i / num_actors
        
        # Calculate the location for this actor
        x = center_location[0] + radius * math.cos(angle)
        y = center_location[1] + radius * math.sin(angle)
        z = center_location[2]
        
        # Calculate the rotation for this actor
        if face_center:
            # Calculate the rotation to face the center
            rotation = (0, math.degrees(angle) + 90, 0)
        else:
            rotation = (0, 0, 0)
        
        # Spawn the actor
        actor = spawn_actor(actor_class, (x, y, z), rotation)
        
        if actor:
            actors.append(actor)
    
    return actors

def create_random_scatter(actor_class, num_actors, min_x, max_x, min_y, max_y, z=0, min_scale=0.8, max_scale=1.2, random_rotation=True):
    """
    Create a random scatter of actors in the current level.
    
    Args:
        actor_class (class): Class of the actor to spawn
        num_actors (int): Number of actors to spawn
        min_x (float): Minimum X coordinate
        max_x (float): Maximum X coordinate
        min_y (float): Minimum Y coordinate
        max_y (float): Maximum Y coordinate
        z (float): Z coordinate
        min_scale (float): Minimum scale factor
        max_scale (float): Maximum scale factor
        random_rotation (bool): Whether to apply random rotation
        
    Returns:
        list: List of spawned actors
    """
    actors = []
    
    for i in range(num_actors):
        # Generate random location
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        
        # Generate random rotation
        if random_rotation:
            rotation = (0, random.uniform(0, 360), 0)
        else:
            rotation = (0, 0, 0)
        
        # Generate random scale
        scale_factor = random.uniform(min_scale, max_scale)
        scale = (scale_factor, scale_factor, scale_factor)
        
        # Spawn the actor
        actor = spawn_actor(actor_class, (x, y, z), rotation, scale)
        
        if actor:
            actors.append(actor)
    
    return actors

def align_actors_to_surface(actors, trace_distance=10000, trace_channel='Visibility'):
    """
    Align actors to the surface below them.
    
    Args:
        actors (list): List of actors to align
        trace_distance (float): Maximum distance to trace
        trace_channel (str): Trace channel to use
        
    Returns:
        int: Number of actors aligned
    """
    aligned_count = 0
    
    for actor in actors:
        # Get the actor's location
        location = actor.get_actor_location()
        
        # Create a trace start and end point
        start = unreal.Vector(location.x, location.y, location.z)
        end = unreal.Vector(location.x, location.y, location.z - trace_distance)
        
        # Perform the trace
        hit_result = unreal.SystemLibrary.line_trace_single(
            actor,
            start,
            end,
            trace_channel,
            False,
            [],
            unreal.DrawDebugTrace.NONE,
            True,
            unreal.LinearColor(1.0, 0.0, 0.0, 1.0),
            unreal.LinearColor(0.0, 1.0, 0.0, 1.0),
            5.0
        )
        
        # If we hit something, align the actor to the hit location
        if hit_result.hit_actor:
            # Get the hit location
            hit_location = hit_result.hit_location
            
            # Get the hit normal
            hit_normal = hit_result.hit_normal
            
            # Calculate the rotation to align with the surface
            rotation = unreal.Rotator.from_vector(hit_normal)
            
            # Set the actor's location and rotation
            actor.set_actor_location(hit_location)
            actor.set_actor_rotation(rotation)
            
            aligned_count += 1
    
    return aligned_count

def create_spline_path(spline_actor_class, points, tangents=None):
    """
    Create a spline path in the current level.
    
    Args:
        spline_actor_class (class): Class of the spline actor to spawn
        points (list): List of points for the spline (each point is a tuple of X, Y, Z)
        tangents (list): Optional list of tangents for the spline (each tangent is a tuple of X, Y, Z)
        
    Returns:
        object: The spawned spline actor
    """
    # Spawn the spline actor
    spline_actor = spawn_actor(spline_actor_class)
    
    if not spline_actor:
        return None
    
    # Get the spline component
    spline_component = spline_actor.spline_component
    
    # Clear any existing points
    spline_component.clear_spline_points()
    
    # Add the points to the spline
    for i, point in enumerate(points):
        # Convert the point to a Vector
        point_vector = unreal.Vector(point[0], point[1], point[2])
        
        # Add the point to the spline
        if tangents and i < len(tangents):
            # Convert the tangent to a Vector
            tangent_vector = unreal.Vector(tangents[i][0], tangents[i][1], tangents[i][2])
            
            # Add the point with the tangent
            spline_component.add_point(
                point_vector,
                tangent_vector,
                unreal.SplinePointType.CURVE,
                True
            )
        else:
            # Add the point without a tangent
            spline_component.add_point(
                point_vector,
                unreal.Vector(0, 0, 0),
                unreal.SplinePointType.LINEAR,
                True
            )
    
    return spline_actor

def place_actors_along_spline(spline_actor, actor_class, num_actors, offset=0, rotation_offset=(0, 0, 0), align_to_spline=True):
    """
    Place actors along a spline path.
    
    Args:
        spline_actor (object): The spline actor to place actors along
        actor_class (class): Class of the actor to spawn
        num_actors (int): Number of actors to place
        offset (float): Offset from the spline in units
        rotation_offset (tuple): Additional rotation to apply (Pitch, Yaw, Roll)
        align_to_spline (bool): Whether to align the actors to the spline direction
        
    Returns:
        list: List of spawned actors
    """
    actors = []
    
    # Get the spline component
    spline_component = spline_actor.spline_component
    
    # Get the spline length
    spline_length = spline_component.get_spline_length()
    
    # Calculate the spacing between actors
    spacing = spline_length / (num_actors - 1) if num_actors > 1 else 0
    
    for i in range(num_actors):
        # Calculate the distance along the spline
        distance = i * spacing
        
        # Get the location and direction at this distance
        location = spline_component.get_location_at_distance_along_spline(distance, unreal.SplineCoordinateSpace.WORLD)
        direction = spline_component.get_direction_at_distance_along_spline(distance, unreal.SplineCoordinateSpace.WORLD)
        
        # Calculate the rotation
        if align_to_spline:
            # Calculate the rotation to align with the spline direction
            rotation = unreal.Rotator.from_vector(direction)
            
            # Add the rotation offset
            rotation.pitch += rotation_offset[0]
            rotation.yaw += rotation_offset[1]
            rotation.roll += rotation_offset[2]
        else:
            rotation = unreal.Rotator(rotation_offset[0], rotation_offset[1], rotation_offset[2])
        
        # Calculate the offset location
        if offset != 0:
            # Calculate the right vector
            right = unreal.MathLibrary.cross_product(direction, unreal.Vector(0, 0, 1))
            right = unreal.MathLibrary.normal(right)
            
            # Apply the offset
            location += right * offset
        
        # Spawn the actor
        actor = spawn_actor(actor_class, (location.x, location.y, location.z), (rotation.pitch, rotation.yaw, rotation.roll))
        
        if actor:
            actors.append(actor)
    
    return actors

# Example usage
if __name__ == "__main__":
    # Create a grid of cubes
    cubes = create_grid_of_actors(unreal.StaticMeshActor, 5, 5)
    
    # Create a circle of spheres
    spheres = create_circle_of_actors(unreal.StaticMeshActor, 12, 500) 
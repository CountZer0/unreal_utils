# Gameplay Utils

A collection of reusable gameplay mechanics and systems for Unreal Engine.

## Features

### Blueprint Function Library

The plugin includes a Blueprint Function Library with the following utility functions:

#### Math Functions

- **SmoothRotatorInterp**: Calculates a smooth interpolation between two rotators using spherical interpolation.
  - Parameters:
    - Current: Current rotator
    - Target: Target rotator
    - DeltaTime: Time since last tick
    - InterpSpeed: Interpolation speed
  - Returns: Interpolated rotator

#### Movement Functions

- **CalculateJumpVelocity**: Calculates a parabolic jump velocity to reach a target position.
  - Parameters:
    - StartPos: Starting position
    - TargetPos: Target position to jump to
    - GravityZ: Z component of gravity (typically negative)
    - JumpTime: Desired time to reach the target
  - Returns: Velocity vector to apply for the jump

#### Actor Functions

- **FindClosestActor**: Finds the closest actor from an array of actors.
  - Parameters:
    - SourceLocation: Reference location to measure from
    - ActorArray: Array of actors to check
    - OutClosestActor: The closest actor found (output)
    - OutClosestDistance: The distance to the closest actor (output)
  - Returns: True if a closest actor was found

## Installation

1. Copy the GameplayUtils folder to your project's Plugins directory
2. Restart the Unreal Editor
3. Enable the plugin in Edit > Plugins

## Usage

After enabling the plugin, you can access the utility functions in your Blueprints by searching for them in the context menu. The functions are categorized under "GameplayUtils" with subcategories for Math, Movement, and Actor functions.

### Example: Using SmoothRotatorInterp

This function is useful for creating smooth camera or character rotations:

1. In your character or camera Blueprint, create a variable to store the target rotation
2. In the Tick event, use SmoothRotatorInterp to smoothly interpolate between the current rotation and the target rotation
3. Apply the resulting rotation to your character or camera

### Example: Using CalculateJumpVelocity

This function is useful for AI characters that need to jump to specific locations:

1. Determine the target location for the jump
2. Call CalculateJumpVelocity with the character's current location, target location, gravity, and desired jump time
3. Apply the resulting velocity to the character's movement component

### Example: Using FindClosestActor

This function is useful for finding the nearest enemy, pickup, or interactive object:

1. Get all actors of a specific class or with a specific tag
2. Call FindClosestActor with the character's location and the array of actors
3. Use the resulting closest actor for gameplay logic (attacking, interacting, etc.)
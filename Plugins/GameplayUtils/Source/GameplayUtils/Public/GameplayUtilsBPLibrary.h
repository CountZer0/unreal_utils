// Copyright (c) 2025 CountZer0. All rights reserved.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "GameplayUtilsBPLibrary.generated.h"

/**
 * Blueprint Function Library containing utility functions for gameplay mechanics
 */
UCLASS()
class GAMEPLAYUTILS_API UGameplayUtilsBPLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	/** 
	 * Calculates a smooth interpolation between two rotators using spherical interpolation
	 * @param Current - Current rotator
	 * @param Target - Target rotator
	 * @param DeltaTime - Time since last tick
	 * @param InterpSpeed - Interpolation speed
	 * @return Interpolated rotator
	 */
	UFUNCTION(BlueprintPure, Category = "GameplayUtils|Math")
	static FRotator SmoothRotatorInterp(const FRotator& Current, const FRotator& Target, float DeltaTime, float InterpSpeed);

	/**
	 * Calculates a parabolic jump velocity to reach a target position
	 * @param StartPos - Starting position
	 * @param TargetPos - Target position to jump to
	 * @param GravityZ - Z component of gravity (typically negative)
	 * @param JumpTime - Desired time to reach the target
	 * @return Velocity vector to apply for the jump
	 */
	UFUNCTION(BlueprintPure, Category = "GameplayUtils|Movement")
	static FVector CalculateJumpVelocity(const FVector& StartPos, const FVector& TargetPos, float GravityZ, float JumpTime);

	/**
	 * Finds the closest actor from an array of actors
	 * @param SourceLocation - Reference location to measure from
	 * @param ActorArray - Array of actors to check
	 * @param OutClosestActor - The closest actor found
	 * @param OutClosestDistance - The distance to the closest actor
	 * @return True if a closest actor was found
	 */
	UFUNCTION(BlueprintCallable, Category = "GameplayUtils|Actor")
	static bool FindClosestActor(const FVector& SourceLocation, const TArray<AActor*>& ActorArray, AActor*& OutClosestActor, float& OutClosestDistance);
};
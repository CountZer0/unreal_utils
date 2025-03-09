// Copyright (c) 2025 CountZer0. All rights reserved.

#include "GameplayUtilsBPLibrary.h"
#include "Kismet/KismetMathLibrary.h"

FRotator UGameplayUtilsBPLibrary::SmoothRotatorInterp(const FRotator& Current, const FRotator& Target, float DeltaTime, float InterpSpeed)
{
    // Use quaternion interpolation for smooth rotation
    const FQuat CurrentQuat = Current.Quaternion();
    const FQuat TargetQuat = Target.Quaternion();
    
    // Perform spherical interpolation between quaternions
    const FQuat ResultQuat = FQuat::Slerp(CurrentQuat, TargetQuat, FMath::Clamp(DeltaTime * InterpSpeed, 0.0f, 1.0f));
    
    // Convert back to rotator
    return ResultQuat.Rotator();
}

FVector UGameplayUtilsBPLibrary::CalculateJumpVelocity(const FVector& StartPos, const FVector& TargetPos, float GravityZ, float JumpTime)
{
    // Calculate the XY direction and distance
    FVector Direction = TargetPos - StartPos;
    const float ZDiff = Direction.Z;
    Direction.Z = 0.0f;
    
    const float XYDistance = Direction.Size();
    Direction.Normalize();
    
    // Calculate XY velocity needed to reach the target in the given time
    const FVector XYVelocity = Direction * (XYDistance / JumpTime);
    
    // Calculate Z velocity using the jump time and gravity
    // Using the formula: z = z0 + v0*t + 0.5*a*t^2
    // Solving for v0: v0 = (z - z0 - 0.5*a*t^2) / t
    const float ZVelocity = (ZDiff - 0.5f * GravityZ * JumpTime * JumpTime) / JumpTime;
    
    // Combine XY and Z velocities
    return FVector(XYVelocity.X, XYVelocity.Y, ZVelocity);
}

bool UGameplayUtilsBPLibrary::FindClosestActor(const FVector& SourceLocation, const TArray<AActor*>& ActorArray, AActor*& OutClosestActor, float& OutClosestDistance)
{
    OutClosestActor = nullptr;
    OutClosestDistance = MAX_FLT;
    
    if (ActorArray.Num() == 0)
    {
        return false;
    }
    
    for (AActor* Actor : ActorArray)
    {
        if (!Actor)
        {
            continue;
        }
        
        const float Distance = FVector::Distance(SourceLocation, Actor->GetActorLocation());
        
        if (Distance < OutClosestDistance)
        {
            OutClosestDistance = Distance;
            OutClosestActor = Actor;
        }
    }
    
    return OutClosestActor != nullptr;
}
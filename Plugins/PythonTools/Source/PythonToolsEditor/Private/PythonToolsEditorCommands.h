// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Framework/Commands/Commands.h"
#include "PythonToolsEditorStyle.h"

class FPythonToolsEditorCommands : public TCommands<FPythonToolsEditorCommands>
{
public:

	FPythonToolsEditorCommands()
		: TCommands<FPythonToolsEditorCommands>(TEXT("PythonToolsEditor"), NSLOCTEXT("Contexts", "PythonToolsEditor", "PythonTools Plugin"), NAME_None, FPythonToolsEditorStyle::GetStyleSetName())
	{
	}

	// TCommands<> interface
	virtual void RegisterCommands() override;

public:
	TSharedPtr< FUICommandInfo > PluginAction;
}; 
// Copyright Epic Games, Inc. All Rights Reserved.

#include "PythonToolsEditorCommands.h"

#define LOCTEXT_NAMESPACE "FPythonToolsEditorModule"

void FPythonToolsEditorCommands::RegisterCommands()
{
	UI_COMMAND(PluginAction, "Python Tools", "Execute Python Tools action", EUserInterfaceActionType::Button, FInputChord());
}

#undef LOCTEXT_NAMESPACE 
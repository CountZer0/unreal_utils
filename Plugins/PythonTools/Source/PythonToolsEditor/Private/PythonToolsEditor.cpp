// Copyright Epic Games, Inc. All Rights Reserved.

#include "PythonToolsEditor.h"
#include "PythonToolsEditorStyle.h"
#include "PythonToolsEditorCommands.h"
#include "Misc/MessageDialog.h"
#include "ToolMenus.h"

// Python includes
#include "PythonScriptPlugin.h"
#include "PythonScriptPluginSettings.h"
#include "IPythonScriptPlugin.h"

static const FName PythonToolsTabName("PythonTools");

#define LOCTEXT_NAMESPACE "FPythonToolsEditorModule"

void FPythonToolsEditorModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module

	FPythonToolsEditorStyle::Initialize();
	FPythonToolsEditorStyle::ReloadTextures();

	FPythonToolsEditorCommands::Register();
	
	PluginCommands = MakeShareable(new FUICommandList);

	PluginCommands->MapAction(
		FPythonToolsEditorCommands::Get().PluginAction,
		FExecuteAction::CreateRaw(this, &FPythonToolsEditorModule::PluginButtonClicked),
		FCanExecuteAction());

	UToolMenus::RegisterStartupCallback(FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FPythonToolsEditorModule::RegisterMenus));
	
	// Initialize Python paths
	InitializePythonPaths();
}

void FPythonToolsEditorModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.

	UToolMenus::UnRegisterStartupCallback(this);

	UToolMenus::UnregisterOwner(this);

	FPythonToolsEditorStyle::Shutdown();

	FPythonToolsEditorCommands::Unregister();
}

void FPythonToolsEditorModule::PluginButtonClicked()
{
	// Run a sample Python script
	RunPythonScript("import unreal\nunreal.log('Python Tools plugin is working!')");
}

void FPythonToolsEditorModule::RegisterMenus()
{
	// Owner will be used for cleanup in call to UToolMenus::UnregisterOwner
	FToolMenuOwnerScoped OwnerScoped(this);

	{
		UToolMenu* Menu = UToolMenus::Get()->ExtendMenu("LevelEditor.MainMenu.Window");
		{
			FToolMenuSection& Section = Menu->FindOrAddSection("WindowLayout");
			Section.AddMenuEntryWithCommandList(FPythonToolsEditorCommands::Get().PluginAction, PluginCommands);
		}
	}

	{
		UToolMenu* ToolbarMenu = UToolMenus::Get()->ExtendMenu("LevelEditor.LevelEditorToolBar");
		{
			FToolMenuSection& Section = ToolbarMenu->FindOrAddSection("Settings");
			{
				FToolMenuEntry& Entry = Section.AddEntry(FToolMenuEntry::InitToolBarButton(FPythonToolsEditorCommands::Get().PluginAction));
				Entry.SetCommandList(PluginCommands);
			}
		}
	}
}

void FPythonToolsEditorModule::InitializePythonPaths()
{
	// Make sure Python is enabled
	if (IPythonScriptPlugin::IsAvailable())
	{
		IPythonScriptPlugin& PythonScriptPlugin = IPythonScriptPlugin::Get();
		
		// Add our plugin's Python scripts directory to the Python path
		FString PluginPythonPath = FPaths::ConvertRelativePathToFull(FPaths::Combine(FPaths::ProjectPluginsDir(), TEXT("PythonTools"), TEXT("Content"), TEXT("Python")));
		PythonScriptPlugin.AddPythonPath(PluginPythonPath);
		
		// Add the project's Python scripts directory to the Python path
		FString ProjectPythonPath = FPaths::ConvertRelativePathToFull(FPaths::Combine(FPaths::ProjectContentDir(), TEXT("Python")));
		PythonScriptPlugin.AddPythonPath(ProjectPythonPath);
		
		UE_LOG(LogTemp, Log, TEXT("Python paths initialized for PythonTools plugin"));
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("Python Script Plugin is not available. Please enable it in Edit > Plugins > Scripting > Python Editor Script Plugin"));
	}
}

bool FPythonToolsEditorModule::RunPythonScript(const FString& PythonScript)
{
	if (IPythonScriptPlugin::IsAvailable())
	{
		IPythonScriptPlugin& PythonScriptPlugin = IPythonScriptPlugin::Get();
		return PythonScriptPlugin.ExecPythonCommand(*PythonScript);
	}
	
	UE_LOG(LogTemp, Warning, TEXT("Failed to run Python script: Python Script Plugin is not available"));
	return false;
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FPythonToolsEditorModule, PythonToolsEditor) 
// Copyright Epic Games, Inc. All Rights Reserved.

#include "PythonToolsEditorStyle.h"
#include "PythonToolsEditor.h"
#include "Framework/Application/SlateApplication.h"
#include "Styling/SlateStyleRegistry.h"
#include "Slate/SlateGameResources.h"
#include "Interfaces/IPluginManager.h"
#include "Styling/SlateStyleMacros.h"

#define RootToContentDir Style->RootToContentDir

TSharedPtr< FSlateStyleSet > FPythonToolsEditorStyle::StyleInstance = nullptr;

void FPythonToolsEditorStyle::Initialize()
{
	if (!StyleInstance.IsValid())
	{
		StyleInstance = Create();
		FSlateStyleRegistry::RegisterSlateStyle(*StyleInstance);
	}
}

void FPythonToolsEditorStyle::Shutdown()
{
	FSlateStyleRegistry::UnRegisterSlateStyle(*StyleInstance);
	ensure(StyleInstance.IsUnique());
	StyleInstance.Reset();
}

FName FPythonToolsEditorStyle::GetStyleSetName()
{
	static FName StyleSetName(TEXT("PythonToolsEditorStyle"));
	return StyleSetName;
}

const FVector2D Icon16x16(16.0f, 16.0f);
const FVector2D Icon20x20(20.0f, 20.0f);

TSharedRef< FSlateStyleSet > FPythonToolsEditorStyle::Create()
{
	TSharedRef< FSlateStyleSet > Style = MakeShareable(new FSlateStyleSet("PythonToolsEditorStyle"));
	Style->SetContentRoot(IPluginManager::Get().FindPlugin("PythonTools")->GetBaseDir() / TEXT("Resources"));

	Style->Set("PythonToolsEditor.PluginAction", new IMAGE_BRUSH(TEXT("ButtonIcon_40x"), Icon20x20));
	
	return Style;
}

void FPythonToolsEditorStyle::ReloadTextures()
{
	if (FSlateApplication::IsInitialized())
	{
		FSlateApplication::Get().GetRenderer()->ReloadTextureResources();
	}
}

const ISlateStyle& FPythonToolsEditorStyle::Get()
{
	return *StyleInstance;
} 
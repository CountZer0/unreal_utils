# Unreal Utils

A collection of utility functions, tools, and snippets for Unreal Engine development.

## Overview

This repository contains a variety of utilities designed to streamline and enhance Unreal Engine development workflows. These utilities aim to solve common problems, automate repetitive tasks, and provide helpful extensions to the Unreal Engine ecosystem.

## Features

- **Blueprint Function Libraries**: Reusable Blueprint functions for common game development tasks
- **Editor Utilities**: Tools to enhance the Unreal Editor experience
- **Performance Optimization**: Utilities for profiling and optimizing Unreal Engine projects
- **Gameplay Helpers**: Common gameplay mechanics and systems
- **Asset Management**: Tools for managing and organizing project assets
- **Python Scripting**: Python utilities and scripts for Unreal Engine 5.5

## Getting Started

### Prerequisites

- Unreal Engine 4.26 or later (some utilities may work with earlier versions)
- Basic knowledge of Unreal Engine development
- Visual Studio 2019 or later (for C++ utilities)
- Python 3.9+ (for Python utilities in UE5.5)

### Installation

#### As a Plugin

1. Clone this repository or download the latest release
2. Copy the desired plugin folders to your Unreal Engine project's `Plugins` directory
3. Restart the Unreal Editor
4. Enable the plugin(s) in Edit > Plugins

#### Individual Utilities

1. Browse the repository for specific utilities you need
2. Follow the installation instructions in each utility's documentation

#### Python Tools

1. Enable the Python Editor Script Plugin in Edit > Plugins > Scripting
2. Copy the PythonTools plugin to your project's Plugins directory
3. Copy the Python scripts from Snippets/Python to your project
4. See the [Python documentation](Documentation/Python/README.md) for more details

## Documentation

Detailed documentation for each utility can be found in their respective directories. The documentation includes:

- Usage instructions
- API reference
- Examples
- Performance considerations

## Project Structure

```
unreal_utils/
├── Plugins/
│   ├── EditorTools/
│   ├── GameplayUtils/
│   ├── PerformanceTools/
│   └── PythonTools/
├── Snippets/
│   ├── Blueprint/
│   ├── C++/
│   └── Python/
├── Examples/
└── Documentation/
    └── Python/
```

## Python Tools

The Python tools provide a variety of utilities for automating tasks in Unreal Engine 5.5:

- **Asset Management**: Find, organize, and manipulate assets
- **Editor Automation**: Create custom editor tools and commands
- **Level Design**: Automate level design tasks
- **Data Processing**: Process and transform data
- **UI Extensions**: Create custom UI elements

See the [Python documentation](Documentation/Python/README.md) for more details.

## Contributing

Contributions are welcome! If you have a utility that might be useful to others, please consider contributing it to this repository.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-utility`)
3. Commit your changes (`git commit -m 'Add some amazing utility'`)
4. Push to the branch (`git push origin feature/amazing-utility`)
5. Open a Pull Request

Please make sure your code follows the [Unreal Engine coding standards](https://docs.unrealengine.com/en-US/ProductionPipelines/DevelopmentSetup/CodingStandard/index.html).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Epic Games for creating Unreal Engine
- The Unreal Engine community for their continuous support and inspiration
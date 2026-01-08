# AI Workflow Config Tools for Blender

A Blender add-on that provides JSON-driven workflow actions for camera control, image management, node tree switching, timeline control, and automated image saving. Perfect for AI-assisted video production workflows.

## Features

- **Camera Management**: Automatically switch between cameras and create them if they don't exist
- **Image Editor Control**: Change displayed images in the Image Editor viewport
- **Node Tree Switching**: Switch between different node trees (great for ComfyUI integration)
- **Timeline Control**: Jump to specific frames automatically
- **Image Reset**: Reset images to blank state for new renders
- **Batch Image Saving**: Save multiple images to disk with configurable paths
- **User-Friendly Configuration**: Edit all settings through Blender's preferences UI
- **JSON Import/Export**: Portable configuration files for sharing workflows

## Installation

### Method 1: Install as ZIP (Recommended)

1. Download or zip the `ai_workflow_tools` folder
2. In Blender, go to **Edit → Preferences → Add-ons**
3. Click **Install...** and select the `ai_workflow_tools` folder or zip file
4. Enable the add-on by checking the checkbox next to "Development: AI Workflow Config Tools"

### Method 2: Manual Installation

1. Copy the entire `ai_workflow_tools` folder to your Blender addons directory:
   - **Windows**: `C:\Users\{username}\AppData\Roaming\Blender Foundation\Blender\{version}\scripts\addons\`
   - **macOS**: `/Users/{username}/Library/Application Support/Blender/{version}/scripts/addons/`
   - **Linux**: `~/.config/blender/{version}/scripts/addons/`

2. Restart Blender or click **Refresh** in the Add-ons preferences
3. Enable the add-on in **Edit → Preferences → Add-ons**

## Usage

### Quick Start

1. After installation, find the **AI Tools** tab in the 3D Viewport sidebar (press `N` if hidden)
2. Click **Edit Config** to open the preferences panel
3. Click **Load from JSON** to load the default configuration
4. Add, edit, or remove actions as needed
5. Click **Save to JSON** to save your configuration
6. Use the action buttons in the AI Tools panel to execute workflows

### Creating Actions

The add-on supports three types of actions:

#### 1. Camera Select / View
- Switches active camera
- Changes image in Image Editor
- Switches node tree
- Optionally updates timeline frame

#### 2. Reset Images
- Resets specified images to blank
- Optionally switches camera and node tree
- Great for preparing new render passes

#### 3. Save Images
- Saves multiple images to disk
- Supports custom file paths
- Optional overwrite protection

### Configuring Actions

1. Open **Edit → Preferences → Add-ons → AI Workflow Config Tools**
2. Use the **+** button to add a new action
3. Select the action in the list to edit its properties
4. Configure the action settings:
   - **Button Name**: Display name in the UI
   - **Action Type**: Choose from Camera Select, Reset, or Save Images
   - **Camera Settings**: Enable/disable camera switching
   - **Image Editor**: Choose which image to display
   - **Node Tree**: Select which node tree to activate
   - **Timeline**: Set frame to jump to
   - **Images**: Add images to reset or save

5. Click **Save to JSON** to persist your configuration

### Sharing Configurations

Your configuration is stored in `ai_workflow_tools/config.json`. You can:
- Share this file with team members
- Version control it with git
- Create multiple configurations and swap them out
- Edit it directly in a text editor (advanced users)

## Configuration File Format

The `config.json` file uses this structure:

```json
[
    {
        "button_name": "First Frame View",
        "action_type": "CAMERA_SELECT",
        "select_camera": true,
        "camera_object_name": "Camera.001",
        "change_image_editor": true,
        "image_name_to_view": "FirstFrame",
        "change_node_tree": true,
        "node_tree_name": "First Frame",
        "update_timeline": false,
        "timeline_frame": 0
    }
]
```

## File Structure

```
ai_workflow_tools/
├── __init__.py          # Main entry point with bl_info
├── config_manager.py    # JSON loading and saving logic
├── operators.py         # All operator classes
├── panels.py            # 3D View UI panel
├── preferences.py       # Addon preferences panel
├── properties.py        # Property group definitions
├── ui_lists.py          # UIList components
├── utils.py             # Helper functions
└── config.json          # Configuration file
```

## Development

### Module Structure

The add-on uses a modular architecture:

- **properties.py**: Defines data structures for actions
- **operators.py**: Implements action execution and management
- **panels.py**: Creates the main UI panel in 3D View
- **preferences.py**: Builds the configuration UI in preferences
- **ui_lists.py**: Custom list widgets for actions
- **utils.py**: Shared utility functions
- **config_manager.py**: Handles JSON serialization

### Hot Reload

The add-on supports hot reloading during development. When enabled, changes to modules are automatically reloaded without restarting Blender.

## Troubleshooting

### Actions not appearing
- Click **Reload Config** in the AI Tools panel
- Check the config.json file exists in the addon folder
- Verify the JSON syntax is valid

### Camera/Image/Node Tree not found
- The add-on will create cameras and images automatically if they don't exist
- Node trees must exist before switching (create them in your .blend file first)

### Config changes not saving
- Make sure you click **Save to JSON** in preferences after editing
- Check file permissions on the config.json file
- Verify the addon folder is writable

## Version History

### v2.0.0 (Current)
- Complete refactor to modular architecture
- Added preferences UI for configuration
- Added action management (add, remove, duplicate, reorder)
- Improved error handling and validation
- Cross-platform path support
- Better file format detection for image saving

### v1.4.0
- Initial release with JSON-driven actions
- Basic camera, image, and node tree control

## Credits

- **Original Author**: Your Name / Gemini
- **License**: (Add your license here)

## Support

For issues and feature requests, please use the GitHub issue tracker.

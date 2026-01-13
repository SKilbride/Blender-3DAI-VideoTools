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
- **One-Click Resource Creation**: Create cameras and images directly from the preferences panel
- **Smart Validation**: Visual warnings when resources don't exist, with quick creation buttons
- **JSON Import/Export**: Portable configuration files for sharing workflows

## Installation

### Method 1: Install from GitHub (Recommended)

1. **Clone or Download** this repository:
   ```bash
   git clone https://github.com/SKilbride/blender_ai_workflow_tools.git
   ```
   Or download as ZIP from GitHub and extract it

2. **Install in Blender**:
   - Go to **Edit → Preferences → Add-ons**
   - Click **Install...** and select the folder (or create a ZIP of it first)
   - Enable the add-on by checking the checkbox next to "Development: AI Workflow Config Tools"

### Method 2: Manual Installation

1. Clone or download this repository
2. Copy the entire repository folder to your Blender addons directory:
   - **Windows**: `C:\Users\{username}\AppData\Roaming\Blender Foundation\Blender\{version}\scripts\addons\`
   - **macOS**: `/Users/{username}/Library/Application Support/Blender/{version}/scripts/addons/`
   - **Linux**: `~/.config/blender/{version}/scripts/addons/`

3. Restart Blender or click **Refresh** in the Add-ons preferences
4. Enable the add-on in **Edit → Preferences → Add-ons**

## Usage

### Quick Start

1. After installation, find the **AI Tools** tab in the 3D Viewport sidebar (press `N` if hidden)
2. Click **Edit Config** to open the preferences panel
3. Click **Load from JSON** to load the default configuration
4. Add, edit, or remove actions as needed
5. Click **Save to JSON** to save your configuration
6. Use the action buttons in the AI Tools panel to execute workflows

[ADD IMAGE: Screenshot of the AI Tools panel in the 3D Viewport sidebar showing the action buttons (First Frame View, LastFrame Frame View, Show Depth, Save Outputs, Reset Images/Setup) with the "Reload Config" and "Edit Config" buttons at the top]

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

[ADD IMAGE: Screenshot of the preferences panel showing the action list on the left with actions like "First Frame View", "LastFrame Frame View", etc., and the action editor on the right showing all the configuration options for a selected action]

### Creating Cameras and Images

The addon includes smart validation that warns you when a camera or image doesn't exist, and provides quick creation buttons:

#### Creating Cameras

When you specify a camera name that doesn't exist:
1. A **warning icon** appears showing "⚠ Camera 'CameraName' doesn't exist"
2. Click the **+** button next to the camera name field
3. A dialog appears where you can set the camera location (X, Y, Z)
4. Click **OK** to create the camera at that position

[ADD IMAGE: Screenshot showing the Camera settings section with a camera name "Camera.001" typed in, a warning message below saying "⚠ Camera 'Camera.001' doesn't exist", and the + button highlighted next to the search icon]

[ADD IMAGE: Screenshot of the "Create Camera" dialog popup showing fields for X, Y, Z location with the camera name "Camera.001" at the top]

#### Creating Images

When you specify an image name that doesn't exist:
1. A **warning icon** appears showing "⚠ Image 'ImageName' doesn't exist"
2. Click the **+** button next to the image name field
3. A dialog appears where you can set width and height (default: 1920x1080)
4. Click **OK** to create a blank image with those dimensions

This works for:
- **Image Editor View**: The image to display when the action runs
- **Reset Images**: Any images you want to reset to blank
- **Save Images**: Any images you want to save to disk

[ADD IMAGE: Screenshot showing the Image Editor settings section with an image name "FirstFrame" typed in, a warning message below saying "⚠ Image 'FirstFrame' doesn't exist", and the + button highlighted]

[ADD IMAGE: Screenshot of the "Create Image" dialog popup showing Width and Height fields (1920 x 1080) with the image name "FirstFrame" at the top]

#### Validation Features

The preferences panel provides real-time validation:

- **Camera Validation**:
  - Warns if camera doesn't exist
  - Warns if object exists but is not a camera type
  - Shows green checkmark when camera exists and is valid

- **Image Validation**:
  - Warns if image doesn't exist
  - Automatically hidden when image exists

- **Search & Create**:
  - Use the search icon (🔍) to pick from existing resources
  - Use the plus icon (+) to create new resources

[ADD IMAGE: Screenshot showing multiple validation states - one section with a valid camera (no warning), one with a non-existent camera (warning shown), and one with an existing object that's not a camera (different warning shown)]

### Example Workflow

Here's a typical workflow for setting up a new AI video generation project:

1. **Open Preferences** and click **Edit Config**
2. **Add a new action** called "First Frame Setup"
3. **Configure the action**:
   - Type camera name "Camera.FirstFrame" → Click **+** to create it at position (0, -5, 2)
   - Type image name "FirstFrame" → Click **+** to create it (1920x1080)
   - Enable "Change Image Editor" and select the "FirstFrame" image
   - Enable "Change Node Tree" and select your ComfyUI workflow
4. **Add another action** called "Save Rendered Frames"
   - Select action type: "Save Images"
   - Add image "FirstFrame" → Save as `//output/first_frame.png`
   - Add image "LastFrame" → Save as `//output/last_frame.png`
5. **Save to JSON** to persist your configuration
6. **Switch to 3D View** and click your action buttons to test

[ADD IMAGE: Screenshot showing a complete workflow - the preferences panel with a configured action on the left side, and the 3D viewport on the right with the AI Tools panel showing the corresponding action buttons]

### Sharing Configurations

Your configuration is stored in `config.json` in the addon folder. You can:
- Share this file with team members
- Version control it with git
- Create multiple configurations and swap them out
- Edit it directly in a text editor (advanced users)

**Pro Tip**: Use relative paths (`//output/`) instead of absolute paths for portability across different machines and operating systems.

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
blender_ai_workflow_tools/  # The addon (install this folder)
├── __init__.py             # Main entry point with bl_info
├── config_manager.py       # JSON loading and saving logic
├── operators.py            # All operator classes
├── panels.py               # 3D View UI panel
├── preferences.py          # Addon preferences panel
├── properties.py           # Property group definitions
├── ui_lists.py             # UIList components
├── utils.py                # Helper functions
├── config.json             # Configuration file
├── README.md               # Documentation
├── INSTALL.md              # Installation guide
└── .gitignore              # Git configuration
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

### Camera/Image not found
- When configuring actions, use the **+** button to create missing cameras or images
- The add-on will also automatically create cameras and images when actions run if they don't exist
- For immediate visibility, create resources via the preferences UI before running actions

### Camera/Image warnings in preferences
- **Warning shown**: Resource doesn't exist - click the **+** button to create it
- **No warning**: Resource exists and is valid
- **"Not a camera" warning**: An object with that name exists but isn't a camera - choose a different name or delete the conflicting object

### Node Tree not found
- Node trees cannot be created automatically - create them in your .blend file first
- Use the ComfyUI Blender addon or manually create node groups
- Ensure the node tree name matches exactly (case-sensitive)

### Config changes not saving
- Make sure you click **Save to JSON** in preferences after editing
- Check file permissions on the config.json file
- Verify the addon folder is writable

### Create buttons not working
- Ensure you've typed a name in the field before clicking the + button
- Check the Blender console (Window → Toggle System Console on Windows) for error messages
- Verify you have permission to create objects in the current scene

## Version History

### v2.0.0 (Current)
- **Complete refactor to modular architecture**
  - Split into separate modules for maintainability
  - Hot reload support for development
  - Proper package structure for distribution

- **Full preferences UI for configuration**
  - Visual action list with icons and type badges
  - Add, remove, duplicate, and reorder actions
  - Search-enabled pickers for cameras, images, and node trees
  - Save/load configuration to/from JSON

- **One-click resource creation**
  - Create cameras directly from preferences with custom location
  - Create images directly from preferences with custom dimensions
  - Smart dialogs for specifying resource properties

- **Smart validation and warnings**
  - Real-time validation of camera and image existence
  - Visual warnings when resources don't exist
  - Warnings when objects exist but aren't the correct type
  - Quick create buttons next to all resource fields

- **Cross-platform improvements**
  - Relative path support using Blender's // notation
  - Better file format detection for image saving (.jpg, .jpeg, .png, .exr, etc.)
  - Fixed hardcoded Windows paths in default config

- **Improved error handling**
  - Proper exception catching throughout
  - User-friendly error messages
  - Input validation before saving

### v1.4.0
- Initial release with JSON-driven actions
- Basic camera, image, and node tree control

## Credits

- **Original Author**: Your Name / Gemini
- **License**: (Add your license here)

## Support

For issues and feature requests, please use the GitHub issue tracker.

# Installation Guide

## Quick Install

### Option 1: Install from Folder (Recommended)

1. **Locate the addon folder**: `ai_workflow_tools/`

2. **Create a ZIP file** (optional but recommended):
   ```bash
   # On Linux/Mac:
   cd Blender-3DAI-VideoTools
   zip -r ai_workflow_tools.zip ai_workflow_tools/

   # On Windows:
   # Right-click the ai_workflow_tools folder → Send to → Compressed (zipped) folder
   ```

3. **Install in Blender**:
   - Open Blender
   - Go to **Edit → Preferences** (or **Blender → Preferences** on macOS)
   - Select the **Add-ons** tab
   - Click **Install...** button at the top
   - Navigate to and select either:
     - The `ai_workflow_tools.zip` file, or
     - The `ai_workflow_tools` folder directly
   - Click **Install Add-on**

4. **Enable the addon**:
   - Search for "AI Workflow" in the add-ons list
   - Check the checkbox next to **"Development: AI Workflow Config Tools"**
   - The addon is now active!

### Option 2: Manual Installation

1. **Find your Blender addons folder**:
   - **Windows**: `C:\Users\{YourUsername}\AppData\Roaming\Blender Foundation\Blender\{version}\scripts\addons\`
   - **macOS**: `/Users/{YourUsername}/Library/Application Support/Blender/{version}/scripts/addons/`
   - **Linux**: `~/.config/blender/{version}/scripts/addons/`

2. **Copy the folder**:
   - Copy the entire `ai_workflow_tools` folder into the addons directory

3. **Restart Blender** or click **Refresh** in Add-ons preferences

4. **Enable the addon**:
   - Go to **Edit → Preferences → Add-ons**
   - Search for "AI Workflow"
   - Check the checkbox to enable it

## First Time Setup

After installation:

1. **Find the panel**:
   - Open the 3D Viewport
   - Press `N` to show the sidebar (if hidden)
   - Look for the **"AI Tools"** tab

2. **Configure your actions**:
   - Click **"Edit Config"** to open preferences
   - Click **"Load from JSON"** to load the example configuration
   - Or click **"+"** to create your first action from scratch

3. **Save your configuration**:
   - After making changes, click **"Save to JSON"**
   - Your configuration is saved in `ai_workflow_tools/config.json`

## Verification

To verify the installation worked:

1. Open the 3D Viewport sidebar (`N` key)
2. Look for the **"AI Tools"** tab
3. You should see the "AI Workflow Config" panel
4. If you see action buttons or "No actions loaded", the addon is working correctly

## Troubleshooting

### "Add-on not showing up"
- Make sure you enabled the checkbox in preferences
- Try searching for "AI" or "Workflow" in the add-ons search
- Check that the folder name is exactly `ai_workflow_tools` (no extra characters)

### "No module named 'ai_workflow_tools'"
- The folder structure is incorrect
- Make sure `__init__.py` is directly inside `ai_workflow_tools/`
- Don't nest folders (it should be `addons/ai_workflow_tools/__init__.py`)

### "Panel not visible"
- Press `N` in the 3D Viewport to show the sidebar
- Look for the "AI Tools" tab at the top of the sidebar
- Make sure the addon is enabled in preferences

### "No actions loaded"
- The addon installed correctly but needs configuration
- Click "Edit Config" and then "Load from JSON"
- Or create your first action using the "+" button

## Updating

To update the addon:

1. **Option A**: Replace the folder
   - Delete the old `ai_workflow_tools` folder from addons
   - Copy in the new version
   - Restart Blender

2. **Option B**: Reinstall
   - Disable and remove the old version in preferences
   - Install the new version using the Install button

**Note**: Your `config.json` will be preserved if you're updating the addon files directly. If you want to keep your custom configuration, back up `config.json` before updating.

## Uninstallation

To remove the addon:

1. Go to **Edit → Preferences → Add-ons**
2. Find "AI Workflow Config Tools"
3. Click the **Remove** button
4. Or manually delete the `ai_workflow_tools` folder from your addons directory

## Next Steps

- Read the [README.md](README.md) for detailed usage instructions
- Explore the example configuration in the preferences
- Create your first custom action!

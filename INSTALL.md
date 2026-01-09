# Installation Guide

## Quick Install

### Option 1: Install from GitHub (Recommended)

1. **Clone or download the repository**:
   ```bash
   # Clone with git
   git clone https://github.com/SKilbride/Blender-3DAI-VideoTools.git

   # Or download ZIP from GitHub and extract
   ```

2. **Rename folder** (optional but recommended):
   - Rename `Blender-3DAI-VideoTools` to `ai_workflow_tools` for a cleaner name

3. **Create a ZIP file** (optional):
   ```bash
   # On Linux/Mac:
   zip -r ai_workflow_tools.zip ai_workflow_tools/

   # On Windows:
   # Right-click the folder → Send to → Compressed (zipped) folder
   ```

4. **Install in Blender**:
   - Open Blender
   - Go to **Edit → Preferences** (or **Blender → Preferences** on macOS)
   - Select the **Add-ons** tab
   - Click **Install...** button at the top
   - Navigate to and select either:
     - The ZIP file you created, or
     - The folder directly (Blender-3DAI-VideoTools or ai_workflow_tools)
   - Click **Install Add-on**

5. **Enable the addon**:
   - Search for "AI Workflow" in the add-ons list
   - Check the checkbox next to **"Development: AI Workflow Config Tools"**
   - The addon is now active!

### Option 2: Manual Installation

1. **Clone or download the repository** (see Option 1, step 1)

2. **Find your Blender addons folder**:
   - **Windows**: `C:\Users\{YourUsername}\AppData\Roaming\Blender Foundation\Blender\{version}\scripts\addons\`
   - **macOS**: `/Users/{YourUsername}/Library/Application Support/Blender/{version}/scripts/addons/`
   - **Linux**: `~/.config/blender/{version}/scripts/addons/`

3. **Copy the folder**:
   - Copy the entire repository folder into the addons directory
   - You can rename it to `ai_workflow_tools` for simplicity

4. **Restart Blender** or click **Refresh** in Add-ons preferences

5. **Enable the addon**:
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
- Check that the folder contains `__init__.py` with `bl_info`

### "No module named" errors
- The folder structure is incorrect
- Make sure `__init__.py` is directly inside the addon folder
- Don't nest folders (it should be `addons/Blender-3DAI-VideoTools/__init__.py` or `addons/ai_workflow_tools/__init__.py`)

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

1. **Option A**: Pull latest changes (if using git)
   ```bash
   cd /path/to/addon/folder
   git pull origin main
   ```
   - Restart Blender to reload the addon

2. **Option B**: Replace the folder
   - Delete the old addon folder from addons directory
   - Download/clone the new version
   - Copy it into addons directory
   - Restart Blender

3. **Option C**: Reinstall via Blender
   - Disable and remove the old version in preferences
   - Install the new version using the Install button

**Note**: Your `config.json` will be preserved if you're updating in place. If you want to keep your custom configuration, back up `config.json` before updating.

## Uninstallation

To remove the addon:

1. Go to **Edit → Preferences → Add-ons**
2. Find "AI Workflow Config Tools"
3. Click the **Remove** button
4. Or manually delete the addon folder from your addons directory

## Next Steps

- Read the [README.md](README.md) for detailed usage instructions
- Explore the example configuration in the preferences
- Create your first custom action!

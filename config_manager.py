"""
Configuration manager for loading and saving JSON configs
"""

import bpy
import json
from pathlib import Path

# Module-level initialization flag
__initialized_flag = False

# Internal config text block name
INTERNAL_CONFIG_NAME = "AI_Tool_Config.json"


def get_config_path():
    """Returns the path to the config.json file."""
    addon_dir = Path(__file__).parent
    return addon_dir / "config.json"


def has_internal_config():
    """Check if the current .blend file has an internal config."""
    return INTERNAL_CONFIG_NAME in bpy.data.texts


def get_internal_config_data():
    """
    Load config data from internal .blend text block.

    Returns:
        tuple: (success: bool, data: list or None, error: str or None)
    """
    if not has_internal_config():
        return False, None, "No internal config found"

    try:
        text_block = bpy.data.texts[INTERNAL_CONFIG_NAME]
        config_content = text_block.as_string()
        config_data = json.loads(config_content)
        return True, config_data, None
    except json.JSONDecodeError as e:
        return False, None, f"Invalid JSON in internal config: {str(e)}"
    except Exception as e:
        return False, None, f"Error reading internal config: {str(e)}"


def save_internal_config(config_data):
    """
    Save config data to internal .blend text block.

    Args:
        config_data: List of action dictionaries

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Create or get existing text block
        if INTERNAL_CONFIG_NAME in bpy.data.texts:
            text_block = bpy.data.texts[INTERNAL_CONFIG_NAME]
            text_block.clear()
        else:
            text_block = bpy.data.texts.new(INTERNAL_CONFIG_NAME)

        # Write JSON to text block
        json_str = json.dumps(config_data, indent=4, ensure_ascii=False)
        text_block.write(json_str)

        return True, f"Saved config to internal .blend file"
    except Exception as e:
        return False, f"Failed to save internal config: {str(e)}"


def delete_internal_config():
    """
    Delete the internal config from the .blend file.

    Returns:
        tuple: (success: bool, message: str)
    """
    if not has_internal_config():
        return False, "No internal config to delete"

    try:
        bpy.data.texts.remove(bpy.data.texts[INTERNAL_CONFIG_NAME])
        return True, "Deleted internal config"
    except Exception as e:
        return False, f"Failed to delete internal config: {str(e)}"


def load_config(context):
    """
    Loads action configuration into scene properties.
    Priority: Internal .blend config > External config.json
    """
    scene = context.scene
    props = scene.my_addon_props

    props.actions.clear()
    props.error_message = ""

    print(f"=== AI Workflow Config Loader ===")

    # Check for internal config first (project-specific)
    if has_internal_config():
        success, config_data, error = get_internal_config_data()
        if success:
            print(f"Loading from INTERNAL .blend config")
            print(f"Loaded {len(config_data)} entries from internal config")
        else:
            print(f"ERROR: {error}")
            props.error_message = error
            # Fall through to try external config
            config_data = None
    else:
        config_data = None

    # Fall back to external config.json if no internal config
    if config_data is None:
        json_path = get_config_path()
        print(f"Looking for EXTERNAL config at: {json_path}")
        print(f"Config exists: {json_path.exists()}")

        if not json_path.exists():
            error_msg = f"Config not found at:\n{json_path}"
            props.error_message = error_msg
            print(f"ERROR: {error_msg}")
            return

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

            print(f"Loaded {len(config_data)} entries from external config")

        except Exception as e:
            error_msg = f"Error loading external config:\n{str(e)}"
            props.error_message = error_msg
            print(f"ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
            return

    # Process config_data (from either source)
    if config_data:
        try:
            for idx, item in enumerate(config_data):
                try:
                    action = props.actions.add()

                    action.button_name = item.get("button_name", "Unnamed Action")
                    action.action_type = item.get("action_type", "CAMERA_SELECT")
                    action.select_camera = item.get("select_camera", False)
                    action.change_image_editor = item.get("change_image_editor", False)
                    action.image_name_to_view = item.get("image_name_to_view", "")
                    action.reset_images = item.get("reset_images", False)
                    action.change_node_tree = item.get("change_node_tree", False)
                    action.node_tree_name = item.get("node_tree_name", "")
                    action.update_timeline = item.get("update_timeline", False)
                    action.timeline_frame = item.get("timeline_frame", 0)

                    print(f"  Action {idx}: '{action.button_name}' (type: {action.action_type})")

                    # Handle camera
                    cam_name = item.get("camera_object_name")
                    if cam_name:
                        action.camera_name = cam_name
                        if cam_name in bpy.data.objects and bpy.data.objects[cam_name].type == 'CAMERA':
                            print(f"    Camera: {cam_name} ✓ (exists)")
                        else:
                            print(f"    Camera: {cam_name} (will create if needed)")

                    if action.change_node_tree:
                        print(f"    Node tree: '{action.node_tree_name}' (will verify at execution)")

                    if action.update_timeline:
                        print(f"    Timeline: frame {action.timeline_frame}")

                    # Handle images to reset
                    if item.get("reset_images") and action.action_type == 'RESET':
                        for img_item in item.get("images_to_reset", []):
                            reset_img = action.images_to_reset.add()
                            reset_img.name = img_item.get("name", "")
                            print(f"    Reset image: {reset_img.name}")

                    # Handle images to save
                    if action.action_type == 'IMAGE_SAVE':
                        for img_item in item.get("images_to_save", []):
                            save_img = action.images_to_save.add()
                            save_img.name = img_item.get("name", "")
                            save_img.save_as = img_item.get("save_as", "")
                            save_img.allow_overwrite = img_item.get("allow_overwrite", True)
                            print(f"    Save image: '{save_img.name}' → '{save_img.save_as}'")

                except Exception as e:
                    print(f"  ERROR loading action {idx}: {e}")
                    import traceback
                    traceback.print_exc()
                    # Continue loading other actions even if one fails

            print(f"Successfully loaded {len(props.actions)} actions")
            print("=================================")

        except Exception as e:
            error_msg = f"Error processing config:\n{str(e)}"
            props.error_message = error_msg
            print(f"ERROR: {error_msg}")
            import traceback
            traceback.print_exc()


def save_config(actions):
    """
    Saves actions to config.json.

    Args:
        actions: Collection of ActionProperty objects

    Returns:
        tuple: (success: bool, message: str)
    """
    json_path = get_config_path()

    try:
        config_data = []

        for action in actions:
            item = {
                "button_name": action.button_name,
                "action_type": action.action_type,
            }

            # Camera settings
            if action.select_camera and action.camera_name:
                item["select_camera"] = True
                item["camera_object_name"] = action.camera_name
            else:
                item["select_camera"] = False

            # Image editor settings
            if action.change_image_editor and action.image_name_to_view:
                item["change_image_editor"] = True
                item["image_name_to_view"] = action.image_name_to_view
            else:
                item["change_image_editor"] = False

            # Node tree settings
            if action.change_node_tree and action.node_tree_name:
                item["change_node_tree"] = True
                item["node_tree_name"] = action.node_tree_name
            else:
                item["change_node_tree"] = False

            # Timeline settings
            if action.update_timeline:
                item["update_timeline"] = True
                item["timeline_frame"] = action.timeline_frame
            else:
                item["update_timeline"] = False

            # Image reset settings (for RESET type)
            if action.action_type == 'RESET' and action.reset_images:
                item["reset_images"] = True
                item["images_to_reset"] = [
                    {"name": img.name} for img in action.images_to_reset
                ]
            else:
                item["reset_images"] = False

            # Image save settings (for IMAGE_SAVE type)
            if action.action_type == 'IMAGE_SAVE':
                item["images_to_save"] = [
                    {
                        "name": img.name,
                        "save_as": img.save_as,
                        "allow_overwrite": img.allow_overwrite
                    }
                    for img in action.images_to_save
                ]

            config_data.append(item)

        # Write to file with pretty formatting
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)

        print(f"Successfully saved {len(config_data)} actions to {json_path}")
        return True, f"Saved {len(config_data)} action(s) to config.json"

    except Exception as e:
        error_msg = f"Failed to save config: {str(e)}"
        print(f"ERROR: {error_msg}")
        import traceback
        traceback.print_exc()
        return False, error_msg


def load_config_to_preferences(preferences):
    """
    Loads config.json into addon preferences.

    Args:
        preferences: AddonPreferences object

    Returns:
        tuple: (success: bool, message: str)
    """
    json_path = get_config_path()

    if not json_path.exists():
        return False, f"Config file not found: {json_path}"

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)

        preferences.actions.clear()

        for item in config_data:
            action = preferences.actions.add()

            action.button_name = item.get("button_name", "Unnamed Action")
            action.action_type = item.get("action_type", "CAMERA_SELECT")
            action.select_camera = item.get("select_camera", False)
            action.camera_name = item.get("camera_object_name", "")
            action.change_image_editor = item.get("change_image_editor", False)
            action.image_name_to_view = item.get("image_name_to_view", "")
            action.reset_images = item.get("reset_images", False)
            action.change_node_tree = item.get("change_node_tree", False)
            action.node_tree_name = item.get("node_tree_name", "")
            action.update_timeline = item.get("update_timeline", False)
            action.timeline_frame = item.get("timeline_frame", 0)

            # Handle images to reset
            for img_item in item.get("images_to_reset", []):
                reset_img = action.images_to_reset.add()
                reset_img.name = img_item.get("name", "")

            # Handle images to save
            for img_item in item.get("images_to_save", []):
                save_img = action.images_to_save.add()
                save_img.name = img_item.get("name", "")
                save_img.save_as = img_item.get("save_as", "")
                save_img.allow_overwrite = img_item.get("allow_overwrite", True)

        return True, f"Loaded {len(config_data)} action(s) from config.json"

    except Exception as e:
        return False, f"Failed to load config: {str(e)}"


@bpy.app.handlers.persistent
def load_handler(dummy):
    """Application handler that runs after the scene is loaded/ready."""
    global __initialized_flag

    if __initialized_flag:
        return

    if bpy.context.scene and hasattr(bpy.context.scene, 'my_addon_props'):
        try:
            load_config(bpy.context)
            __initialized_flag = True
        except Exception as e:
            print(f"Post-load config initialization failed: {e}")
            import traceback
            traceback.print_exc()


def delayed_config_load():
    """Load config after Blender is fully initialized."""
    global __initialized_flag

    try:
        if bpy.context and bpy.context.scene and hasattr(bpy.context.scene, 'my_addon_props'):
            if not __initialized_flag:
                load_config(bpy.context)
                __initialized_flag = True
            return None
    except Exception as e:
        print(f"Delayed config load failed: {e}")

    return 0.5

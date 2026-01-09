"""
Utility functions for AI Workflow Config Tools
"""

import bpy
from pathlib import Path


def get_image_editor_space(context):
    """Finds the active space data of the first Image Editor area."""
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                return area.spaces.active
    return None


def replace_with_blank(image_name, width=1024, height=1024, color=(0.0, 0.0, 0.0, 1.0)):
    """Replaces the source of an existing image with a generated blank image."""
    if image_name in bpy.data.images:
        img = bpy.data.images[image_name]

        if img.packed_file:
            img.unpack(method='REMOVE')

        img.source = 'GENERATED'
        img.generated_type = 'BLANK'
        img.generated_width = width
        img.generated_height = height
        img.generated_color = color

        print(f"Success: '{image_name}' is now a blank image.")
    else:
        print(f"Error: Image '{image_name}' not found.")


def get_or_create_camera(name, location=(0, 0, 0)):
    """Gets existing camera or creates a new one if it doesn't exist."""
    if name in bpy.data.objects:
        obj = bpy.data.objects[name]
        if obj.type == 'CAMERA':
            print(f"Using existing camera: '{name}'")
            return obj
        else:
            print(f"Warning: Object '{name}' exists but is not a camera")
            return None

    try:
        camera_data = bpy.data.cameras.new(name=name)
        camera_object = bpy.data.objects.new(name, camera_data)
        bpy.context.scene.collection.objects.link(camera_object)
        camera_object.location = location
        print(f"Created new camera: '{name}' at {location}")
        return camera_object
    except Exception as e:
        print(f"Error creating camera '{name}': {e}")
        return None


def get_or_create_image(name, width=1024, height=1024):
    """Gets existing image or creates a new one if it doesn't exist."""
    if name in bpy.data.images:
        print(f"Using existing image: '{name}'")
        return bpy.data.images[name]

    try:
        img = bpy.data.images.new(name, width, height)
        print(f"Created new image: '{name}' ({width}x{height})")
        return img
    except Exception as e:
        print(f"Error creating image '{name}': {e}")
        return None


def save_image_to_file(image_name, filepath, allow_overwrite=True):
    """Saves an image to disk."""
    if image_name not in bpy.data.images:
        print(f"Error: Image '{image_name}' not found for saving.")
        return False

    img = bpy.data.images[image_name]

    # Check if file exists and overwrite is not allowed
    file_path = Path(filepath)
    if file_path.exists() and not allow_overwrite:
        print(f"Error: File '{filepath}' already exists and overwrite is disabled.")
        return False

    # Create parent directory if it doesn't exist
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating directory '{file_path.parent}': {e}")
        return False

    # Save the image
    try:
        # Store original filepath
        original_filepath = img.filepath

        # Set new filepath and save
        img.filepath_raw = str(file_path)

        # Set file format based on extension
        extension = file_path.suffix.lower()
        format_map = {
            '.png': 'PNG',
            '.jpg': 'JPEG',
            '.jpeg': 'JPEG',
            '.bmp': 'BMP',
            '.tga': 'TARGA',
            '.tif': 'TIFF',
            '.tiff': 'TIFF',
            '.exr': 'OPEN_EXR',
        }
        img.file_format = format_map.get(extension, 'PNG')

        img.save()

        # Restore original filepath to avoid changing the image's internal path
        if original_filepath:
            img.filepath = original_filepath

        print(f"Saved image '{image_name}' to '{filepath}'")
        return True
    except Exception as e:
        print(f"Error saving image '{image_name}' to '{filepath}': {e}")
        return False


def validate_action(action):
    """Validates an action configuration and returns (is_valid, error_message)."""
    if not action.button_name.strip():
        return False, "Button name cannot be empty"

    if action.action_type == 'CAMERA_SELECT':
        if action.select_camera and not action.camera_name.strip():
            return False, "Camera name is required when 'Select Camera' is enabled"

    elif action.action_type == 'RESET':
        if action.reset_images and len(action.images_to_reset) == 0:
            return False, "At least one image must be specified for reset"

    elif action.action_type == 'IMAGE_SAVE':
        if len(action.images_to_save) == 0:
            return False, "At least one image must be specified for saving"
        for img in action.images_to_save:
            if not img.name.strip():
                return False, "Image name cannot be empty"
            if not img.save_as.strip():
                return False, f"Save path for image '{img.name}' cannot be empty"

    return True, ""

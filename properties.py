"""
Property groups for AI Workflow Config Tools
"""

import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    EnumProperty,
    StringProperty,
    BoolProperty,
    IntProperty,
    PointerProperty,
    CollectionProperty,
)


class ResetImageProperty(PropertyGroup):
    """Property group for a single image name to be reset."""
    name: StringProperty(
        name="Image Name",
        description="Name of the Blender Image data-block to reset"
    )


class SaveImageProperty(PropertyGroup):
    """Property group for a single image to save."""
    name: StringProperty(
        name="Image Name",
        description="Name of the Blender Image data-block to save"
    )
    save_as: StringProperty(
        name="Save As",
        description="Full filepath to save the image",
        subtype='FILE_PATH'
    )
    allow_overwrite: BoolProperty(
        name="Allow Overwrite",
        description="Allow overwriting existing files",
        default=True
    )


class ActionProperty(PropertyGroup):
    """A single configured action, simulating one entry from the JSON."""

    action_type: EnumProperty(
        name="Action Type",
        description="Type of action to perform",
        items=[
            ('CAMERA_SELECT', "Camera Select / View", "Selects a camera, changes image and node tree"),
            ('RESET', "Reset Images", "Resets images and optionally changes camera/node tree"),
            ('IMAGE_SAVE', "Save Images", "Saves specified images to disk"),
        ],
        default='CAMERA_SELECT'
    )

    button_name: StringProperty(
        name="Button Name",
        description="Display name for the action button",
        default="New Action"
    )

    # Camera settings
    select_camera: BoolProperty(
        name="Select Camera",
        description="Enable camera selection",
        default=True
    )
    camera_name: StringProperty(
        name="Camera Name",
        description="Name of the camera object to select",
        default=""
    )

    # Image editor settings
    change_image_editor: BoolProperty(
        name="Change Image Editor View",
        description="Switch the image displayed in Image Editor",
        default=False
    )
    image_name_to_view: StringProperty(
        name="Image Name to View",
        description="Name of the image to display",
        default=""
    )

    # Image reset settings
    reset_images: BoolProperty(
        name="Reset Images",
        description="Reset specified images to blank",
        default=False
    )
    images_to_reset: CollectionProperty(
        type=ResetImageProperty,
        name="Images to Reset"
    )

    # Image save settings
    images_to_save: CollectionProperty(
        type=SaveImageProperty,
        name="Images to Save"
    )

    # Node tree settings
    change_node_tree: BoolProperty(
        name="Change Node Tree",
        description="Switch the active node tree",
        default=False
    )
    node_tree_name: StringProperty(
        name="Node Tree Name",
        description="Name of the node tree to activate",
        default="NodeTree"
    )

    # Timeline control
    update_timeline: BoolProperty(
        name="Update Timeline",
        description="Set the current frame",
        default=False
    )
    timeline_frame: IntProperty(
        name="Timeline Frame",
        description="Frame number to set",
        default=0,
        min=0
    )


class MainProperties(PropertyGroup):
    """Main property group attached to the scene, holding all actions."""
    actions: CollectionProperty(
        type=ActionProperty,
        name="Configured Actions"
    )
    active_action_index: IntProperty(
        name="Active Action Index",
        description="Index of the currently selected action",
        default=0
    )
    error_message: StringProperty(
        name="Error Message",
        description="Last error message from config loading",
        default=""
    )
    show_loaded_actions: BoolProperty(
        name="Show Loaded Actions",
        description="Display debug information about loaded actions",
        default=False
    )


# -------------------------------------------------------------------
# REGISTRATION
# -------------------------------------------------------------------

classes = (
    ResetImageProperty,
    SaveImageProperty,
    ActionProperty,
    MainProperties,
)


def register():
    """Register property classes."""
    for cls in classes:
        bpy.utils.register_class(cls)

    # Attach main properties to scene
    bpy.types.Scene.my_addon_props = PointerProperty(type=MainProperties)


def unregister():
    """Unregister property classes."""
    # Remove scene property
    del bpy.types.Scene.my_addon_props

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

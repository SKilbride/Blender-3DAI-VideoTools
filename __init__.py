"""
AI Workflow Config Tools - Blender Add-on
JSON-driven workflow actions for camera, image, node tree, timeline control, and image saving.
"""

import bpy

# -------------------------------------------------------------------
# BLENDER ADD-ON INFO
# -------------------------------------------------------------------

bl_info = {
    "name": "AI Workflow Config Tools",
    "author": "Your Name / Gemini",
    "version": (2, 0, 0),
    "blender": (4, 5, 0),
    "location": "3D View > Sidebar > AI Tools",
    "description": "JSON-driven workflow actions for camera, image, node tree, timeline control, and image saving.",
    "category": "Development",
    "doc_url": "",
    "tracker_url": "",
}

# -------------------------------------------------------------------
# MODULE IMPORTS
# -------------------------------------------------------------------

# Import all modules
from . import (
    utils,
    properties,
    operators,
    ui_lists,
    preferences,
    panels,
    config_manager,
)

# Hot reload support for development
if "bpy" in locals():
    import importlib
    importlib.reload(utils)
    importlib.reload(properties)
    importlib.reload(operators)
    importlib.reload(ui_lists)
    importlib.reload(preferences)
    importlib.reload(panels)
    importlib.reload(config_manager)

# -------------------------------------------------------------------
# REGISTRATION
# -------------------------------------------------------------------

# Module-level initialization flag
__initialized_flag = False

def register():
    """Register all addon classes and properties."""
    # Register in order: properties -> operators -> ui_lists -> preferences -> panels
    properties.register()
    operators.register()
    ui_lists.register()
    preferences.register()
    panels.register()

    # Register handlers
    bpy.app.handlers.load_post.append(config_manager.load_handler)
    bpy.app.timers.register(config_manager.delayed_config_load, first_interval=0.1)

    print("AI Workflow Config Tools registered successfully")


def unregister():
    """Unregister all addon classes and properties."""
    global __initialized_flag

    # Remove handlers
    if config_manager.load_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(config_manager.load_handler)

    if bpy.app.timers.is_registered(config_manager.delayed_config_load):
        bpy.app.timers.unregister(config_manager.delayed_config_load)

    # Unregister in reverse order
    panels.unregister()
    preferences.unregister()
    ui_lists.unregister()
    operators.unregister()
    properties.unregister()

    __initialized_flag = False
    print("AI Workflow Config Tools unregistered successfully")


if __name__ == "__main__":
    register()

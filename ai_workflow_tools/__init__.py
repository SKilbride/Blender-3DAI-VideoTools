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
if "bpy" in locals():
    import importlib
    if "utils" in locals():
        importlib.reload(utils)
    if "properties" in locals():
        importlib.reload(properties)
    if "operators" in locals():
        importlib.reload(operators)
    if "ui_lists" in locals():
        importlib.reload(ui_lists)
    if "preferences" in locals():
        importlib.reload(preferences)
    if "panels" in locals():
        importlib.reload(panels)
    if "config_manager" in locals():
        importlib.reload(config_manager)
else:
    from . import utils
    from . import properties
    from . import operators
    from . import ui_lists
    from . import preferences
    from . import panels
    from . import config_manager

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

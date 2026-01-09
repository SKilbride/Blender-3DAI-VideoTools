"""
UIList classes for AI Workflow Config Tools
"""

import bpy
from bpy.types import UIList


class ActionUIList(UIList):
    """UIList for displaying and managing actions."""
    bl_idname = "AI_WORKFLOW_UL_action_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        """Draw a single item in the list."""
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)

            # Icon based on action type
            icon_map = {
                'CAMERA_SELECT': 'CAMERA_DATA',
                'RESET': 'FILE_REFRESH',
                'IMAGE_SAVE': 'FILE_TICK',
            }
            action_icon = icon_map.get(item.action_type, 'DOT')

            row.prop(item, "button_name", text="", emboss=False, icon=action_icon)

            # Show action type badge
            type_text = {
                'CAMERA_SELECT': "CAM",
                'RESET': "RST",
                'IMAGE_SAVE': "SAVE",
            }.get(item.action_type, "")

            row.label(text=type_text)

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text=item.button_name)


# -------------------------------------------------------------------
# REGISTRATION
# -------------------------------------------------------------------

classes = (
    ActionUIList,
)


def register():
    """Register UIList classes."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister UIList classes."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

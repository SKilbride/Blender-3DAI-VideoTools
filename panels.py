"""
UI panels for AI Workflow Config Tools
"""

import bpy
from bpy.types import Panel


class AIWorkflowPanel(Panel):
    """Main panel in 3D View sidebar."""
    bl_label = "AI Workflow Config"
    bl_idname = "AI_WORKFLOW_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AI Tools"

    def draw(self, context):
        layout = self.layout
        sdn_config = context.scene.my_addon_props

        # Top buttons row
        row = layout.row(align=True)
        row.operator("ai_workflow.reload_config", icon='FILE_REFRESH')

        # Add "Edit Config" button that opens preferences
        op = row.operator(
            "preferences.addon_show",
            text="Edit Config",
            icon='PREFERENCES'
        )
        op.module = __package__

        layout.separator()

        if not sdn_config.actions:
            layout.label(text="No actions loaded.", icon='ERROR')

            if sdn_config.error_message:
                box = layout.box()
                box.label(text="Error Details:", icon='INFO')
                for line in sdn_config.error_message.split('\n'):
                    if line:
                        box.label(text=line)
            else:
                layout.label(text="Check config.json location")
                layout.label(text="or use 'Edit Config' to create")
            return

        # Display buttons for all configured actions
        box = layout.box()
        box.label(text="Actions", icon='PLAY')

        for i, action in enumerate(sdn_config.actions):
            # Icon based on action type
            icon_map = {
                'CAMERA_SELECT': 'CAMERA_DATA',
                'RESET': 'FILE_REFRESH',
                'IMAGE_SAVE': 'FILE_TICK',
            }
            action_icon = icon_map.get(action.action_type, 'PLAY')

            op = box.operator(
                "ai_workflow.execute_action",
                text=action.button_name,
                icon=action_icon
            )
            op.action_index = i

        # Collapsible section for loaded actions (debugging info)
        layout.separator()
        box = layout.box()
        row = box.row()
        row.prop(sdn_config, "show_loaded_actions",
                 icon='TRIA_DOWN' if sdn_config.show_loaded_actions else 'TRIA_RIGHT',
                 icon_only=True, emboss=False)
        row.label(text=f"Loaded Actions ({len(sdn_config.actions)})", icon='SETTINGS')

        # Only show details if expanded
        if sdn_config.show_loaded_actions:
            for action in sdn_config.actions:
                row = box.row()
                row.label(text="", icon='DOT')
                info_text = f"'{action.button_name}' ({action.action_type})"
                if action.update_timeline:
                    info_text += f" [Frame: {action.timeline_frame}]"
                row.label(text=info_text)


# -------------------------------------------------------------------
# REGISTRATION
# -------------------------------------------------------------------

classes = (
    AIWorkflowPanel,
)


def register():
    """Register panel classes."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister panel classes."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

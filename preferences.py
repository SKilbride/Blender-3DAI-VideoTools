"""
Addon preferences panel for AI Workflow Config Tools
"""

import bpy
from bpy.types import AddonPreferences
from bpy.props import CollectionProperty, IntProperty

from .properties import ActionProperty
from . import config_manager


class AIWorkflowPreferences(AddonPreferences):
    """Addon preferences for configuring actions."""
    bl_idname = __package__

    # Collection of actions (same structure as in scene properties)
    actions: CollectionProperty(type=ActionProperty)

    # Active action index for UI selection
    active_action_index: IntProperty(
        name="Active Action",
        description="Currently selected action",
        default=0
    )

    def draw(self, context):
        """Draw the preferences panel."""
        layout = self.layout

        # Header with load/save buttons
        box = layout.box()
        row = box.row(align=True)
        row.label(text="External Config (JSON File):", icon='FILE_FOLDER')
        row.operator("ai_workflow.load_config", text="Load", icon='IMPORT')
        row.operator("ai_workflow.save_config", text="Save", icon='EXPORT')

        # Internal .blend config section
        box = layout.box()
        has_internal = config_manager.has_internal_config()

        row = box.row(align=True)
        if has_internal:
            row.label(text="Internal Config (.blend):", icon='CHECKMARK')
            row.operator("ai_workflow.load_from_internal", text="Reload", icon='FILE_REFRESH')
            row.operator("ai_workflow.delete_internal", text="Delete", icon='X')
        else:
            row.label(text="Internal Config (.blend):", icon='ADD')
            row.operator("ai_workflow.save_to_internal", text="Save to .blend", icon='FILE_TEXT')

        # Show which config is active
        info_row = box.row()
        if has_internal:
            info_row.label(text="✓ Using internal .blend config (project-specific)", icon='INFO')
        else:
            info_row.label(text="ℹ Using external config.json (global)", icon='INFO')

        layout.separator()

        # Actions list section
        box = layout.box()
        box.label(text="Actions", icon='PREFERENCES')

        row = box.row()

        # Left column: Action list with controls
        col = row.column()
        col_row = col.row(align=True)
        col_row.operator("ai_workflow.add_action", text="", icon='ADD')
        col_row.operator("ai_workflow.remove_action", text="", icon='REMOVE')
        col_row.operator("ai_workflow.duplicate_action", text="", icon='DUPLICATE')
        col_row.separator()
        col_row.operator("ai_workflow.move_action", text="", icon='TRIA_UP').direction = 'UP'
        col_row.operator("ai_workflow.move_action", text="", icon='TRIA_DOWN').direction = 'DOWN'

        col.template_list(
            "AI_WORKFLOW_UL_action_list",
            "",
            self,
            "actions",
            self,
            "active_action_index",
            rows=6
        )

        # Right column: Action editor
        if len(self.actions) > 0 and self.active_action_index < len(self.actions):
            action = self.actions[self.active_action_index]

            col = row.column()
            self.draw_action_editor(col, action)
        else:
            col = row.column()
            col.label(text="No action selected", icon='INFO')
            col.label(text="Add an action to get started")

    def draw_action_editor(self, layout, action):
        """Draw the editor for a single action."""
        box = layout.box()
        box.label(text="Edit Action", icon='PREFERENCES')

        # Basic properties
        box.prop(action, "button_name")
        box.prop(action, "action_type")

        box.separator()

        # Action-type specific settings
        if action.action_type == 'CAMERA_SELECT':
            self.draw_camera_settings(box, action)
            box.separator()
            self.draw_image_editor_settings(box, action)
            box.separator()
            self.draw_node_tree_settings(box, action)
            box.separator()
            self.draw_timeline_settings(box, action)

        elif action.action_type == 'RESET':
            self.draw_camera_settings(box, action)
            box.separator()
            self.draw_reset_images_settings(box, action)
            box.separator()
            self.draw_image_editor_settings(box, action)
            box.separator()
            self.draw_node_tree_settings(box, action)
            box.separator()
            self.draw_timeline_settings(box, action)

        elif action.action_type == 'IMAGE_SAVE':
            self.draw_save_images_settings(box, action)

    def draw_camera_settings(self, layout, action):
        """Draw camera settings."""
        box = layout.box()
        row = box.row()
        row.prop(action, "select_camera", text="Select Camera")

        if action.select_camera:
            row = box.row(align=True)
            row.prop(action, "camera_name", text="Camera")
            # Add object picker
            row.prop_search(action, "camera_name", bpy.data, "objects", text="")
            # Add create button
            create_op = row.operator("ai_workflow.create_camera_for_action", text="", icon='ADD')

            # Show warning if camera doesn't exist or is not a camera
            if action.camera_name:
                if action.camera_name not in bpy.data.objects:
                    warning_row = box.row()
                    warning_row.label(text=f"⚠ Camera '{action.camera_name}' doesn't exist", icon='ERROR')
                elif bpy.data.objects[action.camera_name].type != 'CAMERA':
                    warning_row = box.row()
                    warning_row.label(text=f"⚠ '{action.camera_name}' is not a camera", icon='ERROR')

    def draw_image_editor_settings(self, layout, action):
        """Draw image editor settings."""
        box = layout.box()
        row = box.row()
        row.prop(action, "change_image_editor", text="Change Image Editor")

        if action.change_image_editor:
            row = box.row(align=True)
            row.prop(action, "image_name_to_view", text="Image")
            # Add image picker
            row.prop_search(action, "image_name_to_view", bpy.data, "images", text="")
            # Add create button
            create_op = row.operator("ai_workflow.create_image_editor_image", text="", icon='ADD')

            # Show warning if image doesn't exist
            if action.image_name_to_view and action.image_name_to_view not in bpy.data.images:
                warning_row = box.row()
                warning_row.label(text=f"⚠ Image '{action.image_name_to_view}' doesn't exist", icon='ERROR')

    def draw_node_tree_settings(self, layout, action):
        """Draw node tree settings."""
        box = layout.box()
        row = box.row()
        row.prop(action, "change_node_tree", text="Change Node Tree")

        if action.change_node_tree:
            row = box.row()
            row.prop(action, "node_tree_name", text="Node Tree")
            # Add node group picker
            row.prop_search(action, "node_tree_name", bpy.data, "node_groups", text="")

    def draw_timeline_settings(self, layout, action):
        """Draw timeline settings."""
        box = layout.box()
        row = box.row()
        row.prop(action, "update_timeline", text="Update Timeline")

        if action.update_timeline:
            row = box.row()
            row.prop(action, "timeline_frame", text="Frame")

    def draw_reset_images_settings(self, layout, action):
        """Draw reset images settings."""
        box = layout.box()
        row = box.row()
        row.prop(action, "reset_images", text="Reset Images")

        if action.reset_images:
            col = box.column(align=True)

            for idx, img in enumerate(action.images_to_reset):
                row = col.row(align=True)
                row.prop(img, "name", text="")
                row.prop_search(img, "name", bpy.data, "images", text="")

                # Add create button
                create_op = row.operator("ai_workflow.create_reset_image", text="", icon='ADD')
                create_op.index = idx

                # Remove button
                remove_op = row.operator("ai_workflow.remove_reset_image", text="", icon='X')
                remove_op.index = idx

                # Show warning if image doesn't exist
                if img.name and img.name not in bpy.data.images:
                    warning_row = col.row()
                    warning_row.label(text=f"  ⚠ '{img.name}' doesn't exist", icon='ERROR')

            row = col.row()
            row.operator("ai_workflow.add_reset_image", text="Add Image", icon='ADD')

    def draw_save_images_settings(self, layout, action):
        """Draw save images settings."""
        box = layout.box()
        box.label(text="Images to Save", icon='FILE_TICK')

        col = box.column(align=True)

        for idx, img in enumerate(action.images_to_save):
            sub_box = col.box()
            row = sub_box.row(align=True)
            row.label(text=f"Image {idx + 1}:", icon='IMAGE_DATA')
            remove_op = row.operator("ai_workflow.remove_save_image", text="", icon='X')
            remove_op.index = idx

            row = sub_box.row(align=True)
            row.prop(img, "name", text="Image Name")
            row.prop_search(img, "name", bpy.data, "images", text="")

            # Add create button
            create_op = row.operator("ai_workflow.create_save_image", text="", icon='ADD')
            create_op.index = idx

            # Show warning if image doesn't exist
            if img.name and img.name not in bpy.data.images:
                warning_row = sub_box.row()
                warning_row.label(text=f"⚠ Image '{img.name}' doesn't exist", icon='ERROR')

            sub_box.prop(img, "save_as", text="Save Path")
            sub_box.prop(img, "allow_overwrite", text="Allow Overwrite")

        row = col.row()
        row.operator("ai_workflow.add_save_image", text="Add Image", icon='ADD')


# -------------------------------------------------------------------
# REGISTRATION
# -------------------------------------------------------------------

classes = (
    AIWorkflowPreferences,
)


def register():
    """Register preferences classes."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister preferences classes."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

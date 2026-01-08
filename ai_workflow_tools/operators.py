"""
Operators for AI Workflow Config Tools
"""

import bpy
from bpy.types import Operator
from bpy.props import IntProperty, StringProperty, BoolProperty

from . import utils
from . import config_manager


class ExecuteActionOperator(Operator):
    """Executes a configured action by changing scene state."""
    bl_idname = "ai_workflow.execute_action"
    bl_label = "Execute Configured Action"
    bl_description = "Executes an action defined by the custom configuration"
    bl_options = {'INTERNAL'}

    action_index: IntProperty(name="Action Index")

    def execute(self, context):
        sdn_config = context.scene.my_addon_props
        if self.action_index >= len(sdn_config.actions):
            self.report({'ERROR'}, "Invalid action index.")
            return {'CANCELLED'}

        action = sdn_config.actions[self.action_index]
        self.report({'INFO'}, f"Executing Action: '{action.button_name}'")

        # --- 1. Handle Camera Selection (Create if doesn't exist) ---
        if action.select_camera and action.camera_name:
            cam_obj = utils.get_or_create_camera(action.camera_name)

            if cam_obj and cam_obj.type == 'CAMERA':
                context.scene.camera = cam_obj
                print(f"Action: Set active camera to {cam_obj.name}")
            elif cam_obj:
                self.report({'WARNING'}, f"Object '{action.camera_name}' is not a camera.")
            else:
                self.report({'ERROR'}, f"Failed to get or create camera '{action.camera_name}'.")

        # --- 2. Handle Node Tree Change (for ComfyUI Node Editor) ---
        if action.change_node_tree and action.node_tree_name:
            node_tree_exists = action.node_tree_name in bpy.data.node_groups

            if not node_tree_exists:
                self.report({'WARNING'}, f"Node Group '{action.node_tree_name}' not found at execution time.")
                print(f"Available node groups: {[ng.name for ng in bpy.data.node_groups]}")
            else:
                # Method 1: Set the sdn.comfyui_tree property
                if hasattr(context.scene, 'sdn') and hasattr(context.scene.sdn, 'comfyui_tree'):
                    try:
                        old_tree = context.scene.sdn.comfyui_tree
                        context.scene.sdn.comfyui_tree = action.node_tree_name
                        print(f"Action: Set sdn.comfyui_tree: '{old_tree}' → '{action.node_tree_name}'")
                    except Exception as e:
                        print(f"Warning: Failed to set sdn.comfyui_tree: {e}")

                # Method 2: Directly change the node tree in the Node Editor space
                node_editor_found = False
                for window in context.window_manager.windows:
                    for area in window.screen.areas:
                        if area.type == 'NODE_EDITOR':
                            try:
                                space = area.spaces.active
                                old_tree_name = space.node_tree.name if space.node_tree else "None"
                                space.node_tree = bpy.data.node_groups[action.node_tree_name]
                                new_tree_name = space.node_tree.name if space.node_tree else "None"
                                print(f"Action: ✓ Changed Node Editor: '{old_tree_name}' → '{new_tree_name}'")
                                area.tag_redraw()
                                node_editor_found = True
                            except Exception as e:
                                print(f"Warning: Failed to update Node Editor: {e}")

                if not node_editor_found:
                    print("Action: Node tree property set, but no Node Editor visible to update.")

        # --- 3. Handle Image Reset (RESET type - Create if doesn't exist) ---
        if action.action_type == 'RESET' and action.reset_images:
            for item in action.images_to_reset:
                img = utils.get_or_create_image(item.name)
                if img:
                    utils.replace_with_blank(item.name)
            print("Action: Completed image reset.")

        # --- 4. Handle Image Save (IMAGE_SAVE type) ---
        if action.action_type == 'IMAGE_SAVE':
            saved_count = 0
            failed_count = 0

            for item in action.images_to_save:
                if utils.save_image_to_file(item.name, item.save_as, item.allow_overwrite):
                    saved_count += 1
                else:
                    failed_count += 1

            if saved_count > 0:
                self.report({'INFO'}, f"Saved {saved_count} image(s)")
                print(f"Action: Saved {saved_count} image(s)")
            if failed_count > 0:
                self.report({'WARNING'}, f"Failed to save {failed_count} image(s)")
                print(f"Action: Failed to save {failed_count} image(s)")

        # --- 5. Handle Image Editor Display Change (Create if doesn't exist) ---
        if action.change_image_editor and action.image_name_to_view:
            img = utils.get_or_create_image(action.image_name_to_view)

            if img:
                img_space = utils.get_image_editor_space(context)
                if img_space:
                    try:
                        img_space.image = img
                        print(f"Action: Set Image Editor to '{action.image_name_to_view}'")

                        # Reset zoom to 1:1
                        try:
                            img_space.zoom = (1.0, 1.0)
                            img_space.cursor_location = (0.5, 0.5)
                            print(f"Action: Reset zoom for '{action.image_name_to_view}'")
                        except Exception as e:
                            print(f"Note: Could not reset zoom (not critical): {e}")

                    except Exception as e:
                        print(f"Warning: Failed to update Image Editor: {e}")
                else:
                    self.report({'WARNING'}, "No Image Editor Area found to change the view.")
            else:
                self.report({'ERROR'}, f"Failed to get or create image '{action.image_name_to_view}'.")

        # --- 6. Handle Timeline Update ---
        if action.update_timeline:
            try:
                frame_start = context.scene.frame_start
                frame_end = context.scene.frame_end
                target_frame = action.timeline_frame

                # Clamp to valid range
                if target_frame < frame_start:
                    self.report({'WARNING'}, f"Frame {target_frame} is before timeline start ({frame_start}). Setting to start.")
                    target_frame = frame_start
                elif target_frame > frame_end:
                    self.report({'WARNING'}, f"Frame {target_frame} is after timeline end ({frame_end}). Setting to end.")
                    target_frame = frame_end

                old_frame = context.scene.frame_current
                context.scene.frame_set(target_frame)
                print(f"Action: ✓ Changed timeline frame: {old_frame} → {target_frame}")
            except Exception as e:
                print(f"Warning: Failed to update timeline: {e}")

        return {'FINISHED'}


class ReloadConfigOperator(Operator):
    """Manually reload the config.json file."""
    bl_idname = "ai_workflow.reload_config"
    bl_label = "Reload Config"
    bl_description = "Reload configuration from config.json"

    def execute(self, context):
        config_manager.load_config(context)
        self.report({'INFO'}, "Config reloaded")
        return {'FINISHED'}


class AddActionOperator(Operator):
    """Add a new action to the configuration."""
    bl_idname = "ai_workflow.add_action"
    bl_label = "Add Action"
    bl_description = "Add a new action to the configuration"

    def execute(self, context):
        preferences = context.preferences.addons[__package__].preferences
        new_action = preferences.actions.add()
        new_action.button_name = "New Action"
        preferences.active_action_index = len(preferences.actions) - 1
        self.report({'INFO'}, "Added new action")
        return {'FINISHED'}


class RemoveActionOperator(Operator):
    """Remove the selected action from the configuration."""
    bl_idname = "ai_workflow.remove_action"
    bl_label = "Remove Action"
    bl_description = "Remove the selected action from the configuration"

    @classmethod
    def poll(cls, context):
        preferences = context.preferences.addons[__package__].preferences
        return len(preferences.actions) > 0

    def execute(self, context):
        preferences = context.preferences.addons[__package__].preferences
        if preferences.active_action_index < len(preferences.actions):
            preferences.actions.remove(preferences.active_action_index)
            preferences.active_action_index = min(
                preferences.active_action_index,
                len(preferences.actions) - 1
            )
            self.report({'INFO'}, "Removed action")
        return {'FINISHED'}


class MoveActionOperator(Operator):
    """Move an action up or down in the list."""
    bl_idname = "ai_workflow.move_action"
    bl_label = "Move Action"
    bl_description = "Move the selected action up or down"

    direction: StringProperty(default="UP")

    @classmethod
    def poll(cls, context):
        preferences = context.preferences.addons[__package__].preferences
        return len(preferences.actions) > 1

    def execute(self, context):
        preferences = context.preferences.addons[__package__].preferences
        index = preferences.active_action_index

        if self.direction == "UP" and index > 0:
            preferences.actions.move(index, index - 1)
            preferences.active_action_index = index - 1
        elif self.direction == "DOWN" and index < len(preferences.actions) - 1:
            preferences.actions.move(index, index + 1)
            preferences.active_action_index = index + 1

        return {'FINISHED'}


class DuplicateActionOperator(Operator):
    """Duplicate the selected action."""
    bl_idname = "ai_workflow.duplicate_action"
    bl_label = "Duplicate Action"
    bl_description = "Duplicate the selected action"

    @classmethod
    def poll(cls, context):
        preferences = context.preferences.addons[__package__].preferences
        return len(preferences.actions) > 0

    def execute(self, context):
        preferences = context.preferences.addons[__package__].preferences
        index = preferences.active_action_index

        if index < len(preferences.actions):
            source = preferences.actions[index]
            new_action = preferences.actions.add()

            # Copy all properties
            new_action.button_name = source.button_name + " (Copy)"
            new_action.action_type = source.action_type
            new_action.select_camera = source.select_camera
            new_action.camera_name = source.camera_name
            new_action.change_image_editor = source.change_image_editor
            new_action.image_name_to_view = source.image_name_to_view
            new_action.reset_images = source.reset_images
            new_action.change_node_tree = source.change_node_tree
            new_action.node_tree_name = source.node_tree_name
            new_action.update_timeline = source.update_timeline
            new_action.timeline_frame = source.timeline_frame

            # Copy images to reset
            for reset_img in source.images_to_reset:
                new_reset = new_action.images_to_reset.add()
                new_reset.name = reset_img.name

            # Copy images to save
            for save_img in source.images_to_save:
                new_save = new_action.images_to_save.add()
                new_save.name = save_img.name
                new_save.save_as = save_img.save_as
                new_save.allow_overwrite = save_img.allow_overwrite

            preferences.active_action_index = len(preferences.actions) - 1
            self.report({'INFO'}, "Duplicated action")

        return {'FINISHED'}


class SaveConfigOperator(Operator):
    """Save the current configuration to config.json."""
    bl_idname = "ai_workflow.save_config"
    bl_label = "Save Config"
    bl_description = "Save the current configuration to config.json"

    def execute(self, context):
        preferences = context.preferences.addons[__package__].preferences
        success, message = config_manager.save_config(preferences.actions)

        if success:
            self.report({'INFO'}, message)
            # Reload the config into the scene
            config_manager.load_config(context)
        else:
            self.report({'ERROR'}, message)

        return {'FINISHED'}


class LoadConfigOperator(Operator):
    """Load configuration from config.json into preferences."""
    bl_idname = "ai_workflow.load_config"
    bl_label = "Load Config"
    bl_description = "Load configuration from config.json"

    def execute(self, context):
        preferences = context.preferences.addons[__package__].preferences
        success, message = config_manager.load_config_to_preferences(preferences)

        if success:
            self.report({'INFO'}, message)
        else:
            self.report({'ERROR'}, message)

        return {'FINISHED'}


class AddResetImageOperator(Operator):
    """Add an image to the reset list."""
    bl_idname = "ai_workflow.add_reset_image"
    bl_label = "Add Image"
    bl_description = "Add an image to the reset list"

    def execute(self, context):
        preferences = context.preferences.addons[__package__].preferences
        if preferences.active_action_index < len(preferences.actions):
            action = preferences.actions[preferences.active_action_index]
            new_img = action.images_to_reset.add()
            new_img.name = "ImageName"
            self.report({'INFO'}, "Added reset image")
        return {'FINISHED'}


class RemoveResetImageOperator(Operator):
    """Remove an image from the reset list."""
    bl_idname = "ai_workflow.remove_reset_image"
    bl_label = "Remove Image"
    bl_description = "Remove an image from the reset list"

    index: IntProperty()

    def execute(self, context):
        preferences = context.preferences.addons[__package__].preferences
        if preferences.active_action_index < len(preferences.actions):
            action = preferences.actions[preferences.active_action_index]
            if self.index < len(action.images_to_reset):
                action.images_to_reset.remove(self.index)
                self.report({'INFO'}, "Removed reset image")
        return {'FINISHED'}


class AddSaveImageOperator(Operator):
    """Add an image to the save list."""
    bl_idname = "ai_workflow.add_save_image"
    bl_label = "Add Image"
    bl_description = "Add an image to the save list"

    def execute(self, context):
        preferences = context.preferences.addons[__package__].preferences
        if preferences.active_action_index < len(preferences.actions):
            action = preferences.actions[preferences.active_action_index]
            new_img = action.images_to_save.add()
            new_img.name = "ImageName"
            new_img.save_as = "//output.png"
            self.report({'INFO'}, "Added save image")
        return {'FINISHED'}


class RemoveSaveImageOperator(Operator):
    """Remove an image from the save list."""
    bl_idname = "ai_workflow.remove_save_image"
    bl_label = "Remove Image"
    bl_description = "Remove an image from the save list"

    index: IntProperty()

    def execute(self, context):
        preferences = context.preferences.addons[__package__].preferences
        if preferences.active_action_index < len(preferences.actions):
            action = preferences.actions[preferences.active_action_index]
            if self.index < len(action.images_to_save):
                action.images_to_save.remove(self.index)
                self.report({'INFO'}, "Removed save image")
        return {'FINISHED'}


class CreateImageOperator(Operator):
    """Create a new image if it doesn't exist."""
    bl_idname = "ai_workflow.create_image"
    bl_label = "Create Image"
    bl_description = "Create a new blank image with the specified name"

    image_name: StringProperty(name="Image Name")
    width: IntProperty(name="Width", default=1920, min=1, max=65536)
    height: IntProperty(name="Height", default=1080, min=1, max=65536)

    def invoke(self, context, event):
        """Show dialog for image dimensions."""
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        """Draw the dialog."""
        layout = self.layout
        layout.label(text=f"Create: {self.image_name}")
        layout.prop(self, "width")
        layout.prop(self, "height")

    def execute(self, context):
        if not self.image_name.strip():
            self.report({'ERROR'}, "Image name cannot be empty")
            return {'CANCELLED'}

        if self.image_name in bpy.data.images:
            self.report({'INFO'}, f"Image '{self.image_name}' already exists")
            return {'FINISHED'}

        try:
            img = bpy.data.images.new(self.image_name, self.width, self.height)
            self.report({'INFO'}, f"Created image '{self.image_name}' ({self.width}x{self.height})")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to create image: {str(e)}")
            return {'CANCELLED'}


class CreateImageEditorImageOperator(Operator):
    """Create the image for Image Editor view."""
    bl_idname = "ai_workflow.create_image_editor_image"
    bl_label = "Create Image"
    bl_description = "Create the image specified for Image Editor view"

    def execute(self, context):
        preferences = context.preferences.addons[__package__].preferences
        if preferences.active_action_index < len(preferences.actions):
            action = preferences.actions[preferences.active_action_index]
            if action.image_name_to_view.strip():
                bpy.ops.ai_workflow.create_image(
                    'INVOKE_DEFAULT',
                    image_name=action.image_name_to_view
                )
            else:
                self.report({'ERROR'}, "Image name is empty")
                return {'CANCELLED'}
        return {'FINISHED'}


class CreateResetImageOperator(Operator):
    """Create an image from the reset list."""
    bl_idname = "ai_workflow.create_reset_image"
    bl_label = "Create Image"
    bl_description = "Create the specified reset image"

    index: IntProperty()

    def execute(self, context):
        preferences = context.preferences.addons[__package__].preferences
        if preferences.active_action_index < len(preferences.actions):
            action = preferences.actions[preferences.active_action_index]
            if self.index < len(action.images_to_reset):
                img_item = action.images_to_reset[self.index]
                if img_item.name.strip():
                    bpy.ops.ai_workflow.create_image(
                        'INVOKE_DEFAULT',
                        image_name=img_item.name
                    )
                else:
                    self.report({'ERROR'}, "Image name is empty")
                    return {'CANCELLED'}
        return {'FINISHED'}


class CreateSaveImageOperator(Operator):
    """Create an image from the save list."""
    bl_idname = "ai_workflow.create_save_image"
    bl_label = "Create Image"
    bl_description = "Create the specified save image"

    index: IntProperty()

    def execute(self, context):
        preferences = context.preferences.addons[__package__].preferences
        if preferences.active_action_index < len(preferences.actions):
            action = preferences.actions[preferences.active_action_index]
            if self.index < len(action.images_to_save):
                img_item = action.images_to_save[self.index]
                if img_item.name.strip():
                    bpy.ops.ai_workflow.create_image(
                        'INVOKE_DEFAULT',
                        image_name=img_item.name
                    )
                else:
                    self.report({'ERROR'}, "Image name is empty")
                    return {'CANCELLED'}
        return {'FINISHED'}


# -------------------------------------------------------------------
# REGISTRATION
# -------------------------------------------------------------------

classes = (
    ExecuteActionOperator,
    ReloadConfigOperator,
    AddActionOperator,
    RemoveActionOperator,
    MoveActionOperator,
    DuplicateActionOperator,
    SaveConfigOperator,
    LoadConfigOperator,
    AddResetImageOperator,
    RemoveResetImageOperator,
    AddSaveImageOperator,
    RemoveSaveImageOperator,
    CreateImageOperator,
    CreateImageEditorImageOperator,
    CreateResetImageOperator,
    CreateSaveImageOperator,
)


def register():
    """Register operator classes."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister operator classes."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

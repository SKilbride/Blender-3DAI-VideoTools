import bpy
import json
from pathlib import Path

# --- CORE BLENDER IMPORTS ---
from bpy.types import Operator, Panel, PropertyGroup 
from bpy.props import (
    EnumProperty,
    StringProperty,
    BoolProperty,
    IntProperty,
    PointerProperty,
    CollectionProperty,
)

# -------------------------------------------------------------------
# 0. BLENDER ADD-ON INFO
# -------------------------------------------------------------------

bl_info = {
    "name": "AI Workflow Config Tools",
    "author": "Your Name / Gemini",
    "version": (1, 4, 0),
    "blender": (4, 5, 0),
    "location": "3D View > Sidebar > AI Tools",
    "description": "JSON-driven workflow actions for camera, image, node tree, timeline control, and image saving.",
    "category": "Development",
}

# Use a module-level flag to ensure configuration runs only once
__initialized_flag = False

# -------------------------------------------------------------------
# 1. HELPER UTILITY FUNCTIONS
# -------------------------------------------------------------------

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
        img.file_format = file_path.suffix[1:].upper()  # PNG, JPG, etc.
        img.save()
        
        # Restore original filepath to avoid changing the image's internal path
        img.filepath = original_filepath
        
        print(f"Saved image '{image_name}' to '{filepath}'")
        return True
    except Exception as e:
        print(f"Error saving image '{image_name}' to '{filepath}': {e}")
        return False

# -------------------------------------------------------------------
# 2. PROPERTY GROUPS (The data structure that holds the JSON info)
# -------------------------------------------------------------------

class MY_PG_ResetImage(PropertyGroup):
    """Property group for a single image name to be reset."""
    name: StringProperty(name="Image Name", description="Name of the Blender Image data-block to reset.")

class MY_PG_SaveImage(PropertyGroup):
    """Property group for a single image to save."""
    name: StringProperty(name="Image Name", description="Name of the Blender Image data-block to save.")
    save_as: StringProperty(name="Save As", description="Full filepath to save the image.")
    allow_overwrite: BoolProperty(name="Allow Overwrite", default=True)

class MY_PG_Action(PropertyGroup):
    """A single configured action, simulating one entry from the JSON."""
    
    action_type: EnumProperty(
        name="Action Type",
        items=[
            ('CAMERA_SELECT', "Camera Select / View", "Selects a camera, changes image and node tree."),
            ('RESET', "Reset Images", "Resets images and optionally changes camera/node tree."),
            ('IMAGE_SAVE', "Save Images", "Saves specified images to disk."),
        ],
        default='CAMERA_SELECT'
    )
    
    button_name: StringProperty(name="Button Name", default="New Action")

    # Camera settings
    select_camera: BoolProperty(name="Select Camera", default=True)
    camera_name: StringProperty(name="Camera Name", default="")

    # Image editor settings
    change_image_editor: BoolProperty(name="Change Image Editor View", default=False)
    image_name_to_view: StringProperty(name="Image Name to View", default="")

    # Image reset settings
    reset_images: BoolProperty(name="Reset Images", default=False)
    images_to_reset: CollectionProperty(type=MY_PG_ResetImage, name="Images to Reset")
    
    # Image save settings
    images_to_save: CollectionProperty(type=MY_PG_SaveImage, name="Images to Save")

    # Node tree settings
    change_node_tree: BoolProperty(name="Change Node Tree", default=False)
    node_tree_name: StringProperty(name="Node Tree Name", default="NodeTree")
    
    # Timeline control
    update_timeline: BoolProperty(name="Update Timeline", default=False)
    timeline_frame: IntProperty(name="Timeline Frame", default=0, min=0)


class MY_PG_MainProperties(PropertyGroup):
    """Main property group attached to the scene, holding all actions."""
    actions: CollectionProperty(type=MY_PG_Action, name="Configured Actions")
    error_message: StringProperty(name="Error Message", default="")
    show_loaded_actions: BoolProperty(name="Show Loaded Actions", default=False)

# -------------------------------------------------------------------
# 3. OPERATOR (The Logic Executor)
# -------------------------------------------------------------------

class MY_ACTION_OT_execute_json_action(Operator):
    """Executes a configured action by changing scene state."""
    bl_idname = "mynew.execute_action"
    bl_label = "Execute Configured Action"
    bl_description = "Executes an action defined by the custom configuration."
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
            cam_obj = get_or_create_camera(action.camera_name)
            
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
                img = get_or_create_image(item.name)
                if img:
                    replace_with_blank(item.name)
            print("Action: Completed image reset.")
        
        # --- 4. Handle Image Save (IMAGE_SAVE type) ---
        if action.action_type == 'IMAGE_SAVE':
            saved_count = 0
            failed_count = 0
            
            for item in action.images_to_save:
                if save_image_to_file(item.name, item.save_as, item.allow_overwrite):
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
            img = get_or_create_image(action.image_name_to_view)
            
            if img:
                img_space = get_image_editor_space(context)
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


class MY_ACTION_OT_reload_config(Operator):
    """Manually reload the config.json file."""
    bl_idname = "mynew.reload_config"
    bl_label = "Reload Config"
    bl_description = "Reload configuration from config.json"

    def execute(self, context):
        load_config(context)
        self.report({'INFO'}, "Config reloaded")
        return {'FINISHED'}

# -------------------------------------------------------------------
# 4. UI PANEL (Displays Buttons based on Data Structure)
# -------------------------------------------------------------------

class MY_PANEL_PT_json_driven_panel(Panel):
    bl_label = "AI Workflow Config"
    bl_idname = "MY_PANEL_PT_json_driven_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AI Tools"

    def draw(self, context):
        layout = self.layout
        sdn_config = context.scene.my_addon_props
        
        # Add reload button at the top
        layout.operator(MY_ACTION_OT_reload_config.bl_idname, icon='FILE_REFRESH')
        
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
            return
            
        # Display buttons for all configured actions
        for i, action in enumerate(sdn_config.actions):
            op = layout.operator(
                MY_ACTION_OT_execute_json_action.bl_idname, 
                text=action.button_name, 
                icon='PLAY'
            )
            op.action_index = i

        # Collapsible section for loaded actions (debugging info)
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
                row.label(text="", icon='DOT')  # Indent with bullet
                info_text = f"'{action.button_name}' ({action.action_type})"
                if action.update_timeline:
                    info_text += f" [Frame: {action.timeline_frame}]"
                row.label(text=info_text)

# -------------------------------------------------------------------
# 5. CONFIG LOADER, HANDLERS, AND REGISTRATION
# -------------------------------------------------------------------

def load_config(context):
    """Loads action configuration from a physical 'config.json' file."""
    
    addon_dir = Path(__file__).parent
    json_path = addon_dir / "config.json"
    
    scene = context.scene
    props = scene.my_addon_props
    
    props.actions.clear()
    props.error_message = ""
    
    print(f"=== AI Workflow Config Loader ===")
    print(f"Add-on directory: {addon_dir}")
    print(f"Looking for config at: {json_path}")
    print(f"Config exists: {json_path.exists()}")
    
    if not json_path.exists():
        error_msg = f"Config not found at:\n{json_path}"
        props.error_message = error_msg
        print(f"ERROR: {error_msg}")
        return

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        print(f"Loaded JSON with {len(config_data)} entries")
            
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

        print(f"Successfully loaded {len(props.actions)} actions from config.json")
        print("=================================")
        
    except Exception as e:
        error_msg = f"Error loading config:\n{str(e)}"
        props.error_message = error_msg
        print(f"ERROR: {error_msg}")
        import traceback
        traceback.print_exc()


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
    except:
        pass
    
    return 0.5


classes = (
    MY_PG_ResetImage,
    MY_PG_SaveImage,
    MY_PG_Action,
    MY_PG_MainProperties,
    MY_ACTION_OT_execute_json_action,
    MY_ACTION_OT_reload_config,
    MY_PANEL_PT_json_driven_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.my_addon_props = PointerProperty(type=MY_PG_MainProperties)
    bpy.app.handlers.load_post.append(load_handler)
    bpy.app.timers.register(delayed_config_load, first_interval=0.1)


def unregister():
    global __initialized_flag
    
    if load_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_handler)
    
    if bpy.app.timers.is_registered(delayed_config_load):
        bpy.app.timers.unregister(delayed_config_load)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.my_addon_props
    __initialized_flag = False

if __name__ == "__main__":
    register()
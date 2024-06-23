bl_info = {
    "name": "Vector Animation",
    "author": "FlipThoseTitle",
    "version": (1, 1),
    "blender": (2, 28, 0),
    "location": "View3D > N",
    "description": "Addons for Vector Animation",
    "category": "",
}

import bpy
import os
import mathutils

# limbs order
NODEPOINT_ORDER = [
    "NHip_1", "NHip_2", "NStomach", "NChest", "NNeck", "NShoulder_1", "NShoulder_2",
    "NKnee_1", "NKnee_2", "NAnkle_1", "NAnkle_2", "NToe_1", "NHeel_1", "NToeTip_1", 
    "NToeS_1", "NHeel_2", "NToe_2", "NToeTip_2", "NToeS_2", "NElbow_1", "NElbow_2",
    "NWrist_1", "NWrist_2", "NKnuckles_1", "NFingertips_1", "NKnucklesS_1", "NKnuckles_2", 
    "NFingertips_2", "NKnucklesS_2", "NHead", "NTop", "NChestS_1", "NChestS_2", 
    "NStomachS_1", "NStomachS_2", "NChestF", "NStomachF", "NPelvisF", "NHeadS_1",
    "NHeadS_2", "NHeadF", "NPivot", "DetectorH", "DetectorV", "COM", "Camera"
]

# export node point positions to .bindec file
def export_bindec(filepath):
    scene = bpy.context.scene
    start_frame = scene.frame_start
    end_frame = scene.frame_end

    lines = []

    # Iterate through each frame
    for frame in range(start_frame, end_frame + 1):
        scene.frame_set(frame)
        positions = []

        for name in NODEPOINT_ORDER:
            obj = bpy.data.objects.get(name)
            if obj:
                pos = obj.matrix_world.translation
                x = pos.x
                z = pos.y
                y = -pos.z  # flip the y
                positions.append(f"{x:.8f},{y:.8f},{z:.8f}")
            else:
                positions.append("0,0,0")

        line = f"[46]{{{'}{'.join(positions)}}}END"
        lines.append(line)

    with open(filepath, 'w') as file:
        file.write(f"Binary blocks count: {len(lines)}\n")
        for line in lines:
            file.write(f"{line}\n")

# import .bindec file
def import_bindec(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    # get number of binary blocks from the first line
    if lines[0].startswith("Binary blocks count:"):
        binary_blocks_count = int(lines[0].split(":")[1].strip())
    else:
        return {'CANCELLED'}

    scene = bpy.context.scene

    # Iterate through each line in the file
    frame_index = 1  # start after the first line
    for frame in range(scene.frame_start, scene.frame_start + binary_blocks_count):
        line = lines[frame_index].strip()
        frame_index += 1

        if line.startswith("[46]{") and line.endswith("}END"):
            line = line.replace("[46]{", "").replace("}END", "")
            positions_str = line.split("}{")
            positions = [p.split(",") for p in positions_str]

            if len(positions) != len(NODEPOINT_ORDER):
                continue

            # move node points directly
            for i, name in enumerate(NODEPOINT_ORDER):
                obj = bpy.data.objects.get(name)
                if obj:
                    
                    # transform coordinates to be correct
                    x = float(positions[i][0])
                    z = -float(positions[i][1])
                    y = float(positions[i][2])

                    pos = (x, y, z)
                    obj.location = pos

                    obj.keyframe_insert(data_path="location", frame=frame)

    scene.frame_end = scene.frame_start + binary_blocks_count
    scene.frame_set(scene.frame_start)

# Operator to export node point positions
class ExportBindecOperator(bpy.types.Operator):
    bl_idname = "export.bindec"
    bl_label = "Export Bindec"
    bl_description = "Export the positions of node points in every frames to a .bindec file"

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Filepath used for exporting the .bindec file",
        subtype="FILE_PATH"
    )

    def execute(self, context):
        if not self.filepath.endswith(".bindec"):
            self.filepath += ".bindec"
        export_bindec(self.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        scene_name = bpy.path.basename(bpy.context.blend_data.filepath)
        scene_name = os.path.splitext(scene_name)[0]
        
        #   default file path
        self.filepath = bpy.path.abspath("//") + scene_name + ".bindec"
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Operator to import node point positions
class ImportBindecOperator(bpy.types.Operator):
    bl_idname = "import.bindec"
    bl_label = "Import Bindec"
    bl_description = "Import positions of node points from a .bindec file"

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Filepath used for importing the .bindec file",
        subtype="FILE_PATH"
    )

    def execute(self, context):
        import_bindec(self.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        # Set the default file path
        self.filepath = bpy.path.abspath("//")  # Start with current blend file directory
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

# sideview panel menu
class VIEW3D_PT_bindec_export_panel(bpy.types.Panel):
    bl_label = "Vector Animation"
    bl_idname = "VIEW3D_PT_bindec_export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Vector Animation'

    def draw(self, context):
        layout = self.layout
        layout.operator(ExportBindecOperator.bl_idname, icon='ARMATURE_DATA')
        layout.operator(ImportBindecOperator.bl_idname, icon='OUTLINER_OB_ARMATURE')

def register():
    bpy.utils.register_class(ExportBindecOperator)
    bpy.utils.register_class(ImportBindecOperator)
    bpy.utils.register_class(VIEW3D_PT_bindec_export_panel)

def unregister():
    bpy.utils.unregister_class(ExportBindecOperator)
    bpy.utils.unregister_class(ImportBindecOperator)
    bpy.utils.unregister_class(VIEW3D_PT_bindec_export_panel)

if __name__ == "__main__":
    register()

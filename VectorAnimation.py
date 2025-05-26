bl_info = {
    "name": "Vector Animation",
    "author": "FlipThoseTitle",
    "version": (1, 3),
    "blender": (2, 28, 0),
    "location": "View3D > N",
    "description": "Addons for Vector Animation",
    "category": "",
}

import bpy
import os
import mathutils
import xml.etree.ElementTree as ET

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

# limbs order for SF2
NODEPOINT_ORDER_SF2 = [
    "NTop", "NNeck", "NShoulder_2", "NShoulder_1", "NElbow_2", "NElbow_1", "NWrist_2", "NWrist_1",
    "NFingertipsSS_2", "NFingertipsSS_1", "NHip_2", "NHip_1", "NKnee_2", "NKnee_1", "NAnkle_2", 
    "NAnkle_1", "NToe_2", "NToe_1", "NPivot", "Weapon-Node1_1", "Weapon-Node2_1", "Weapon-Node3_1", 
    "Weapon-Node4_1", "Weapon-Node1_2", "Weapon-Node2_2", "Weapon-Node3_2", "Weapon-Node4_2", 
    "NStomach", "NChest", "NToeTip_2", "NHeel_2", "NHeel_1", "NToeS_2", "NToeTip_1", "NToeS_1", 
    "NKnuckles_2", "NKnucklesS_2", "NKnuckles_1", "NKnucklesS_1", "NFingertips_2", "NFingertips_1", 
    "NFingertipsS_2", "NFingertipsS_1", "NHead", "NChestS_2", "NChestS_1", "NStomachS_2", 
    "NStomachS_1", "NChestF", "NStomachF", "NPelvisF", "NHeadS_2", "NHeadS_1", "NHeadF", "COM", 
    "MacroNode1_2", "MacroNode2_2", "MacroNode3_2", "MacroNode4_2", "MacroNode5_2", "MacroNode6_2", 
    "MacroNode1_1", "MacroNode2_1", "MacroNode3_1", "MacroNode4_1", "MacroNode5_1", "MacroNode6_1"
]


# export node point positions to .bindec file
def export_bindec(filepath, nodepoint_order, limit=46):
    scene = bpy.context.scene
    start_frame = scene.frame_start
    end_frame = scene.frame_end

    lines = []

    # Iterate through each frame
    for frame in range(start_frame, end_frame + 1):
        scene.frame_set(frame)
        positions = []

        for name in nodepoint_order[:limit]:  # Use the limit to slice the node order
            obj = bpy.data.objects.get(name)
            if obj:
                pos = obj.matrix_world.translation
                x = pos.x
                z = pos.y
                y = -pos.z  # flip the y
                positions.append(f"{x:.8f},{y:.8f},{z:.8f}")
            else:
                positions.append("0,0,0")

        line = f"[{limit}]{{{'}{'.join(positions)}}}END"
        lines.append(line)

    with open(filepath, 'w') as file:
        file.write(f"Binary blocks count: {len(lines)}\n")
        for line in lines:
            file.write(f"{line}\n")

# import .bindec file
def import_bindec(filepath, nodepoint_order, limit=46):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    # Get the number of binary blocks from the first line
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

        if line.startswith("[") and line.endswith("END"):
            # Extract the positions data between the braces
            try:
                positions_str = line[line.index("{") + 1:line.rindex("}")].split("}{")
                positions = [p.split(",") for p in positions_str[:limit]]  # Use the limit to slice positions

                if len(positions) < limit:
                    # Fill in the missing positions with default values if necessary
                    positions += [["0", "0", "0"]] * (limit - len(positions))

                # Move node points directly
                for i, name in enumerate(nodepoint_order[:limit]):  # Use nodepoint_order with limit
                    obj = bpy.data.objects.get(name)
                    if obj:
                        # Transform coordinates to be correct
                        x = float(positions[i][0])
                        z = -float(positions[i][1])
                        y = float(positions[i][2])

                        pos = (x, y, z)
                        obj.location = pos

                        obj.keyframe_insert(data_path="location", frame=frame)
            except ValueError:
                print(f"Error processing line {frame_index}: {line}")
                continue

    scene.frame_end = scene.frame_start + binary_blocks_count
    scene.frame_set(scene.frame_start)
    
def xml_to_bindec_string(xml_path, nodepoint_order=NODEPOINT_ORDER):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    frame_count = int(root.attrib.get('Count', 0))
    lines = [f"Binary blocks count: {frame_count}"]
    # Each frame is a child element
    for frame in root.findall('Frame_1/..'):
        # Actually root.findall('Frame') won't work; use direct iteration
        pass
    # Correct iteration:
    lines = [f"Binary blocks count: {frame_count}"]
    for frame_elem in list(root):
        nodes = frame_elem.findall('Node')
        positions = [f"{{{n.attrib['X']},{n.attrib['Y']},{n.attrib['Z']}}}" for n in nodes]
        lines.append(f"[{len(nodes)}]" + "".join(positions) + "END")
    return "\n".join(lines)

# Helper: import from bindec text

def import_bindec_from_string(bindec_text, nodepoint_order, limit=46):
    lines = bindec_text.splitlines()
    if not lines or not lines[0].startswith("Binary blocks count:"):
        return {'CANCELLED'}
    binary_blocks_count = int(lines[0].split(":")[1].strip())
    scene = bpy.context.scene
    frame_index = 1
    for frame in range(scene.frame_start, scene.frame_start + binary_blocks_count):
        line = lines[frame_index].strip()
        frame_index += 1
        if line.startswith("[") and line.endswith("END"):
            try:
                pos_str = line[line.index("{") + 1:line.rindex("}")]
                parts = pos_str.split("}{")[:limit]
                positions = [p.split(",") for p in parts]
                # pad if needed
                if len(positions) < limit:
                    positions += [["0", "0", "0"]] * (limit - len(positions))
                for i, name in enumerate(nodepoint_order[:limit]):
                    obj = bpy.data.objects.get(name)
                    if obj:
                        x = float(positions[i][0])
                        z = -float(positions[i][1])
                        y = float(positions[i][2])
                        obj.location = (x, y, z)
                        obj.keyframe_insert(data_path="location", frame=frame)
            except ValueError:
                continue
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
        export_bindec(self.filepath, NODEPOINT_ORDER)
        return {'FINISHED'}

    def invoke(self, context, event):
        scene_name = bpy.path.basename(bpy.context.blend_data.filepath)
        scene_name = os.path.splitext(scene_name)[0]
        
        #   default file path
        self.filepath = bpy.path.abspath("//") + scene_name + ".bindec"
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
# Operator to export node point positions (SF2)
class ExportBindecSF2Operator(bpy.types.Operator):
    bl_idname = "export.bindec_sf2"
    bl_label = "Export Bindec (SF2)"
    bl_description = "Export the positions of node points (SF2) in every frame to a .bindec file"

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Filepath used for exporting the .bindec file",
        subtype="FILE_PATH"
    )

    def execute(self, context):
        if not self.filepath.endswith(".bindec"):
            self.filepath += ".bindec"
        export_bindec(self.filepath, NODEPOINT_ORDER_SF2, limit=67)  # Export with limit 67 for SF2
        return {'FINISHED'}

    def invoke(self, context, event):
        scene_name = bpy.path.basename(bpy.context.blend_data.filepath)
        scene_name = os.path.splitext(scene_name)[0]

        # default file path
        self.filepath = bpy.path.abspath("//") + scene_name + "_sf2.bindec"
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Operator to import node point positions
class ImportBindecOperator(bpy.types.Operator):
    bl_idname = "import.bindec"
    bl_label = "Import Bindec or XML"
    bl_description = "Import positions of node points from a .bindec or .xml file"

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Filepath used for importing the file",
        subtype="FILE_PATH"
    )

    def execute(self, context):
        ext = os.path.splitext(self.filepath)[1].lower()
        if ext == '.xml':
            bindec_text = xml_to_bindec_string(self.filepath, NODEPOINT_ORDER)
            import_bindec_from_string(bindec_text, NODEPOINT_ORDER)
        else:
            import_bindec(self.filepath, NODEPOINT_ORDER)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = bpy.path.abspath("//")
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Operator to import node point positions (SF2)
class ImportBindecSF2Operator(bpy.types.Operator):
    bl_idname = "import.bindec_sf2"
    bl_label = "Import Bindec (SF2)"
    bl_description = "Import positions of node points (SF2) from a .bindec file"

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Filepath used for importing the .bindec file",
        subtype="FILE_PATH"
    )

    def execute(self, context):
        import_bindec(self.filepath, NODEPOINT_ORDER_SF2, limit=67)  # Pass NODEPOINT_ORDER_SF2 and limit
        return {'FINISHED'}

    def invoke(self, context, event):
        # Set the default file path
        self.filepath = bpy.path.abspath("//")  # Start with the current blend file directory
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
        layout.operator(ExportBindecSF2Operator.bl_idname, icon='ARMATURE_DATA')
        layout.operator(ImportBindecSF2Operator.bl_idname, icon='OUTLINER_OB_ARMATURE')

def register():
    bpy.utils.register_class(ExportBindecOperator)
    bpy.utils.register_class(ImportBindecOperator)
    bpy.utils.register_class(ExportBindecSF2Operator)
    bpy.utils.register_class(ImportBindecSF2Operator)
    bpy.utils.register_class(VIEW3D_PT_bindec_export_panel)

def unregister():
    bpy.utils.unregister_class(ExportBindecOperator)
    bpy.utils.unregister_class(ImportBindecOperator)
    bpy.utils.unregister_class(ExportBindecSF2Operator)
    bpy.utils.unregister_class(ImportBindecSF2Operator)
    bpy.utils.unregister_class(VIEW3D_PT_bindec_export_panel)

if __name__ == "__main__":
    register()

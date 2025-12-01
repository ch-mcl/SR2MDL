import bpy

from .SR2Tools import sr2mdl

from bpy.props import (StringProperty,
                       PointerProperty,
                       )

from bpy.types import (Panel,
                       PropertyGroup,
                       )

bl_info = {
    "name": "Sega Rally 2 MDL importer/exporter",
    "description": "Allows editing of Sega Rally 2 models",
    "author": "Spreit, chmcl95",
    "version": (0, 0, 6),
    "blender": (4, 0, 0),
    "category": "Import-Export",
}


class SR2PanelProperties(PropertyGroup):

    path_to_input: StringProperty(
        name="MDL path",
        description="Path to MDl file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH')

    path_to_output: StringProperty(
        name="Output path",
        description="Path to output folder",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')


class SaveOperator(bpy.types.Operator):
    """Save"""
    bl_label = "Save"
    bl_idname = "sr2mdl.save"

    def execute(self, context):
        save_path = bpy.context.scene.sr2_panel_props.path_to_output

        if save_path != "":
            save(save_path)

        return {'FINISHED'}


class LoadOperator(bpy.types.Operator):
    """Load"""
    bl_label = "Load"
    bl_idname = "sr2mdl.load"

    def execute(self, context):
        load_path = bpy.context.scene.sr2_panel_props.path_to_input
        print("Load path", load_path)

        if load_path != "":
            load(load_path, mathutils.Matrix())

        return {'FINISHED'}


class SR2MDLSidebarPanel(bpy.types.Panel):
    """Creates a custom panel in the sidebar"""
    bl_label = "SR2 MDL"
    bl_idname = "OBJECT_PT_SR2_sidebar"
    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    bl_category = "SR2MDL"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        my_props = scene.sr2_panel_props

        # top_row = layout.row()
        # top_row.label(text="Path to file")

        layout.prop(my_props, "path_to_input", text="Path to MDL")

        layout.operator("sr2mdl.load", text="Load")

        row = layout.row()
        row.label(text="Don't forget to triangulate faces (CTRL + T)!")

        layout.prop(my_props, "path_to_output", text="Output folder")
        layout.operator("sr2mdl.save", text="Save")


# List of classes to register
classes = (
    SR2PanelProperties,
    SaveOperator,
    LoadOperator,
    SR2MDLSidebarPanel,
)


# Registration and unregistration
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sr2_panel_props = bpy.props.PointerProperty(type=SR2PanelProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.sr2_panel_props

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()

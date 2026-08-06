import os

import bpy
import mathutils

from .SR2Tools import sr2mdl

from bpy.props import (StringProperty,
                       CollectionProperty,
                       PointerProperty,
                       )

from bpy.types import (Panel,
                       PropertyGroup,
                       )

from bpy_extras.io_utils import (ImportHelper,
                                 ExportHelper,
                                 axis_conversion,
                                 orientation_helper,
                                 )

bl_info = {
    "name": "Sega Rally 2 MDL importer/exporter",
    "description": "Allows editing of Sega Rally 2 models",
    "author": "Spreit, chmcl95",
    "version": (0, 0, 7),
    "blender": (4, 0, 0),
    "location": "File > Import/Export, and the SR2MDL sidebar tab",
    "category": "Import-Export",
}

MDL_FILTER = "*.mdl;*.MDL"

# A MDL is Y-up, Blender is Z-up. Reading one without converting leaves the
# model lying on its back. These are the axes of the MDL, named the way
# Blender's axis_conversion wants them, and they also flip X - not a mirror,
# but the rotation that takes a Y-up model upright without turning its faces
# inside out.
DEFAULT_AXIS_FORWARD = '-Z'
DEFAULT_AXIS_UP = 'Y'


def defaultGlobalMatrix():
    return axis_conversion(from_forward=DEFAULT_AXIS_FORWARD,
                           from_up=DEFAULT_AXIS_UP).to_4x4()


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


def findCollectionToExport(context):
    """
    The SR2MDL collection a File > Export should write.

    One imported model is the normal case. With several open at once the
    active object says which one is meant.
    """
    sr2_collections = sr2mdl.collectSR2Collections(context.scene.collection)

    if len(sr2_collections) == 1:
        return sr2_collections[0], None

    if not sr2_collections:
        return None, "No Sega Rally 2 model in the scene. Import a MDL first"

    active_object = context.view_layer.objects.active
    if active_object is not None:
        for sr2_collection in sr2_collections:
            if active_object.name in sr2_collection.objects:
                return sr2_collection, None

    names = ", ".join(collection.name for collection in sr2_collections)
    return None, "Several models are open ({}). Select an object of the one to export".format(names)


class SaveOperator(bpy.types.Operator):
    """Save"""
    bl_label = "Save"
    bl_idname = "sr2mdl.save"

    def execute(self, context):
        save_path = bpy.context.scene.sr2_panel_props.path_to_output

        if save_path != "":
            sr2mdl.save(save_path)

        return {'FINISHED'}


class LoadOperator(bpy.types.Operator):
    """Load"""
    bl_label = "Load"
    bl_idname = "sr2mdl.load"

    def execute(self, context):
        load_path = bpy.context.scene.sr2_panel_props.path_to_input
        print("Load path", load_path)

        if load_path != "":
            sr2mdl.load(load_path, defaultGlobalMatrix())

        return {'FINISHED'}


@orientation_helper(axis_forward=DEFAULT_AXIS_FORWARD, axis_up=DEFAULT_AXIS_UP)
class ImportSR2MDL(bpy.types.Operator, ImportHelper):
    """Import a Sega Rally 2 model"""
    bl_idname = "import_scene.sr2mdl"
    bl_label = "Import MDL"
    bl_options = {'UNDO'}

    filename_ext = ".mdl"

    filter_glob: StringProperty(default=MDL_FILTER, options={'HIDDEN'})

    # Lets a whole car folder be picked at once
    files: CollectionProperty(type=bpy.types.OperatorFileListElement,
                              options={'HIDDEN', 'SKIP_SAVE'})
    directory: StringProperty(subtype='DIR_PATH',
                              options={'HIDDEN', 'SKIP_SAVE'})

    def execute(self, context):
        if self.files:
            paths = [os.path.join(self.directory, file.name) for file in self.files if file.name]
        else:
            paths = [self.filepath]

        global_matrix = axis_conversion(from_forward=self.axis_forward,
                                        from_up=self.axis_up).to_4x4()

        for path in paths:
            try:
                sr2mdl.load(path, global_matrix)
            except Exception as exception:
                self.report({'ERROR'}, "Could not import {}: {}".format(os.path.basename(path), exception))
                return {'CANCELLED'}

        self.report({'INFO'}, "Imported {} MDL file(s)".format(len(paths)))
        return {'FINISHED'}


class ExportSR2MDL(bpy.types.Operator, ExportHelper):
    """Export a Sega Rally 2 model"""
    bl_idname = "export_scene.sr2mdl"
    bl_label = "Export MDL"

    filename_ext = ".mdl"

    filter_glob: StringProperty(default=MDL_FILTER, options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return bool(sr2mdl.collectSR2Collections(context.scene.collection))

    def invoke(self, context, event):
        # Offer the model's own name, the way it was imported
        sr2_collection, _ = findCollectionToExport(context)
        if sr2_collection is not None:
            self.filepath = sr2_collection.name + self.filename_ext

        return ExportHelper.invoke(self, context, event)

    def execute(self, context):
        sr2_collection, problem = findCollectionToExport(context)

        if sr2_collection is None:
            self.report({'ERROR'}, problem)
            return {'CANCELLED'}

        try:
            sr2mdl.saveCollection(sr2_collection, self.filepath)
        except Exception as exception:
            self.report({'ERROR'}, "Could not export {}: {}".format(sr2_collection.name, exception))
            return {'CANCELLED'}

        self.report({'INFO'}, "Exported {} to {}".format(sr2_collection.name, self.filepath))
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

        layout.prop(my_props, "path_to_output", text="Output folder")
        layout.operator("sr2mdl.save", text="Save")


def menu_func_import(self, context):
    self.layout.operator(ImportSR2MDL.bl_idname, text="Sega Rally 2 Model (.mdl)")


def menu_func_export(self, context):
    self.layout.operator(ExportSR2MDL.bl_idname, text="Sega Rally 2 Model (.mdl)")


# List of classes to register
classes = (
    SR2PanelProperties,
    SaveOperator,
    LoadOperator,
    ImportSR2MDL,
    ExportSR2MDL,
    SR2MDLSidebarPanel,
)


# Registration and unregistration
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sr2_panel_props = bpy.props.PointerProperty(type=SR2PanelProperties)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.sr2_panel_props

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()

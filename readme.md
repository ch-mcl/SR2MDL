# Install
Models can be loaded from File > Import > Sega Rally 2 Model (.mdl) and written
back from File > Export. Several files can be picked at once when importing.
Installing also adds a side panel (where Item, Tool, View, etc are) that loads a
single file and writes every open model into a folder.

MDL files are Y-up while Blender is Z-up, so import rotates the model upright.
The Forward Axis / Up Axis options of the import dialog control that, and the
choice is stored on the collection so export puts the model back the way the
file had it.

Import parents the objects the way the file does. A node's relation names its
first child and its next sibling, and the game draws a child through its
parent's transform, so moving a parent in Blender moves what hangs off it. A
child's transform is parent-relative in the file and in Blender alike, which is
why the axis conversion above sits on the root objects only.

SR2MDL and relevant classes handle MDL file unpacking and packing.
load and generate_mesh functions turn unpacked data into a Blender collection with nodes and meshes.
Blender collection and its Nodes have Custom Properties that store necessary data.

## Save function
- Makes a new SR2MDL
- Takes Blender collection
- Fill SR2MDL with data from collection
- SR2MDL packs the data and saves it


# Notes
- `docs/課題.md` - the open issues
- `docs/mdl_node_pointer_memo.md` - how a node's child and sibling offsets look


# TODO
- Refactor code

? Redo the way additional data is shared between Blender and SR2MDL and SR2Node

A mesh's MDL material comes in as a Blender material. Its values sit under
"SR2 MDL Material" in the Material tab, where they can be edited, and export
writes them back. The six floats of a material are still unidentified.

    Missing
- Write the extra 0x20 block that a mesh's Model Pointers "unk_0x18" points at
  (the light meshes have one, and it is dropped on export)
- Keep the section order a mesh had in the file. Export always writes
  Material, Vertex, Face, while some files have Vertex first

Import reads textures too. A node's transform holds a "Texture Index" at 0x0C,
-1 when the mesh is drawn untextured, otherwise an index into the textures the
model uses. A Track model keeps those in a file named after it (tree_a.mdl and
tree_a.txr); a car indexes into the shared files of its folder, where 0 is
body and 1 the tyre, plus WINDOW.TXR from the EFFECT folder beside them for 2.

    Textures
- Read level embedded textures
- Pick the tyre matching the surface. Import always takes the tarmac one,
  and never the *_dirt* variants
- Draw the wind01..wind14 variants the game puts on a windscreen. Import
  always takes the plain WINDOW

    QOL
- Flip UVs for easy editing
- Work out what the light meshes mean by a Face Count of 1 with 4 vertices.
  Import currently assumes a quad and writes 6 indices back

    Opening Levels
- Figure out Road values meaning
- Figure out Kinda Pointers values meaning. They do not look like the array of
  eight pointers they are read as
- Figure out what Node Indexes array is for
- Write a level back out. Export does not know about roads or anything else
  that only a level has
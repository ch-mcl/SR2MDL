# Install
Models can be loaded from File > Import > Sega Rally 2 Model (.mdl) and written
back from File > Export. Several files can be picked at once when importing.
Installing also adds a side panel (where Item, Tool, View, etc are) that loads a
single file and writes every open model into a folder.

MDL files are Y-up while Blender is Z-up, so import rotates the model upright.
The Forward Axis / Up Axis options of the import dialog control that, and the
choice is stored on the collection so export puts the model back the way the
file had it.

SR2MDL and relevant classes handle MDL file unpacking and packing.
load and generate_mesh functions turn unpacked data into a Blender collection with nodes and meshes.
Blender collection and its Nodes have Custom Properties that store necessary data.

## Save function
- Makes a new SR2MDL
- Takes Blender collection
- Fill SR2MDL with data from collection
- SR2MDL packs the data and saves it


# TODO
- Refactor code

? Redo the way additional data is shared between Blender and SR2MDL and SR2Node
? Make Blender object heirarchy in the same way they are in node.relation? 

A mesh's MDL material comes in as a Blender material. Its values sit under
"SR2 MDL Material" in the Material tab, where they can be edited, and export
writes them back. The six floats of a material are still unidentified.

    Missing
- Write the extra 0x20 block that a mesh's Model Pointers "unk_0x18" points at
  (the light meshes have one, and it is dropped on export)
- Keep the section order a mesh had in the file. Export always writes
  Material, Vertex, Face, while some files have Vertex first

    Textures
- Auto load textures, if present
- Auto flip the texture
- Read level embedded textures

    QOL
- Flip UVs for easy editing
- Work out what the light meshes mean by a Face Count of 1 with 4 vertices.
  Import currently assumes a quad and writes 6 indices back

    Opening Levels
- Figure out where to get offsets for the rest of the environment
- Figure out Road values meaning
- Figure out Kinda Pointers values meaning
- Figure out what Node Indexes array is for
- Figure out how to parse Nodes with 0xFFFFFFFF
# Install
When you install/run the script, a side panel will appear (where Item, Tool, View, etc are)

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

    Missing
- Update Node Scale and Position when saving
- Material representation?

    Usability
- Add import button to Blender import submenu

    Textures
- Auto load textures, if present
- Auto flip the texture
- Read level embedded textures

    QOL
- Flip UVs for easy editing
- Rotate entire model on load. Pivot at the world origin
- Scale X axis of all parts by -1 to have correct texture display
(Don't forget to undo the above while saving)

- Load entire car folder

    Opening Levels
- Figure out where to get offsets for the rest of the environment
- Figure out Road values meaning
- Figure out Kinda Pointers values meaning
- Figure out what Node Indexes array is for
- Figure out how to parse Nodes with 0xFFFFFFFF
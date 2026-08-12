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

A mesh can carry a 0x20 block between its faces and its Model Pointers, whose
"unk_0x18" holds the offset. Only the four-vertex light billboards of a car
have one - 73 of the 3810 meshes in the sample files - and all 73 hold the same
eight floats, 0.0 and 1.0 four times over. What they mean is open, so import
keeps the bytes on the object under "Model Extra Block" and export puts them
back where they were.

A round trip of a whole car folder has been driven in game and behaves. That
settles two of the differences below as cosmetic: the game reads a mesh through
the offsets in its Model Pointers, so the order the sections sit in does not
reach it, and neither does a UV that is off by a sign bit or an ULP.

A UV that was not edited goes back as it was read, the same way a normal does.
Import flips V and export flips it back, which is exact on paper but not in
single precision: a V of 0.0 returned as -0.0, and the rounding could move the
last bit besides.

A MDL keeps one UV per vertex while Blender keeps one per corner, so a UV edit
only reaches the file if every corner sharing that vertex is given the same
value. Export takes the last corner it sees otherwise.

    Byte-identity, not correctness
- Keep the section order a mesh had in the file. Export always writes
  Material, Vertex, Face, while 54 of the 136 sample models have Vertex first
- 28 UV coordinates, spread over four KEROLLA light models, hold a signalling
  NaN. Reading one into a Python float quiets it, which no amount of storing
  can undo - it would take carrying raw words through the whole vertex path.
  The value stays a NaN either way, in the U of an untextured billboard

A normal that Blender cannot hold goes back exactly as it was read. Blender
normalizes a custom normal, so a zero-length one comes back as whatever the
faces say and a non-finite one comes back as a default - the value in the file
never reaches the user, so it cannot have been edited either. tree_a.mdl
through tree_f.mdl zero four normals each, and Char/A.MDL and Char/Z.MDL store
0, NaN, 0 for every vertex, NaN payload and all.

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

Not every mesh stores its faces the way this tool writes them. "Face Count" is
an index count for the usual mesh, always a multiple of three. 98 meshes of the
sample files hold 1 instead - every one of them a four-vertex billboard, a
car's lights among them - and their face region is four 32-bit indices, 3, 2,
1, 0 or 1, 0, 3, 2, sometimes followed by a 1.0 or -1.0. Writing those back as
six 16-bit indices with a Face Count of 6 froze the game.

Import flags such a mesh with a "Fixed Face Data" custom property, and export
writes its face bytes from the file instead of from the Blender mesh for as
long as that is set. Editing one is therefore safe: move its vertices, change
its UVs, even add geometry, and the encoding the game expects still comes out.
Both have been driven in game - a car's lights scaled to twice their size, and
the same again with a vertex added, which the game takes in its stride because
nothing references it.
The flag sits in the object's Custom Properties, so it can be cleared to hand
the mesh back to the usual triangle path, or set on a mesh built in Blender to
have it written as a billboard - one with no bytes of its own falls back to a
single face of 3, 2, 1, 0.

    QOL
- Flip UVs for easy editing
- Work out what picks one face encoding over the other. Until then a mesh can
  only be moved between the two by hand, through the "Fixed Face Data" flag

A level's node index array turned out to be one slice of road indexes per
road, the road saying where its slice starts and how long it is. A slice holds
other roads, never itself, never a duplicate, always ascending - the set of
road segments that matter while driving this one. How many there are tracks how
far one can see: RIVIERA averages 2.6, the desert of DES_SS1 15.2.

The header field counts indexes, not bytes. Reading it as a size took a quarter
of the array and started every section behind it mid-array, which is why the
kinda pointers looked like nothing in particular.

    Opening Levels
- Figure out the rest of the Road values. A road has 24 of them and two more
  are now known: where its slice of the node index array starts and how long
- Figure out Kinda Pointers values meaning. With the node index array read at
  its real length they start where they should, and RIVIERA's count times 32
  accounts for its remaining bytes exactly - DES_SS1 has more left over than
  that, so something else follows them there
- Write a level back out. Export does not know about roads or anything else
  that only a level has
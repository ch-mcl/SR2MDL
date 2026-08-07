chmcl95 — 2025/11/16 20:52
I guess Node like this.
Ah Offsets have mistakes.
Case: l_corolla.mdl
```
Address        0x68value   0x6Cvalue
0xA320         0x00        0x00
 |-0xA2A0      0x01        0x01
 |-0xA220      0x02        0x01
 |-0xA1A0      0x03        0x01
 |-0xA120      0x04        0x01
 |-0xA0A0      0x05        0x01
 |-0xA020      0x06        0x02
 |-0x9FA0      0x07        0x02
 |-0x9F20      0x08        0xFFFFFFFF(-1)
    |-0x9EA0   0x09        0xFFFFFFFF(-1)
```

Case: DES_SS1.DAT
only 0x1D5D20 (NodePointer[43]) expalain.
NodePointer[43] of 0x04 pointing 0x14CE80.

And I guess 0x14CE80 Node likes.
```
Address        0x68value  0x6Cvalue
0x1D5D20       (Actual not Node. But write for  Nose 0x14CE80 to 0x14D180 relations.)
 |-0x14CE80    0x41       0x09
 |-0x14CF00    0x43       0x0B
 |-0x14CF80    0x49       0x0F
 |-0x14D000    0x4C       0x10
 |-0x14D080    0x4B       0x07
 |-0x14D100    0x46       0x11
 |-0x14D180    0x47       0x13
```
I based 0x60 of Node is child.
And 0x64 of Node is sibling.
So no additional space with |- means sibling.(0x64 has valid pointer for node).
Additional space with |- means child.(0x60 has valid pointer for node).

---

# Checked against the files

The tree above is right. A node's relation holds the offset of its first child
at 0x60 and of its next sibling at 0x64, and both cases reproduce exactly.

Two labels in it are off, so reading it later does not send anyone the wrong
way:

- The two columns are **0x08 and 0x0C**, not 0x68 and 0x6C. They are the Node
  Index and the Texture Index of the node transform. Every value listed for
  l_corolla.mdl matches what is at those offsets.
- **NodePointer[43] is Road[43]**. The road array starts at Relation Offset +
  0x20, which puts entry 43 of DES_SS1.DAT at 0x1D4D00 + 43 * 0x60 = 0x1D5D20.
  Its field at +0x04 is the road's "Node Offset", pointing at 0x14CE80.

One transcription slip: the first node of the DES_SS1 chain has Node Index
0x42, not 0x41. The rest of that table, including every Texture Index, is
exactly what the file holds.

Following the chain matters. A road points at the head of a sibling list, and
reading only the head left most of a level behind - 120 of RIVIERA.DAT's 628
nodes, 437 of DES_SS1.DAT's 902.

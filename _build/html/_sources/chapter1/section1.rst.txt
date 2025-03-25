Design Architecture
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _Diagram1:
.. figure:: _static/images/LatestStructureDiagram.png
   :width: 100%
   :align: center
   :alt: pic1
   
   Structure Diagram
   
:numref:`Figure %s <Diagram1>` shows the latest HW sturcture of redesigned P5 CPU module, P5 use AM64 brick(GEX95646) with main processor AM6442 macrocomponent integrate the set of common core components needed by any host project which wants to use the AM64 SoC:

- AM64
- LPDDR4 SDRAM Memory
- OSPI NOR Flash Memory
- NAND Flash Memory
- Crystal
- Power Management (DC/DC converters, Power sequencer and voltage supervisor)
- Power Bypass capacitors 

.. _Diagram1-2:
.. figure:: _static/images/AM64_brick.png
   :width: 100%
   :align: center
   :alt: pic1
   
   AM64 brick Diagram


Refer to the typical design of the brick :numref:`Figure %s <Diagram1-2>` .It can cover all the functions instead of Spear1380 did(except LCD interface).
Co-processor AM2434 are designed for expend the IOs and ethernet for P5.

.. _example-pdf:

Here is a link to an example PDF: :download:`AM64 BRICK SPEC.pdf <_static/pdf/AM64 BRICK - Technical Specifications rev05.pdf>`

Power Tree and reset Tree are following existing P5 CPU board and optimized based on TI Sitara seies processor.
  

.. figure:: _static/images/Power_Tree.png
   :width: 100%
   :align: center
   :alt: pic1
   
   Power Tree
   

.. figure:: _static/images/Reset_Tree(Draft).png
   :width: 100%
   :align: center
   :alt: pic1
   
   Reset Tree 






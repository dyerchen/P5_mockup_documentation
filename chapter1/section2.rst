P5 mockup First Prototype
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:numref:`Figure %s <Diagram6>` shows the latest HW sturcture of redesigned P5 CPU module, P5 use AM64 brick(GEX95646) with main processor AM6442 macrocomponent integrate the set of common core components needed by any host project which wants to use the AM64 SoC:

.. _Diagram6:
.. figure:: _static/images/P5-CPU-MOCKUP-TOP.png
   :width: 70%
   :align: center
   :alt: pic1
   
   P5-CPU-MOCKUP-TOP   

.. figure:: _static/images/P5-CPU-MOCKUP-BOTTOM.png
   :width: 70%
   :align: center
   :alt: pic1
   
   P5-CPU-MOCKUP-Bottom   


.. _Diagram7:
.. figure:: _static/images/P5-CPU-TOP_00.png
   :width: 70%
   :align: center
   :alt: pic1
   
   Old CPU board.
   
   
Compared to the old CPU board, the new P5 CPU board has the following improvements:

1. The processor has been changed, the FPGA has been removed, the AM64 is used as the main processor, and the AM24 is used as the coprocessor.

2. The USB port has been changed from mini-USB to Type-C, and one Type-C port can handle all the functions of the previous two USB ports, with automatic switching between master and slave modes.

3. DI and DO control has been implemented in the P3+, and it is compatible with the logic control of 12I4O/6I4O/PSU boards.

4. The RGB screen has been successfully lit.

5. The PCIE demo has been completed by the French team. Currently, it is only necessary to determine whether the final architecture of the FW is based on VXworks or updated to Linux.








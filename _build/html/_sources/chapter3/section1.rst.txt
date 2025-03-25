Send uboot to Cache/LPDDR
------------------------------------------------------------------------------

xmode tiboot3-hs.bin 2 times
******************************

.. _Diagram31:
.. figure:: _static/images/xmode1.png
   :width: 40%
   :align: center
   :alt: pic1
   
   xmode 1st time
   
.. _Diagram32:
.. figure:: _static/images/xmode2.png
   :width: 40%
   :align: center
   :alt: pic1
   
   xmode 2nd time
   
ymode tispl.bin 1 time
**************************

.. _Diagram33:
.. figure:: _static/images/ymode.png
   :width: 40%
   :align: center
   :alt: pic1
   
   ymode tispl.bin


ymode  u-boot.img 1 time
**************************

can remove jump cap in programming

.. _Diagram34:
.. figure:: _static/images/ymode2.png
   :width: 40%
   :align: center
   :alt: pic1
   
   ymode  u-boot.img

System will reboot automatically

.. Attention::

	系统自动重启时用 ctrl-C 打断启动过程 不及时打断会直接进入CCCCCC 模式，前面的操作白做。
	
Enter uboot → program to Nor flash
------------------------------------------------------------------------------

- Switch to DFU download mode

.. code-block:: bash        
		
		dfu 0 sf

.. _Diagram5:
.. figure:: _static/images/Switch_to_DFU.png
   :width: 40%
   :align: center
   :alt: pic1
   
   ymode  u-boot.img
   
connect USB and find USB download gadget device

.. _Diagram35:
.. figure:: _static/images/DFU.png
   :width: 40%
   :align: center
   :alt: pic1
   
   ymode  DFU Device
   
Operation in Powershell
------------------------------------------------------------------------------

after uboot boot up
**************************

.. code-block:: bash        
		
		dfu-util -a tiboot3.bin -D tiboot3-hs.bin -d 0451:6165
		
.. _Diagram36:
.. figure:: _static/images/tiboot3.png
   :width: 40%
   :align: center
   :alt: pic1
   
   dfu-util tiboot3
		
.. code-block:: bash        
		
		dfu-util -a tispl.bin -D tispl.bin -d 0451:6165
		
.. _Diagram37:
.. figure:: _static/images/tispl.png
   :width: 40%
   :align: center
   :alt: pic1
   
   dfu-util tispl
		
.. code-block:: bash        
		
		dfu-util -a u-boot.img -D u-boot.img -d 0451:6165
		
.. _Diagram38:
.. figure:: _static/images/u-boot.png
   :width: 40%
   :align: center
   :alt: pic1
   
   dfu-util u-boot.img

//dfu-util -a bitfile -D bitfile -d 0451:6165 backup

.. code-block:: bash        
		
		dfu-util -a rootfs_a -D customized-dev-image-ep-p3plus.ubi -d 0451:6165
		
.. _Diagram39:
.. figure:: _static/images/customized-dev.png
   :width: 40%
   :align: center
   :alt: pic1
   
   dfu-util customized-dev-image-ep-p3plus.ubi


.. code-block:: bash        
		
		reset

		
.. _Diagram40:
.. figure:: _static/images/reset.png
   :width: 40%
   :align: center
   :alt: pic1
   
   reset and reboot

enter in Linux.

.. _Diagram41:
.. figure:: _static/images/enter_in_Linux.png
   :width: 40%
   :align: center
   :alt: pic1
   
   enter in Linux

find a new ethernet adaptor when plug in USB cable, setting IP address to 90.0.0.X, ping 90.0.0.1. (如有必要可关闭防火墙)


.. raw:: html

	<span style="color: bule;">Congratulation! Linux run successfully.</span>. 


.. Attention::
	在使用P3+的工程加载到P5的mockup板是，会出现尝试三次之后无法进入linux的情况，原因是在Linux系统里看到的设备树有问题，可能跟NOR的型号有关联。	
	因此会在尝试3次失败后停止进入Linux.
	需要擦除0x7f0000 地址的信息后reset.
	
uboot command

.. code-block:: Shell        
		
		sf probe
		sf erase 0x7f0000 0x10000
		reset
		
		
.. Attention::
	如果出现NOR被破坏的情况，需要擦除后重新烧录bin文件dfu-util -a tiboot3.bin(两次)/tispl.bin/u-boot.img

擦除整片操作：

.. code-block:: Shell        
		
	sf probe
	sf erase 0 0x2000000
	dfu 0 sf

NAND flash used in ARC and P5 mockup
**************************************


.. table:: NAND Flash Test Results

    +----------------+------------+------------+-----------------+---------------------------------------------------------------+
    | Project        | SPN        | Manufacture | Test Result    | Description                                                   |
    +----------------+------------+------------+-----------------+---------------------------------------------------------------+
    | P5 mockup      | TME23633   | MACRONIX-M | 4 blocks bad,   | Does not support Permanent Block Lock Disable Mode.           |
    |                |            | X60UF8G18AC| 3 blocks        | Each time a single block needs to be tested and skipped.      |
    +----------------+------------+------------+-----------------+---------------------------------------------------------------+
    | ARC            | TME09355   | Micron     | Works well      | Device 0: nand0, sector size 256 KiB                          |
    |                |            | MT29F4G08  | Page size 4096 b| Permanent block lock disable mode is enabled, for the drive,  |
    |                |            | ABBF4H4-   | OOB size 256 b  | the block address is continuous.                              |
    |                |            | AAT:F      | Erase size      | Software shows no bad blocks.                                 |
    |                |            |            | 262144 b        |                                                               |
    |                |            |            | ecc strength    |                                                               |
    |                |            |            | 8 bits          |                                                               |
    |                |            |            | ecc step size   |                                                               |
    |                |            |            | 512 b           |                                                               |
    |                |            |            | subpagesize     |                                                               |
    |                |            |            | 1024 b          |                                                               |
    |                |            |            | options         | 0x00000400c                                                   |
    |                |            |            | bbt options     | 0x00000000                                                    |
    +----------------+------------+------------+-----------------+---------------------------------------------------------------+
	
.. _example-pdf3:
	
datasheet::download:`Macronix_MX60UF8G18AC datasheet<_static/pdf/Macronix_MX60UF8G18AC.pdf>`

.. _example-pdf4:
	
datasheet::download:`MT29F4G08ABBFAH4 datasheet<_static/pdf/MT29F4G08ABBFAH4 .pdf>`	



.. seealso:: more ref :doc:`/chapter1/section1`。
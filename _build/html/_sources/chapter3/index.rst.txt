Program Linux to NOR/NAND for P5 MOCKUP CPU board
===========================================================================

Tools:

Teraterm → program in UART mode

Main process:
- xmode tiboot3-hs.bin 2 times 
- ymode tispl.bin 
- ymode u-boot.img


In Powershell

- earse NAND(check black block)
- Switch to DFU download mode 
- dfu-util -a tiboot3.bin/tispl.bin/u-boot.img
- dfu-util customized-dev-image-ep-p3plus.ubi

切换成UART 模式 跳冒 ON

.. toctree::
   :maxdepth: 2
   :caption: PRU RGB driver

   section1

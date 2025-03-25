P5 PRU RGB Solution
------------------------------------------------------------------------------

A PRU has a total of 20 GPI/GPO pins available. The LCD interface consists of RGB 888 + DCLK + HSYNC + VSYNC + DE + DISP, totaling 28 pins. In the design, sacrificing the lower 3 bits of color does not make a noticeable difference to the naked eye. Therefore, the final implementation uses RGB 555 + DCLK + HSYNC + VSYNC + DE + DISP, which requires 20 pins and can be realized by a single PRU. The only trade-off is that the color depth is reduced from 16.7 million colors (2^24) to 32,768 colors. Since the Spear1380 in P5 also designed base on RGB555 data, there is no impact on user, and in fact, the human eye cannot easily distinguish the difference.

This section describes the functionality of the PRU assembly code for driving a 480x272 RGB555 LCD panel using Texas Instruments' PRU (Programmable Real-Time Unit).

PRU Pin map in P5 mockup CPU board
==================================

One PRU play the role of a LCD controller.

+--------------------+---------------+-----------------------------------------------+
| PRU PIN            | RGB signal    | Description                                   |
+====================+===============+===============================================+
| PRG1_PRU1_GPO0     | LCD_R3        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO1     | LCD_R4        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO2     | LCD_R5        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO3     | LCD_R6        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO4     | LCD_R7        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO5     | LCD_G3        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO6     | LCD_G4        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO7     | LCD_G5        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO8     | LCD_G6        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO9     | LCD_G7        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO10    | LCD_B3        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO11    | LCD_B4        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO12    | LCD_B5        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO13    | LCD_B6        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO14    | LCD_B7        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO15    | LCD_PCLK      | Pixel clock                                   |
|                    |               | DISP="H": Display on                          |
|                    |               | DISP="L": Display off, All outputs High-Z     |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO16    | LCD_PE        |                                               |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO17    | LCD_HSYNC     | Horizontal synchronous signal                 |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO18    | LCD_VSYNC     | Vertical synchronous signal                   |
+--------------------+---------------+-----------------------------------------------+
| PRG1_PRU1_GPO19    | LCD_DE        | Data Enable                                   |
+--------------------+---------------+-----------------------------------------------+


LCD Controller Macro definition
=======================================

Users can easily change the parameters according to the different LCD tpyes.

.. sourcecode:: asm
   :caption: Macro definition for RGB parameters
   :linenos:   

	H_ACTIVE    .set  480   ; 有效行像素数 | Active pixels per line
	V_ACTIVE    .set  272   ; 有效帧行数 | Active lines per frame
	H_FPORCH    .set  43    ; 行前沿周期数 | Horizontal front porch
	H_BPORCH    .set  12    ; 行后沿周期数 | Horizontal back porch
	V_FPORCH    .set  20000 ; 场前沿周期数 | Vertical front porch  20000
	V_BPORCH    .set  10000 ; 场后沿周期数 | Vertical back porch   10000

	CLK_HIGH    .set  4     ; PCLK高电平周期(20ns) | PCLK high duration
	CLK_LOW     .set  2     ; PCLK低电平周期(20ns) | PCLK low duration
	CLK_HIGH_P  .set  4     ; 消隐期PCLK高电平 | Porch period high 4
	CLK_LOW_P   .set  3     ; 消隐期PCLK低电平 | Porch period low  3




Key Components
=======================================

1. **Register Definitions**
   - Critical registers mapped for real-time control:
   
.. code-block:: asm
    :emphasize-lines: 3
        
	.asg    r0, SHARED_MEM		; 共享内存基地址 | Shared memory base address
 	.asg    r1, TEMP_MASK     	; RGB掩码临时寄存器 | Temporary RGB mask register
 	.asg    r2, LINE_CNT		; 行计数器 | Line counter (H_ACTIVE)
 	.asg    r3, FRAME_CNT		; 帧计数器 | Frame counter (V_ACTIVE)
 	.asg    r4, PIXEL_DATA		; 像素数据寄存器 | Pixel data register
 	.asg    r5, DELAY_LOOP		; 延时循环计数器 | Delay loop counter
 	.asg    r6, REG_T1 			; 通用临时寄存器 | General purpose temp register
 	.asg    r7, MEM_ADDR		; 内存地址指针 | Memory address pointer
 	.asg    r8, CTRL_STATE		; 控制状态寄存器 | Control state register
 	.asg    r9, RGB_MASK  		; RGB掩码寄存器 | RGB mask register
 	.asg    r28, RET_ADDR       ; 子程序返回地址 | Subroutine return address

2. **Timing Configuration**
   - Precise clock timing for DE/HSYNC/VSYNC signals:
   
.. code-block:: asm
     :linenos:
        
        CLK_HIGH    .set  4     ; 20ns high pulse
        CLK_LOW     .set  2     ; 10ns low pulse
        H_ACTIVE    .set  480   ; Visible pixels per line
        V_FPORCH    .set  20000 ; Vertical front porch cycles

3. **Memory Mapping**
   - Shared memory configuration for pixel data transfer:
   			
.. note::
	
	In R5, at least one page frame of data needs to be loaded into the memory, and then PRU outputs it according to the RGB logical timing sequence.One frame need 480*272*16 = 2,088,960 bits = 2,040 Kbyte(RGB555,2 bytes for each pixel) stored in memory.
	
	
.. _Diagram9:
.. figure:: _static/images/PRU_ICSSG_DDRAM.png
   :width: 100%
   :align: center
   :alt: pic1
   
   PRU_ICSSG_DDRAM
   
PRU_ICSSG_DDRAM is pivotal in providing low-latency, high-bandwidth storage for PRU cores, enhancing real-time performance and enabling seamless collaboration between heterogeneous processors in industrial control systems. Its hardware-level memory management significantly improves system reliability and responsiveness. But the maximum size is 8KB*4=32KB, **not enough to store on frame**.
   
Latency of W/R of PRU_ICSSG_DDRAM is 15ns (3 instruction cycle) With PRU cores operating at 200 MHz (5ns per instruction cycle)
   
.. code-block:: asm

		; PRU_ICSSG DRAM (local)      0000_0n00h, nnnn = c24_blk_index[3:0]  (not clear if 4 or 8bits are configurable)
		LDI     REG_T1, 0x0000         ; c24 points to begin of DATA RAM
		SBCO    &REG_T1, c11, 0x20, 1  ; c11+0x20 => ICSSG_PRU_CTBIR0, bit7..0 => c24_blk_index;  (refman 6.4.14.1.6, 6.4.5.2.1  )
   
We have to use MSRAM in AM24 to share the farme data from R5 --> PRU.

.. _Diagram10:
.. figure:: _static/images/MSRAM.png
   :width: 100%
   :align: center
   :alt: pic1
   
   MSRAM
   
In the R5 code, it is only necessary to place the data in the SHARE MEM address starting from the offset address 0x70000000, and the PRU will automatically output the frame according to the RGB timing sequence.

.. code-block:: C
	:caption: R5 filled color.
	 
		#define SHARED_MEM_BASE 0x70000000

		void fill_color(uint16_t color) {
			for(int i=0; i<480*272; i++){
				 shared_mem[i] = color;
			}
		}
		
In R5, use LBBO to read out the pixel data from share mem , one ticket one pixel(2 bytes)

.. code-block:: asm
	:caption: PRU read out pixel data
	 
		MAIN_LOOP:
			; 重置共享内存指针 | Reset shared memory pointer
			LDI32   SHARED_MEM, SHARED_BASE
			; 垂直前沿消隐处理 | Vertical front porch handling
			LDI32   DELAY_LOOP, V_FPORCH
			
		LINE_LOOP:
			SHARED_BASE  .set 0x70000000
			LBBO   &PIXEL_DATA, SHARED_MEM, 0, 2  ; 2-byte pixel read


.. Attention::
	
	ICSS internal RAMs, DMEM0 (8KB), DMEM1(8KB) and SMEM (64KB) incurs 15ns latency for LBBO or LBCO.
	
	MSRAM is better suited for burst access of 32 or 64 bytes, as read penalty remain the same as reading 2 bytes (!) and much faster and does not stall PRUs.
	
	LBBO command takes nearly 120ns in PRU when visiting MSRAM (0x70000000) in PRU cores operating at 200 MHz.


The clock range supported by PCLK in the RGB timing sequence is 8-12 MHz (with a period of 125ns-83.333ns) SEE :numref:`Figure %s <Diagram5>`. 

However, in the PRU code, a single LBBO instruction occupies 120ns. Unlike in FPGA, assembly language is executed sequentially. During the execution of the LBBO instruction for data fetching, no other operations can be performed. This results in a very low duty cycle for the output PCLK clock SEE :numref:`Figure %s <Diagram11>` , which can be seen in the actual output waveform. 

TI FAE confirmed that LBBO cause high latency:

`TI Design support link <https://e2e.ti.com/support/microcontrollers/arm-based-microcontrollers-group/arm-based-microcontrollers/f/arm-based-microcontrollers-forum/1485851/am2434-lbbo-command-takes-nearly-120ns-in-pru-when-visiting-msram-0x70000000>`_。

Fortunately, in DE mode, there is no impact, and the screen can display normally. Moreover, when the PRU clock frequency is changed to 333 MHz, the time for the LBBO instruction is further reduced, meeting the timing requirements of 8-12 MHz.

Core Functionality
=======================================

1. **Vertical Blanking** (V_BLANK_LOOP)
   - Generates vertical sync timing with precise clock cycles:
   
.. code-block:: asm
        :emphasize-lines: 3
        
        SET     r30, r30, PCLK_BIT
        LDI     r7, CLK_HIGH_P
        SUB     r7, r7, 1       ; High duration counter

2. **Active Pixel Transfer** (LINE_LOOP)
   - Real-time pixel streaming with RGB555 formatting:
   
.. code-block:: asm
        
        MOV   r30.w0, PIXEL_DATA ; Output RGB to GPIO
        SET   r30, r30, DE_BIT   ; Enable data valid

3. **Horizontal Sync Control**
   - Manages line timing with front/back porch periods:
   
.. code-block:: asm
        
        LDI     DELAY_LOOP, H_FPORCH + H_BPORCH
        CLR     r30, r30, DE_BIT ; End of active line


Timing Diagram(DE MODE)
=======================================

.. figure:: _static/images/pru_timing.png
   :align: center
   :alt: LCD Timing Diagram

   Critical timing parameters for 480x272 resolution
   
.. _Diagram11:
.. figure:: _static/images/PCLK_duty_cycle.png
   :width: 100%
   :align: center
   :alt: pic1
   
   PCLK duty cycle

.. _Diagram12:
.. figure:: _static/images/line_fresh.png
   :width: 100%
   :align: center
   :alt: pic1
   
   line fresh

.. _Diagram13:
.. figure:: _static/images/flash_rate.png
   :width: 100%
   :align: center
   :alt: pic1
   
   frame timing      

Implementation Notes
=======================================
- Uses **6-cycle pixel clock** (4 high + 2 low) @ 333MHz PRU clock
- Achieves **60Hz refresh rate** through cycle-counted loops
- Supports **15-bit RGB555** color depth via GPIO bit mapping


Validation of different LCD models
=======================================

.. _Diagram14:
.. figure:: _static/images/DE_lighing.png
   :width: 70%
   :align: center
   :alt: pic1
   
   Successfully lit up the screen

.. video:: _static/video/LCD_lighting.mp4
   :width: 60%
   :poster: _static/thumbnail.png
   :align: center
   
 
   
   LCD_lighting



Test result

.. raw:: html

	1.YES YTS430ILBC   <span style="color: green;">passed</span>. 

.. _example-pdf:
	
spec::download:`YTS430ILBC-01-100N spec<_static/pdf/YTS430ILBC-01-100N_2021.12.24_ver1.1.pdf>`

.. raw:: html

	2.TIANMA P0430WQF1ME00_V2.1 <span style="color: green;">passed</span>. 

.. _example-pdf-2:

spec::download:`PP0430WQF1ME00 spec <_static/pdf/Final Specification P0430WQF1ME00_V2.1.pdf>`

.. raw:: html

	3.kyocera TCG043WQLBxANN <span style="color: red;">failed</span>.

.. _example-pdf-3:

spec::download:`TCG043WQLBxANN spec <_static/pdf/kyocera_TCG043WQLBxANN-GNx05Eng.pdf>`>
	
.. _Diagram15:
.. figure:: _static/images/kyoceya_fail_DE.png
   :width: 70%
   :align: center
   :alt: pic1
   
   failed lit up kyocera TCG043WQLBxANN



kyocera TCG043WQLBxANN is the LCD which used in P5 mass production now, it used a very old controller which not support DE mode.

.. raw:: html

	Test in Kyocera TCG043WQLBDBNN-AN00-JA <span style="color: green;">passed</span>. 
	
2 OPTIONS if we still want to use Kyocera LCD:

- build a code dedicated for SYNC mode.
- qualify a new Kyocera LCD with DE-mode compatible.


A small tool for generating pixel data for P5
=============================================

A small tool based on Python that can simply upload images and convert them into the pixel format used by P5, and then directly store them at the address 0x7000000.

:download:`download P5_RGB_vector_EN tool <_static/tool/P5_RGB_vector_EN.7z>`

.. _Diagram16:
.. figure:: _static/images/P5_Image_RGB_exporter.png
   :width: 70%
   :align: center
   :alt: pic1
   
   P5_Image_RGB_exporter tool
# FaceRecognition_EntranceGuardSystem
人脸识别门禁系统-2018电子设计大赛初赛

# 题目：基于人脸识别的门禁系统

学  校     华南农业大学        
队  名     除了发呆什么都不会  
队长姓名   李棋俊              
队员姓名   沈俊杰              
队员姓名   邓益贤    

### 基于树莓派的服务器 
- 在设计过程中硬件采用了树莓派作为整个门禁系统的控制核心
- 功能和原理
> 基于树莓派的服务器，它内置网卡和支持TCP协议，因此通过USB口直接与摄像头连接，可以进行图像数据的传输。另外对于摄像头的图像数据经过分析处理、存储后，通过和ESP8266无线模块连接，进而控制Arduino来控制舵机做出开关门动作。基于TCP协议而实现服务器和摄像头及Arduino之间的数据传输。

### 图像采集
> 图像采集是门禁系统的基础，设计中尽可能高效的获得摄像头数据，为后续人脸探测和人脸识别程序节省更多系统资。本系统采用的是罗技C270摄像头，可以通过USB与设备连接，即插即用，方便快捷

-功能和原理
> 该摄像头通过USB端口用数据线和树莓派服务器连接，通过调用设备驱动程序打开摄像头，进行摄像头初始化。当摄像头捕捉到人脸后,执行相应的程序就可将检测到的人脸图像保存在树莓派服务  器本地存储空间中备用，进行解析、分析。如果摄像头没有捕捉到人脸,系统将继续处于待工作状态,直至检测到人脸,以上实现了本系统的自动触发的功能。

### Arduino控制舵机 
- 功能和原理
> Arduino以ESP8266无线接入模块为桥梁来接受服务器的数据控制，当服务器进行人脸的识别的过程也能够，并把识别结果发送到Arduino上后，就可以驱动舵机进行开门或者不开门的功能。

### ESP8266无线接入模块 
- 模块描述
> ESP8266是乐鑫公司生产的低功耗WiFi芯片模块。模块核心处理器 ESP8266 在较小尺寸封装中集成了业界领先的 Tensilica L106 超低功耗 32 位微型 MCU，支持标准IEEE802.11 b/g/n 协议，完整的 TCP/IP 协议栈。用户可以使用该模块为现有的设备添加联网功能。其工作模式有STA 模式、AP 模式、STA+AP 模式三种。

- 功能和原理
> ESP8266无线模块作为连接各个模块的桥梁，可以通过TCP协议与树莓派服务器之间的数据传送，进而使Arduino能够根据人脸识别结果有效运行工作，进而决定舵机的转动与否。


## 操作指南
- 手机放热点，树莓派、ESP8266接到手机的网络，使三者处于同一网络状态
>
1. 树莓派启动服务器程序
2. 手机APP TCP连接 连接到树莓派的服务器
3. ESP8266通电后连接到树莓派服务器
- 树莓派服务器端接收到 手机和ESP8266的客户端
4. 手机发送 开始识别 指令到服务器，服务器收到指令后控制摄像头拍照，并且将结果发送到客户端ESP8266处
5. ESP8266接收到服务器发送的数据，传数据给Arduino，进行关门/开门动作


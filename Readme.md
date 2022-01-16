# 电显生成工具Beta

BU5DR1V3R

本工具目前支持SLK6109收费版电显格式，具体参数：

![empty](F:\INTERESTINGSTUFF\makeK-release\lib\empty.bmp)

第一行 128\*16(p) 第二行256\*16(p)

## 使用方法

### 1.在src.txt中按格式输入

![image-20220116114549088](C:\Users\Busdriver\AppData\Roaming\Typora\typora-user-images\image-20220116114549088.png)

黄色标记必须使用TAB键（\t）分隔符进行分隔，即形成三列。

第一列为保存的文件名，需要你自行在hof文件中查找或添加文件名。

【注】SLK6109的电显文件存储在`Vehicles\Anzeigen\RDx16-2`中，并以该目录为子目录。即若hof文件中表述电显贴图位置为`jhs\1-1.png`，则最终存储位置为`Vehicles\Anzeigen\RDx16-2\jhs\1-1.png`。

### 2.打开main.py文件，调整你需要的参数

参数调整都在第169行实现：

```python
main('.\src.txt',snow=0,kt=0,type = 1)
'''
snow 雪花标志 1 为自动在头显加入雪花标志
kt "空调" 字样  1 为自动加入空调字样
type : 0表示只需要在第三列写入终点，自动生成：线路名->终点站侧显
       1表示自由定义第三列
'''
```

默认保存位置为程序根目录下output文件夹。**请务必保证该文件夹存在后运行。**

### 3.运行main.py文件

依赖库：PIL numpy binascii copy

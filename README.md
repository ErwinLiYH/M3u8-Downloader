# M3u8 Downloader
A multithread m3u8 download module and the number of threads can decide by yourself. using how many threads is decide by your network and your device.

## 1. Install

```shell
pip install mder
```

## 2. Import

```python
import mder
```

## 3. Instance object and start download

```python
downloader = mder.m3u8_downloader(m3u8_file_path='./test.m3u8',temp_file_path='./',mp4_path='./test.mp4',num_of_threads=10)
# parameters
# 1.m3u8_file_path
# default : no default   (type : str)
# 2.temp_file_path
# default : '.'          (type : str)
# 3.mp4_path
# default : './test.mp4' (type : str)
# 4.num_of_threads
# default : 10           (type : int)

downloader.start()
# parameters
# 1.mod
# default : 0            (type : int)
# mod 0 means delete TS folder and m3u8 file if download completely
# mod 1 means delete m3u8 file only if download completely
# mod 2 means delete TS folder only if download completely
# mod 3 means reserve TS folder and m3u8 file if download completely
# 2.time_out
# default : 60           (type : int)(units : seconds)
# The time_out is the timeout in request.get(timeout=)
```

**before download**

the structure of ./ is:
```
.
├── test.m3u8
└── test.py
```

**when it is downloading**

the structure of ./ is:
```
.
├── TS
│   ├── qzCFnDUZE9_720_5308_0000.ts
│   ├── qzCFnDUZE9_720_5308_0001.ts
│   ├── qzCFnDUZE9_720_5308_0002.ts
│   ├── qzCFnDUZE9_720_5308_0003.ts
│   ├── qzCFnDUZE9_720_5308_0004.ts
│   ├── qzCFnDUZE9_720_5308_0005.ts
│   ├── qzCFnDUZE9_720_5308_0006.ts
│   ├── qzCFnDUZE9_720_5308_0007.ts
│   ├── qzCFnDUZE9_720_5308_0008.ts
│   ├── qzCFnDUZE9_720_5308_0009.ts
│   └── qzCFnDUZE9_720_5308_0010.ts  
├── test.m3u8
└── test.py
```
process bar:  <<\*>>  29% 500/1752 [01:33<04:02] <<\*>> 

TS is temp folder, all .ts file are in it. The path of it is %temp_file_path%/TS, in the test case, it is in ./TS. If the mission is not complete, the m3u8 file and TS folder will be reserved, you can instance a new downloader with corresponding TS folder and m3u8 file, and use the start() function to begin, in this way, the mission will go on.

**after download and download successfully**

the structure of ./ is:
```
.
├── test.mp4
└── test.py
```

If some .ts download failed, the module will redownload for 3 times, and the information will print to the command line

at last, the command line is like this:
```
<<*>>  99% 1737/1752 [05:35<00:22] <<*>>
thread0 Time out ERROR qzCFnDUZE9_720_5308_1710.ts
thread2 Time out ERROR qzCFnDUZE9_720_5308_1722.ts
thread0 redownload successfully qzCFnDUZE9_720_5308_1710.ts
<<*>>  99% 1738/1752 [06:20<03:19] <<*>>
thread2 redownload successfully qzCFnDUZE9_720_5308_1722.ts
<<*>> 100% 1752/1752 [06:26<00:00] <<*>>
downloading finished 100.00%
```
## 4.restart
If you want to restart a incomplete mission, you only should use the corresponding TS folder and .m3u8 file

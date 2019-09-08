# LineNotify.py



## Reference

* Refer to [jiankaiwang/Line_Notify_API.py](https://gist.github.com/jiankaiwang).
* Line Notify : https://notify-bot.line.me
* Line Sticker : https://devdocs.line.me/files/sticker_list.pdf



## Requirement

* Configuration file content (named **configuration.txt**)

```ini
[Name_1]
token = 1234567890abcdefghijklmnopqrstuvwxyz1234567

[Name_2]
token = 1234567890abcdefghijklmnopqrstuvwxyz1234567
```



## API

* Remember to comment the code on both sections, **input check** and **send the info**. (Because the source code is available for calling over command line.)

```python
# -----------------------------------------------------------------------------
# input check    
# -----------------------------------------------------------------------------        
#try:
#    opts, args = getopt.getopt(sys.argv[1:], "c:n:m:p:d:i:",\
#          ["conf=","name=","msg=","stkpkg=","stkid=","img="])
#    allOpts = {opts[i][0]: opts[i][1] for i in range(0, len(opts), 1)}
#except getopt.GetoptError as err:
#    sys.exit(1)

#configPath = ""

#...

#if retState.status_code == 200:
#    sys.exit(0)
#else:
#    print(sys.exc_info())
#    sys.exit(99)
```



* Constructor

```python
# 
# para@configPath : configuration file path
# para@envName    : name in the configuration file, e.g. Name_1 on the above requirement
# para@msg        : message to send
# 
lineApiObj = SendInfoToLineGroup(configPath, envName, msg)
```



* Get the token.

```python
# get and print the token from configuration file
print(lineApiObj.getToken())
```



* Only send the message.

```python
# 
# para@msg : message ready to send
#
retState = lineApiObj.sendMsgByOriginPackage(msg)
```



* Send the sticker.

```python
#
# para@msg    : message sent
# para@stkPkg : the sticker package
# para@stkId  : the sticker id in the specific package
#
retState = lineApiObj.sendMsgAndStickerByOriPkg(msg, stkPkg, stkId)
```



* Send the image.

```python
# 
# para@imgPath : the upload image path
#
retState = lineApiObj.sendMsgAndImgByOriPkg(msg, imgPath)
```



* return state

```shell
0 - Complete
1 - Lose necessary parameters or not found. (Necessary: conf, token_name, message)
2 - Either sticker package id or sticker id is error.
3 - Image is not found.
99- Unexpected error
```



## Command Line

```shell
$ python main.py <configuration> <token_name> <message> [<sticker>|<image>]
$ python LineNotify.py -c configuration.txt -n Dev -m "msg"
$ python LineNotify.py -c configuration.txt -n Dev -m "msg" -p 1 -d 114
$ python LineNotify.py -c configuration.txt -n Dev -m "msg" -i data/img.png
```


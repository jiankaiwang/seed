# FTPDownload.cs



### API description
---

* constructor (建構子)

```csharp
/*
 * parameter
 * 1. getFTPuser : ftp user name
 * 2. getFTPPwd : user password
 * 3. getFTPFullDwnPath : file path on the server, including file name and sub file name
 * 4. getFTPFullLocalPath : download file path on the client, include file name and sub file name
 * 5. getFTPReTryCount : count of retring connecting to server 
 * 6. dwnFileFlag : whether to download as a file
 */

public FTPDownload(
  String getFTPuser, 
  String getFTPPwd, 
  String getFTPFullDwnPath
)
 
public FTPDownload(
  String getFTPuser, 
  String getFTPPwd, 
  String getFTPFullDwnPath, 
  String getFTPFullLocalPath
)

public FTPDownload(
  String getFTPuser, 
  String getFTPPwd, 
  String getFTPFullDwnPath, 
  int getFTPReTryCount
)

public FTPDownload(
  String getFTPuser, 
  String getFTPPwd, 
  String getFTPFullDwnPath, 
  String getFTPFullLocalPath, 
  int getFTPReTryCount, 
  bool dwnFileFlag
)
```

* start to down file from a ftp server (開始自 FTP 伺服器下載資料)

```
// ------------------------------
// startFTPDownload()
// desc : main entry to download FTP file
// ret :
// -1 : ftp basic setting is not prepared
// -2 : ftp client can not login the server or file did not exist
// -3 : ftp download is not complete
// -4 : file exists but is can not be written
// -5 : file did not exist or file can not be created
// ------------------------------
public int startFTPDownload()
```

* get the content of downloaded file (取得 ftp 下載資料內容)

```
public String getFTPData()
```

### API Example
---

* Example.1 : get the content of downloaded file 

```
FTPDownload fd = new FTPDownload("user","pwd", "ftp://xyz:8020/file.txt");
int ftpStatus = fd.startFTPDownload();
if (ftpStatus == 0) {
    Console.WriteLine(fd.getFTPData());
}
```

* Example.2 : download file in detailed settings

```
FTPDownload fd = new FTPDownload("user","pwd", "ftp://xyz:8020/file.txt", "C:/Users/user1/Desktop/example.txt", 10, true);
int ftpStatus = fd.startFTPDownload();
```







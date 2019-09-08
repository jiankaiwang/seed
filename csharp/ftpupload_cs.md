# FTPUpload.cs



###API Requirement
---

* [FTPDownload.cs](https://github.com/jiankaiwang/seed/blob/master/csharp/FTPDownload.cs) is necessary
* [MD5HashChecksum.cs](https://github.com/jiankaiwang/seed/blob/master/csharp/MD5HashChecksum.cs) is necessary

### API description
---

* constructor (建構子)

```
/*
 * parameter
 * 1. getFTPuser : ftp user name
 * 2. getFTPPwd : user password
 * 3. getFTPFullUpdPath : upload file path on ftp server
 * 4. getFTPFullLocalPath : local file for upload
 * 5. getDataString : string data type for upload
 * 6. getCSFlag : do checksum flag
 * 7. getReTryCount : count of retrying to upload
 * 8. getUploadFromFile : the data content is from file or from string
 */

public FTPUpload(
  String getFTPuser, 
  String getFTPPwd, 
  String getFTPFullUpdPath, 
  String getFTPFullLocalPath
)

public FTPUpload(
  String getFTPuser, 
  String getFTPPwd, 
  String getFTPFullUpdPath, 
  String getFTPFullLocalPath, 
  bool getCSFlag
)

public FTPUpload(
  String getFTPuser, 
  String getFTPPwd, 
  String getFTPFullUpdPath, 
  String getFTPFullLocalPath, 
  int getReTryCount, 
  bool getCSFlag
)

public FTPUpload(
  String getFTPuser, 
  String getFTPPwd, 
  String getFTPFullUpdPath, 
  String getDataString, 
  int getReTryCount, 
  bool getUploadFromFile, 
  bool getCSFlag
)
```

* start to upload through FTP (開始 FTP 上傳)

```csharp
// ------------------------------
// startFTPUpload()
// desc : main entry to upload FTP file
// ret :
// -1 : local file does not exist
// -2 : upload setting is not correct
// -3 : can not access the ftp server or upload path did not exist
// -4 : upload is not complete
// -5 : checksum is not the same
// ------------------------------    
public int startFTPUpload()
```

### API Example
---

* Example.1 : upload a string to ftp server

```csharp
FTPUpload fd = new FTPUpload("user", "pwd", "ftp://xyz:21/example.txt", "Data test", 10, false, true);
int fdStatus = fd.startFTPUpload();
Console.WriteLine(String.Format("a{0}", fdStatus));
```

* Example.2 : upload from a file to ftp server in detailed settings

```csharp
FTPUpload fd = new FTPUpload("user", "pwd", "ftp://xyz:21/example.txt", "C:/Users/user1/Desktop/example1.txt", true);
int fdStatus = fd.startFTPUpload();
Console.WriteLine(String.Format("a{0}", fdStatus));
```

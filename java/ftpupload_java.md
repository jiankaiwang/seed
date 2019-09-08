# FTPUpload.java



### API description
---

* constructor (建構子)

```Java
/*
 * constructor 
 * parameter : 
 * 1. getHostName : ftp server host url or ip
 * 2. getFTPPort : ftp service port on ftp server
 * 3. getFtpUser : ftp user
 * 4. getFtpPwd : user password
 * 5. getFtpFulUploadFilePath : ftp file path on ftp server
 * 6. getFtpDataString : data string for uploading to ftp server
 * 7. getFtpFullLocalFilePath : local file path for uploading
 * 8. getUpFrFile : whether file preparing for upload is from file or not 
 */

public FTPUpload(
    String getHostName, 
    int getFTPPort, 
    String getFtpUser, 
    String getFtpPwd, 
    String getFtpFulUploadFilePath, 
    String getFtpDataString
)
    
public FTPUpload(
    String getHostName, 
    int getFTPPort, 
    String getFtpUser, 
    String getFtpPwd, 
    String getFtpFulUploadFilePath, 
    String getFtpFullLocalFilePath,
    boolean getUpFrFile
) 
```

* start to upload data to ftp server (將資料上傳至 ftp server)

```Java
public int startFTPUpload()
```

### API Example
---

* Example.1 : upload a data string

```Java
FTPUpload fu = new FTPUpload(
 "0.0.0.0", 21, "user", "pwd", "/home/example.txt", "example txt"
);
int ftpStatus = fu.startFTPUpload();
```

* Example.2 : upload a file

```Java
FTPUpload fu = new FTPUpload(
  "0.0.0.0", 21, "user", "pwd",
  "/home/example.txt", "C:\\Users\\user\\Desktop\\example.sql",true
);
int ftpStatus = fu.startFTPUpload();
```




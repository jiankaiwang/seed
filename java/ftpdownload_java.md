# FTPDownload.java



### API description
---

* constructor (建構子)

```Java
/*
 * constructor
 * parameter : 
 * 1. getFTPHost : ftp host url or IP
 * 2. getFTPPort : ftp service port on the ftp server
 * 3. getFTPUser : ftp user
 * 4. getFTPPwd : user password
 * 5. getFTPDwnFilePath : download file path on the server
 * 6. getFTPLocalFilePath : local file path for downloading
 */

// download as file and file name is the same
public FTPDownload (
    String getFTPHost,
    int getFTPPort,
    String getFTPUser,
    String getFTPPwd,
    String getFTPDwnFilePath,
    String getFTPLocalFilePath
) 

// download as data stream in string type
public FTPDownload (
    String getFTPHost,
    int getFTPPort,
    String getFTPUser,
    String getFTPPwd,
    String getFTPDwnFilePath
) 
```

* start to download data from ftp server (開始自 FTP 伺服器下載資料)

```Java
public int startFTPDownload()
```

* get the downloaded data content (取得下載資料的內容)

```Java
public String getFTPData()
```

###API Example
---

* Example.1 : get data content as string

```Java
FTPDownload fd = new FTPDownload(
  "host", port, "user", "password", "file path on the server"
  );
int ftpStatus = fd.startFTPDownload();
System.out.println(String.format("%s", fd.getFTPData()));
```

* Example.2 : download as file

```Java
FTPDownload fd = new FTPDownload(
  "host", port, "user", "password", "file path on the server", "file path on the local"
  );
int ftpStatus = fd.startFTPDownload();
```


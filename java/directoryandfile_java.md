# DirectoryAndFile.java



### API description
---

* constructor (建構子)

```Java
/*
 * parameter
 * 1. getPath : the path for checking whether it is a file or a directory
 * 2. getTryCreateFlag : if it is not existing, a bollean flag tries to create one
 */

// create a object with default getPath (empty) and getTryCreateFlag (false)
public DirectoryAndFile()

// create a object with a complete path and a creating flag
public DirectoryAndFile(String getPath, boolean getTryCreateFlag)
```

* check directory exists (確認資料夾是否存在)

```java
// use parameters passed on the beginning of creating a object
public int checkDirectoryExist()

// use new passed parameters
public int checkDirectoryExist(String checkDirectoryPath, boolean tryToCreateIfNotExist)
```

* check local file exists (確認本地端檔案是否存在)

```java
// use parameters passed on the beginning of creating a object
public int checkFileExist()

// use new passed parameters
public int checkFileExist(String getCheckFilePath, boolean tryToCreateIfNotExist)
```

### API example
---

* Example.1 : check a folder but not to create one if it is not existing

```java
DirectoryAndFile df = new DirectoryAndFile("C:/Users/user/Desktop/demo",false);
System.out.println(String.format("%d", df.checkDirectoryExist()));
```

* Example.2 : check a file and try to create one if it is not existing

```java
DirectoryAndFile df = new DirectoryAndFile();
System.out.println(String.format("%d", df.checkFileExist("C:/Users/user/Desktop/text.txt",true)));
```

# MD5HashChecksum.cs



* constructor (建構子)

```csharp
// no parameter
public MD5HashChecksum()

// one parameter : a template string
public MD5HashChecksum(String template)

// two parameter : a template and a compare strings
public MD5HashChecksum(String template, String compare)
```

* get md5 hash code of the string (取得一個字串的 MD5 雜湊値)

```csharp
// use default md5 hash object to get hash code
public String getMD5HashCode(String getInputStr)
 
// use passed (self-created) md5 hash object to get hash code
public String getMD5HashCode(MD5 passedMd5HashObj, String getInputStr)
```

* Verify one hash against one string (驗證 MD5 hash code 是否相同，checksum 相互驗證)

```csharp
// no parameter passed, use two strings-based constructor
bool VerifyMd5Hash()

// passed one string against template string
bool VerifyMd5Hash(String getInputStr)

// passed two strings and against each other
bool VerifyMd5Hash(String getInputStr, String getInputStr2)

// passed another md5 hash object and two strings against each other
bool VerifyMd5Hash(MD5 md5HashObj, String getInputStr, String getInputStr2)
```






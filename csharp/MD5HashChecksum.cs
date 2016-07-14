/* author : JinaKai Wang (http://jiankaiwang.no-ip.biz)
 * github : https://github.com/jiankaiwang/DetailScience
 * classification : C#
 * description : compute md5 hash code and checksum between two strings
 * Example to verify checksum :
 * --------------------------------------------------
// method.1 
MD5HashChecksum md5obj1 = new MD5HashChecksum("str1", "str1");
Console.WriteLine(String.Format("Hash compare between two strings is {0}.", md5obj1.VerifyMd5Hash().ToString()));

// method.2
MD5HashChecksum md5obj2 = new MD5HashChecksum("str1");
Console.WriteLine(String.Format("Hash compare between two strings is {0}.", md5obj2.VerifyMd5Hash("str1").ToString()));

// method.3
MD5HashChecksum md5obj3 = new MD5HashChecksum();
Console.WriteLine(String.Format("Hash compare between two strings is {0}.", md5obj3.VerifyMd5Hash("str1","str1").ToString()));

// method.4
MD5HashChecksum md5obj4 = new MD5HashChecksum();
MD5 newMd5Obj = MD5.Create();
Console.WriteLine(String.Format("Hash compare between two strings is {0}.", md5obj4.VerifyMd5Hash(newMd5Obj, "str1", "str1").ToString()));
 * --------------------------------------------------
 * Example to get MD5 hash code :
 * --------------------------------------------------
// method.1
MD5HashChecksum md5obj1 = new MD5HashChecksum();
String getHashCode = md5obj1.getMD5HashCode("str1");

// method.2
MD5HashChecksum md5obj2 = new MD5HashChecksum();
MD5 newMd5Obj = MD5.Create();
String getHashCode = md5obj2.getMD5HashCode(newMd5Obj, "str1");
 * --------------------------------------------------
 */

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

class MD5HashChecksum
{
    /*
     * desc : constructer
     * 1. no parameter
     * 2. one parameter : a template string
     * 3. two parameter : a template and a compare strings
     */

    public MD5HashChecksum()
    {
        templateStr = String.Empty;
        compareStr = String.Empty;
        md5HashObj = MD5.Create();
    }

    public MD5HashChecksum(String template)
    {
        templateStr = template;
        compareStr = String.Empty;
        md5HashObj = MD5.Create();
    }

    public MD5HashChecksum(String template, String compare)
    {
        templateStr = template;
        compareStr = compare;
        md5HashObj = MD5.Create();
    }

    /*
     * desc : private members
     */

    private String templateStr;
    private String compareStr;
    private MD5 md5HashObj;

    // ----------------------------
    // compare2Hash()
    // desc : body for two md5 hash code compare
    // parameter : one template string, one compare string
    // ----------------------------
    private bool compare2Hash(String tmpStrMd5, String cmpStrMd5) {
        // Create a StringComparer as an compare the hashes.
        StringComparer comparer = StringComparer.OrdinalIgnoreCase;

        if (0 == comparer.Compare(tmpStrMd5, cmpStrMd5)) {
            return true;
        }
        else {
            return false;
        }
    }

    // ----------------------------
    // hash2String()
    // desc : format byte[] data into string
    // parameter : one byte array data
    // ----------------------------
    private String hash2String(byte[] data) {
        // Create a new Stringbuilder to collect the bytes 
        // and also create a string
        StringBuilder sBuilder = new StringBuilder();

        // loop through each byte of the hashed byte data 
        // and format each one as a hexadecimal string.
        for (int i = 0; i < data.Length; i++)
        {
            sBuilder.Append(data[i].ToString("x2"));
        }

        // return the hexadecimal string.
        return sBuilder.ToString();
    }

    /*
     * desc : public members
     */

    // ----------------------------
    // getMD5HashCode()
    // desc : get md5 hash code
    // parameter :
    // 1. getMD5HashCode(String getInputStr) : use default MD5 hash object and get one input string
    // 2. getMD5HashCode(MD5 passedMd5HashObj, String getInputStr) : get passed MD5 hash object and one input string
    // ----------------------------
    public String getMD5HashCode(String getInputStr) {
        // Convert the input string to a byte array 
        // and compute the hash code
        byte[] data = md5HashObj.ComputeHash(Encoding.UTF8.GetBytes(getInputStr));

        return hash2String(data);
    }

    public String getMD5HashCode(MD5 passedMd5HashObj, String getInputStr)
    {
        // Convert the input string to a byte array 
        // and compute the hash code
        byte[] data = passedMd5HashObj.ComputeHash(Encoding.UTF8.GetBytes(getInputStr));

        return hash2String(data);
    }

    // -----------------------------
    // VerifyMd5Hash()
    // desc : Verify one hash against one string.
    // function :
    // 1. VerifyMd5Hash() : no parameter passed
    // 2. VerifyMd5Hash(String getInputStr) : passed one string against template string
    // 3. VerifyMd5Hash(String getInputStr, String getInputStr2) : passed two strings and against each other
    // 4. VerifyMd5Hash(MD5 md5HashObj, String getInputStr, String getInputStr2):
    //    passed another md5 hash object and two strings against each other
    // -----------------------------
    public bool VerifyMd5Hash()
    {
        String tmpStrMd5 = getMD5HashCode(templateStr);
        String cmpStrMd5 = getMD5HashCode(compareStr);

        return compare2Hash(tmpStrMd5, cmpStrMd5);
    }

    public bool VerifyMd5Hash(String getInputStr) {
        String tmpStrMd5 = getMD5HashCode(templateStr);
        String cmpStrMd5 = getMD5HashCode(getInputStr);

        return compare2Hash(tmpStrMd5, cmpStrMd5);
    }

    public bool VerifyMd5Hash(String getInputStr, String getInputStr2)
    {
        String tmpStrMd5 = getMD5HashCode(getInputStr);
        String cmpStrMd5 = getMD5HashCode(getInputStr2);

        return compare2Hash(tmpStrMd5, cmpStrMd5);
    }

    public bool VerifyMd5Hash(MD5 md5HashObj, String getInputStr, String getInputStr2)
    {

        String tmpStrMd5 = getMD5HashCode(md5HashObj, getInputStr);
        String cmpStrMd5 = getMD5HashCode(md5HashObj, getInputStr2);

        return compare2Hash(tmpStrMd5, cmpStrMd5);
    }

}

/* author : JinaKai Wang (http://jiankaiwang.no-ip.biz)
 * github : https://github.com/jiankaiwang/seed
 * classification : C#
 * description : upload data from to ftp server
 * necessary outer resource (x2) : 
 * 1. FTPDownload.cs (https://github.com/jiankaiwang/seed)
 * 2. MD5HashChecksum.cs (https://github.com/jiankaiwang/seed)
 * --------------------------------------------------
// method.1 
FTPUpload fd = new FTPUpload("user", "pwd", "ftp://xyz:21/example.txt", "Data test", 10, false, true);
int fdStatus = fd.startFTPUpload();
Console.WriteLine(String.Format("a{0}", fdStatus));
Console.Read();

// method.2
FTPUpload fd = new FTPUpload("user", "pwd", "ftp://xyz:21/example.txt", "C:/Users/user1/Desktop/example1.txt", true);
int fdStatus = fd.startFTPUpload();
Console.WriteLine(String.Format("a{0}", fdStatus));
Console.Read();
 * --------------------------------------------------
 */

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

class FTPUpload
{
    /*
    * constructor
    * parameter :
    * 1. getFTPuser : ftp user name
    * 2. getFTPPwd : user password
    * 3. getFTPFullUpdPath : upload file path on ftp server
    * 4. getFTPFullLocalPath : local file for upload
    * 5. getDataString : string data type for upload
    * 6. getCSFlag : do checksum flag
    * 7. getReTryCount : count of retrying to upload
    * 8. getUploadFromFile : the data content is from file or from string		
    */
    public FTPUpload(String getFTPuser, String getFTPPwd, String getFTPFullUpdPath, String getFTPFullLocalPath)
    {
        ftpUser = getFTPuser;
        ftpPwd = getFTPPwd;
        ftpFullUploadPath = getFTPFullUpdPath;
        ftpFullLocalPath = getFTPFullLocalPath;
        ftpDataString = String.Empty;
        retryCount = 10;
        checkSumFlag = true;
        uploadFromFile = true;
    }

    public FTPUpload(String getFTPuser, String getFTPPwd, String getFTPFullUpdPath, String getFTPFullLocalPath, bool getCSFlag) {
        ftpUser = getFTPuser;
        ftpPwd = getFTPPwd;
        ftpFullUploadPath = getFTPFullUpdPath;
        ftpFullLocalPath = getFTPFullLocalPath;
        ftpDataString = String.Empty;
        retryCount = 10;
        checkSumFlag = getCSFlag;
        uploadFromFile = true;
    }

    public FTPUpload(String getFTPuser, String getFTPPwd, String getFTPFullUpdPath, String getFTPFullLocalPath, int getReTryCount, bool getCSFlag) {
        ftpUser = getFTPuser;
        ftpPwd = getFTPPwd;
        ftpFullUploadPath = getFTPFullUpdPath;
        ftpFullLocalPath = getFTPFullLocalPath;
        ftpDataString = String.Empty;
        retryCount = getReTryCount;
        checkSumFlag = getCSFlag;
        uploadFromFile = true;
    }

    public FTPUpload(String getFTPuser, String getFTPPwd, String getFTPFullUpdPath, String getDataString, int getReTryCount, bool getUploadFromFile, bool getCSFlag)  {
        ftpUser = getFTPuser;
        ftpPwd = getFTPPwd;
        ftpFullUploadPath = getFTPFullUpdPath;
        ftpFullLocalPath = String.Empty;
        ftpDataString = getDataString;
        retryCount = getReTryCount;
        checkSumFlag = getCSFlag;
        uploadFromFile = getUploadFromFile;
    }

    /*
    * private members
    */

    private String ftpUser;
    private String ftpPwd;
    private String ftpFullUploadPath;
    private String ftpFullLocalPath;
    private String ftpDataString;
    private int retryCount;
    private bool checkSumFlag;
    private bool uploadFromFile;

    // ------------------------------
    // checkUploadSetting()
    // desc : check ftp upload setting is correct
    // ------------------------------
    private bool checkUploadSetting() {
        if(Convert.ToInt32(retryCount) <= 200 && Convert.ToInt32(retryCount) > 0) {
            return true;
        }
        else if (ftpUser.Length > 1 && ftpPwd.Length > 1 && ftpFullUploadPath.Length > 1 && ftpFullLocalPath.Length > 1 && uploadFromFile) {
            // upload from file
            return true;
        } else if (ftpUser.Length > 1 && ftpPwd.Length > 1 && ftpFullUploadPath.Length > 1 && ftpDataString.Length > 1 && (! uploadFromFile)) {
            // upload from data string
            return true;
        }
        else {
            return false;
        }
    }

    // ------------------------------
    // ftpUploadBody()
    // desc : ftp upload main body
    // ------------------------------
    private int ftpUploadBody(String getDataStr) {
        int ftpUploadStatus = 0;

        if (! checkUploadSetting()) {
            ftpUploadStatus = -1;
        } else {
            // Get the object used to communicate with the server.
            FtpWebRequest request = (FtpWebRequest)WebRequest.Create(ftpFullUploadPath);

            // set ftp connection type to uploadfile
            request.Method = WebRequestMethods.Ftp.UploadFile;

            // Use user and its password to login the ftp server
            request.Credentials = new NetworkCredential(ftpUser, ftpPwd);

            // Use UTF-8 as encoding type
            byte[] fileContents = System.Text.Encoding.UTF8.GetBytes(getDataStr);

            // get content length
            request.ContentLength = fileContents.Length;

            // make sure access to the remote is connected
            try {
                Stream requestStream = request.GetRequestStream();
                requestStream.Write(fileContents, 0, fileContents.Length);
                requestStream.Close();

                FtpWebResponse response = (FtpWebResponse)request.GetResponse();

                // regular expression to check 226 status reporting
                string pattern = "226";
                foreach (Match match in Regex.Matches(response.StatusDescription, pattern, RegexOptions.IgnoreCase)) {
                    if (! match.ToString().Equals(pattern)) {
                        ftpUploadStatus = -3;
                    }
                }

                response.Close();
            }
            catch {
                // can not access the ftp server or upload path did not exist
                ftpUploadStatus = -2;
            }
        }

        return ftpUploadStatus;
    }

    // ------------------------------
    // getLocalDataContent()
    // desc : get local file content
    // ------------------------------
    private String getLocalDataContent() {
        String fileContents = String.Empty;

        if (File.Exists(ftpFullLocalPath)) {
            // Copy the contents of the file to the request stream.
            StreamReader sourceStream = new StreamReader(ftpFullLocalPath);
            fileContents = sourceStream.ReadToEnd();
            sourceStream.Close();
        }
        else {
            fileContents = "-1";
        }

        return fileContents;
    }

    /*
    * public members
    */

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
    public int startFTPUpload() {
        int ftpStatus = 0;
        String getUploadDataString = String.Empty;
        int ftpUploadBodyFlag = 0;

        for (int rtCnt = 0; rtCnt < retryCount; rtCnt++) {
            if (uploadFromFile) {
                // from local file
                getUploadDataString = getLocalDataContent();

                if (getUploadDataString.Equals("-1")) {
                    // local file does not exist
                    ftpStatus = -1;
                    break;
                }
            }
            else {
                // from String
                getUploadDataString = ftpDataString;
            }

            ftpUploadBodyFlag = ftpUploadBody(getUploadDataString);

            if (ftpUploadBodyFlag == -1) {
                // upload setting is not correct
                ftpStatus = -2;
                break;
            } else if (ftpUploadBodyFlag == -2) {
                // can not access the ftp server or upload path did not exist
                ftpStatus = -3;
            } else if (ftpUploadBodyFlag == -3) {
                // upload is not complete
                ftpStatus = -4;
            }

            // checksum to make sure data upload is correct
            if (ftpStatus == 0 && checkSumFlag) {
                FTPDownload fd = new FTPDownload(ftpUser, ftpPwd, ftpFullUploadPath);
                int fdStatus = fd.startFTPDownload();
                if (fdStatus == 0) {
                    MD5HashChecksum md5obj1;
                    if (uploadFromFile) {
                        // from file
                        md5obj1 = new MD5HashChecksum(fd.getFTPData(), getLocalDataContent());
                    } else {
                        // from data string
                        md5obj1 = new MD5HashChecksum(fd.getFTPData(), ftpDataString);
                    }   
                    if (md5obj1.VerifyMd5Hash()) {
                        ftpStatus = 0;
                        break;
                    }
                    else {
                        // checksum is not the same
                        ftpStatus = -5;
                    }
                }
            }
        }

        return ftpStatus;
    }

}

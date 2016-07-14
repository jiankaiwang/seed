/* author : JinaKai Wang (http://jiankaiwang.no-ip.biz)
 * github : https://github.com/jiankaiwang/seed
 * classification : C#
 * description : download file from the ftp server
 * --------------------------------------------------
// method.1 
FTPDownload fd = new FTPDownload("user","pwd", "ftp://xyz:8020/file.txt");
int ftpStatus = fd.startFTPDownload();
if (ftpStatus == 0) {
    Console.WriteLine(fd.getFTPData());
}

// method.2
FTPDownload fd = new FTPDownload("user","pwd", "ftp://xyz:8020/file.txt", "C:/Users/user1/Desktop/example.txt", 10, true);
int ftpStatus = fd.startFTPDownload();
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

class FTPDownload
{
    /*
     * desc : constructor
     * parameter :
     * 1. use ftp user name, ftp password and file path on the server
     * 2. use ftp user name, ftp password, file path on the server and download file path on the client
     * 3. use ftp user name, ftp password, file path on the server and count of retring connecting to server 
     * 4. use ftp user name, ftp password, file path on the server, download file path on the client, count of retring connecting to server and whether download as a file
     */

    public FTPDownload(String getFTPuser, String getFTPPwd, String getFTPFullDwnPath) {
        ftpUser = getFTPuser;
        ftpPwd = getFTPPwd;
        ftpFullDownloadPath = getFTPFullDwnPath;
        ftpFullLocalPath = String.Empty;
        downloadAsFile = false;
        retryCount = 10;
        ftpData = String.Empty;
    }

    public FTPDownload(String getFTPuser, String getFTPPwd, String getFTPFullDwnPath, String getFTPFullLocalPath) {
        ftpUser = getFTPuser;
        ftpPwd = getFTPPwd;
        ftpFullDownloadPath = getFTPFullDwnPath;
        ftpFullLocalPath = getFTPFullLocalPath;
        downloadAsFile = true;
        retryCount = 10;
        ftpData = String.Empty;
    }

    public FTPDownload(String getFTPuser, String getFTPPwd, String getFTPFullDwnPath, int getFTPReTryCount) {
        ftpUser = getFTPuser;
        ftpPwd = getFTPPwd;
        ftpFullDownloadPath = getFTPFullDwnPath;
        ftpFullLocalPath = String.Empty;
        retryCount = getFTPReTryCount;
        downloadAsFile = false;
        ftpData = String.Empty;
    }

    public FTPDownload(String getFTPuser, String getFTPPwd, String getFTPFullDwnPath, String getFTPFullLocalPath, int getFTPReTryCount, bool dwnFileFlag) {
        ftpUser = getFTPuser;
        ftpPwd = getFTPPwd;
        ftpFullDownloadPath = getFTPFullDwnPath;
        ftpFullLocalPath = getFTPFullLocalPath;
        retryCount = getFTPReTryCount;
        downloadAsFile = dwnFileFlag;
        ftpData = String.Empty;
    }

    /*
     * private members
     */

    private String ftpUser;
    private String ftpPwd;
    private String ftpFullDownloadPath;
    private String ftpFullLocalPath;
    private int retryCount;
    private bool downloadAsFile;
    private String ftpData;

    // ------------------------------
    // checkFTPDownloadStatus()
    // desc : check basic parameters are available
    // ------------------------------
    private bool checkFTPDownloadStatus() {
        if (Convert.ToInt32(retryCount) <= 200 && Convert.ToInt32(retryCount) > 0) {
            return true;
        }
        else if (ftpUser.Length > 1 && ftpPwd.Length > 1 && ftpFullDownloadPath.Length > 1 && (!downloadAsFile)) {
            return true;
        }
        else if (ftpUser.Length > 1 && ftpPwd.Length > 1 && ftpFullDownloadPath.Length > 1 && ftpFullLocalPath.Length > 1) {
            return true;
        }
        else {
            return false;
        }
    }

    // ------------------------------
    // ftpDownloadBody()
    // desc : the body tries to download data on FTP server as String data type
    // ------------------------------
    private String ftpDownloadBody() {
        String retRes = String.Empty;

        if (!checkFTPDownloadStatus()) {
            retRes = "-1";
        }
        else {
            // Get the object used to communicate with the ftp server.
            FtpWebRequest request = (FtpWebRequest)WebRequest.Create(String.Format("{0}", ftpFullDownloadPath));

            // set ftp connection type is download
            request.Method = WebRequestMethods.Ftp.DownloadFile;

            // Login FTP Server
            request.Credentials = new NetworkCredential(ftpUser, ftpPwd);

            // get FTP response
            try {
                FtpWebResponse response = (FtpWebResponse)request.GetResponse();

                // convert to stream ready for data stream
                Stream responseStream = response.GetResponseStream();

                // create a object to read data by stream
                StreamReader reader = new StreamReader(responseStream);

                // get all data
                retRes = reader.ReadToEnd();

                // check download status
                string pattern = "226";
                foreach (Match match in Regex.Matches(response.StatusDescription, pattern, RegexOptions.IgnoreCase)) {
                    if (! match.Value.Equals(pattern)) {
                        retRes = "-3";
                    }
                }

                reader.Close();
                response.Close();
            }
            catch {
                retRes = "-2";
            }
        }

        return retRes;
    }


    // ------------------------------
    // writeIntoFile()
    // desc : try to write the string into a file
    // ------------------------------
    private int writeIntoFile(String getFTPData) {
        int retStatus = -1;

        for (int reTryIndex = 0; reTryIndex < 2; reTryIndex++) {
            if (File.Exists(ftpFullLocalPath)) {
                // file exists
                using (StreamWriter sw = new StreamWriter(ftpFullLocalPath)) {
                    sw.Write(getFTPData);
                    retStatus = 0;
                }
            }
            else {
                // file did not exist and try to create a new file
                try {
                    using (FileStream fs = File.Create(ftpFullLocalPath)) { }
                } catch { }
                retStatus = 2;
            }
        }

        return retStatus;
    }

    /*
     * public members
     */

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
    public int startFTPDownload() {
        int ftpStatus = 0;
        ftpData = String.Empty;

        for (int ftpUploadCount = 0; ftpUploadCount < retryCount; ftpUploadCount++) {
            // start to download the ftp data
            ftpData = ftpDownloadBody();

            if (ftpData.Equals("-1")) {
                // ftp basis status is not prepared
                ftpStatus = -1;
                break;
            }
            else if (ftpData.Equals("-2")) {
                // ftp client can not login the server or file did not exist
                ftpStatus = -2;
            }
            else if (ftpData.Equals("-3")) {
                // ftp download is not complete
                ftpStatus = -3;
            }
            else {
                // data is correct
                ftpStatus = 0;
                break;
            }
        }

        if (ftpStatus == 0 && downloadAsFile) {
            switch (writeIntoFile(ftpData)) {
                case 0:
                    // write file successfully
                    ftpStatus = 0;
                    break;
                case -1:
                    // file exists but is can not be written
                    ftpStatus = -4;
                    break;
                case 2:
                    ftpStatus = -5;
                    // file did not exist
                    break;
            }
        }

        return ftpStatus;
    }

    // ------------------------------
    // getFTPData()
    // desc : get String data type after downloading the file on ftp server
    // ------------------------------
    public String getFTPData() {
        return ftpData;
    }
}

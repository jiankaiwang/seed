/* author : JinaKai Wang (http://jiankaiwang.no-ip.biz)
 * github : https://github.com/jiankaiwang/seed
 * classification : Java
 * description : download data from ftp server
 * necessary outer resource (x1) : 
 * 1. commons-net-3.4.jar (org.apache) : FTPClient class
 * Example.1 : download as string
 * ----------
FTPDownload fd = new FTPDownload("host",port,"user","password","file path on the server");
int ftpStatus = fd.startFTPDownload();
System.out.println(String.format("%s", fd.getFTPData()));
 * ----------
 * Example.2 : download as file
 * ----------
FTPDownload fd = new FTPDownload("host",port,"user","password","file path on the server", "file path on the local");
int ftpStatus = fd.startFTPDownload();
 * ----------
 */

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.io.Writer;
import org.apache.commons.net.ftp.FTPClient;

class FTPDownload {
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
	
	public FTPDownload (
		String getFTPHost,
		int getFTPPort,
		String getFTPUser,
		String getFTPPwd,
		String getFTPDwnFilePath,
		String getFTPLocalFilePath
	) {
		// download as file and file name is the same 
		ftpHost = getFTPHost;
		ftpPort = getFTPPort;
		ftpUser = getFTPUser;
		ftpPwd = getFTPPwd;
		ftpFullDownloadFilePath = getFTPDwnFilePath;
		ftpFullLocalFilePath = getFTPLocalFilePath;
		setOthersParameters("dwnFileAndSameName");
	}
	
	public FTPDownload (
			String getFTPHost,
			int getFTPPort,
			String getFTPUser,
			String getFTPPwd,
			String getFTPDwnFilePath
		) {
			// download as data stream in string type
			ftpHost = getFTPHost;
			ftpPort = getFTPPort;
			ftpUser = getFTPUser;
			ftpPwd = getFTPPwd;
			ftpFullDownloadFilePath = getFTPDwnFilePath;
			setOthersParameters("dwnAsStringStream");
		}
	
	/*
	 * private members 
	 */
	
	private String ftpHost;
	private int ftpPort;
	private String ftpUser;
	private String ftpPwd;
	private String ftpFullDownloadFilePath;
	private String ftpFullLocalFilePath;
	private String ftpDataString;
	private boolean downloadAsFile;
	
	// default settings
	private int reTryCount;
	private int ftpKeepAliveTime;
	
	// ------------------------------
	// setOthersParameters()
	// desc : initial others settings
	// ------------------------------
	private void setOthersParameters(String initialOptions) {
		reTryCount = 10;
		ftpKeepAliveTime = 12000;
		
		switch(initialOptions) {
			default:
			case "dwnFileAndSameName":
				ftpDataString = "";
				downloadAsFile = true;
				break;
			case "dwnAsStringStream":
				ftpFullLocalFilePath = "";
				ftpDataString = "";
				downloadAsFile = false;
				break;
		}
	}
	
	// ------------------------------
	// setOthersParameters()
	// desc : check necessary settings available for ftp download
	// return :
	// 0 : success
	// -1 : basic settings are not available
	// -2 : parameter passed is error
	// ------------------------------
	private int checkFTPDownloadSettings() {
		int ftpDownloadStatus = 0;
		
		// check basic settings
		if(
			reTryCount <= 200 && reTryCount > 0 &&
			ftpHost.length() > 0 && ftpPort > 0 && 
			ftpUser.length() > 0 && ftpPwd.length() > 0 && 
			ftpFullDownloadFilePath.length() > 0
		) {
			if(downloadAsFile && ftpFullLocalFilePath.length() > 0) {
				// download as file
				ftpDownloadStatus = 0;
			} else if ((! downloadAsFile)) {
				// download as data string
				ftpDownloadStatus = 0;
			} else {
				ftpDownloadStatus = -2;
			}
		} else {
			ftpDownloadStatus = -1;
		}
		
		return ftpDownloadStatus;
	}	
	
	// ------------------------------
	// checkDirectoryExist()
	// desc : check local download path exists
	// 0 : success
	// -1 : ftp connection or ftp login is failure
	// -2 : downloading ftp data is failure
	// ------------------------------
	private int FTPDownloadBody() {
		
		int ftpDownloadStatus = 0;
		
		FTPClient ftpClient = new FTPClient();
		
		try {
			ftpClient.connect(ftpHost, ftpPort);
			
			if(! ftpClient.login(ftpUser, ftpPwd)) {
				// ftp login is failure
				return -1;
			}
			
			// time for ftp keep alive
			ftpClient.setControlKeepAliveTimeout(ftpKeepAliveTime);
			ftpClient.setConnectTimeout(ftpKeepAliveTime);
			ftpClient.setControlKeepAliveReplyTimeout(ftpKeepAliveTime);
					
			// enable passive mode to prevent 500 illegal port number
			ftpClient.enterLocalPassiveMode();
			
			// download ftp data as stream	
			BufferedReader input = new BufferedReader(new InputStreamReader(ftpClient.retrieveFileStream(ftpFullDownloadFilePath),"UTF-8"));
			int str = input.read();
			if(str != -1) {
				while(str >= 0) {
					ftpDataString = String.format("%s%c", ftpDataString, (char)str);
					str = input.read();
				}
				input.close();
			} else {
				input.close();
				return -2;
			}
             
            // ftp disconnect
            ftpClient.disconnect();
			
		} catch (IOException e) {
			// ftp connection is failure
			ftpDownloadStatus = -1;
		} 
		
		return ftpDownloadStatus;
	}
	
	// ------------------------------
	// writeStringToFile()
	// desc : write data string to a specific file
	// 0 : success
	// -1 : local file does not exist
	// -2 : file can not be written
	// ------------------------------
	private int writeStringToFile(String getStringData) {
		int writeDataStatus = 0;
		String writeFilePath = String.format("%s", ftpFullLocalFilePath);
		
		File fileDir = new File(writeFilePath);
		Writer out;
		try {
			out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(fileDir),"UTF-8"));
			out.append(getStringData);
			out.flush();
			out.close();
		} catch (UnsupportedEncodingException | FileNotFoundException e) {
			// nothing to do, already check file exist
			writeDataStatus = -1;
		} catch (IOException e) {
			// file can not write
			writeDataStatus = -2;
		}
		
		return writeDataStatus;
	}
	
	/*
	 * public members 
	 */
	
	// ------------------------------
	// getFTPData()
	// desc : get ftp file content
	// ------------------------------
	public String getFTPData() {
		return ftpDataString;
	}
	
	// ------------------------------
	// startFTPDownload()
	// desc : start to download data from ftp server
	// return
	// 0 : success
	// -1 : basic ftp download settings are error
	// -2 : downloading ftp data is failure
	// -3 : local file does not exist
	// -4 : file can not be written
	// ------------------------------
	public int startFTPDownload() {
		int ftpStatus = 0;
		int ftpDwnSetting = checkFTPDownloadSettings();
		
		if(ftpDwnSetting == 0) {
			// FTP download settings are correct
			for(int reTryCnt = 0 ; reTryCnt < reTryCount; reTryCnt ++) {
				// start to download data from FTP Server
				ftpStatus = FTPDownloadBody();	
				
				if(ftpStatus == 0) {
					if(downloadAsFile) {
						// download data as file 
						int writeIntoFileFlag = writeStringToFile(ftpDataString);
						
						if(writeIntoFileFlag == 0) {
							// write to a file successfully
							break;
						} else if (writeIntoFileFlag == -1) {
							// local file does not exist
							ftpStatus = -3;
						} else if (writeIntoFileFlag == -2) {
							// file can not be written
							ftpStatus = -4;
						}
					} else {
						// download data as string
						break;
					}
				} else if(ftpStatus == -1) {
					// ftp can not login
					break;
				} else if (ftpStatus == -2) {
					// downloading ftp data is failure
					continue;
				}
			}
		} else if(ftpDwnSetting == -1) {
			ftpStatus = -1;
		} else if(ftpDwnSetting == -2) {
			ftpStatus = -2;
		}
			
		return ftpStatus;
	}
	
	
}












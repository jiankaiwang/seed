/* author : JinaKai Wang (http://jiankaiwang.no-ip.biz)
 * github : https://github.com/jiankaiwang/seed
 * classification : Java
 * description : upload data to ftp server
 * necessary outer resource (x1) : 
 * 1. commons-net-3.4.jar (org.apache) : FTPClient class
 * Example.1
 * ----------
 FTPUpload fu = new FTPUpload("0.0.0.0",21,"user","pwd","/home/example.txt","example txt");
 int ftpStatus = fu.startFTPUpload();
 * ----------
 * Example.2
 * ----------
FTPUpload fu = new FTPUpload("0.0.0.0",21,"user","pwd","/home/example.txt","C:\\Users\\user\\Desktop\\example.sql",true);
int ftpStatus = fu.startFTPUpload();
System.out.println(String.valueOf(ftpStatus));
 * ----------
 */

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import org.apache.commons.net.ftp.FTPClient;

class FTPUpload {
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
	{
		// upload a data string
		ftpHost = getHostName;
		ftpPort = getFTPPort;
		ftpUser = getFtpUser;
		ftpPwd = getFtpPwd;
		ftpFulUploadFilePath = getFtpFulUploadFilePath; 
		ftpDataString = getFtpDataString;
		setInitialSetting("uploadFromString");
	}
	
	public FTPUpload(
			String getHostName, 
			int getFTPPort, 
			String getFtpUser, 
			String getFtpPwd, 
			String getFtpFulUploadFilePath, 
			String getFtpFullLocalFilePath,
			boolean getUpFrFile
		) 
	{
		// upload a file 
		ftpHost = getHostName;
		ftpPort = getFTPPort;
		ftpUser = getFtpUser;
		ftpPwd = getFtpPwd;
		ftpFulUploadFilePath = getFtpFulUploadFilePath; 
		ftpFullLocalFilePath = getFtpFullLocalFilePath;
		uploadFromFile = getUpFrFile;
		setInitialSetting("uploadFromFile");
	}
	
	/*
	 * private member
	 */
	
	private String ftpHost;
	private int ftpPort;
	private String ftpUser;
	private String ftpPwd;
	private String ftpFulUploadFilePath;
	private String ftpFullLocalFilePath;
    private String ftpDataString;
    private boolean uploadFromFile;
    
    // default setting
    private int retryCount;
    private int ftpKeepAliveTime;
    
    // ------------------------------
    // setInitialSetting()
    // desc : set several parameters for ftp connections in default
    // ------------------------------
    private void setInitialSetting(String getUploadOption) {
    	ftpKeepAliveTime = 120000;
    	retryCount = 10;
    	switch(getUploadOption) {
	    	case "uploadFromString":
	    		ftpFullLocalFilePath = "";
	    		uploadFromFile = false;
	    		break;
	    	case "uploadFromFile":
	    		ftpDataString = "";
	    		break;
    	}
    }
    
    // ------------------------------
    // checkFTPSettings()
    // desc : check basic FTP Settings are correct
    // ------------------------------
    private boolean checkFTPSettings() {
    	boolean checkStatus = false;
    	
    	// check basic settings
    	if(retryCount <= 200 && retryCount > 0 && 
    			ftpUser.length() > 0 && ftpPwd.length() > 0 && 
    			ftpFulUploadFilePath.length() > 0) 
    	{
    		if(uploadFromFile && ftpFullLocalFilePath.length() > 0 && checkFileExist(ftpFullLocalFilePath)) {
    			// upload from file
    			checkStatus = true;
    		} else if ((! uploadFromFile) && ftpDataString.length() > 0) {
    			// upload from string data
    			checkStatus = true;
    		} else {
    			checkStatus = false;
    		}
    	} else {
    		checkStatus = false;
    	}
    	
    	return checkStatus;
    }
    
    // ------------------------------
    // checkFileExist()
    // desc : check local file exists
    // ------------------------------
    private boolean checkFileExist(String getCheckFilePath) {
    	File fcheck = new File(String.format("%s", getCheckFilePath));
    	if(fcheck.exists()) {
    		return true;
    	} else {
    		return false;
    	}
    }
	
	// ------------------------------
    // ftpUploadBody()
    // desc : check basic FTP Settings are correct
    // return 
    // 0 : success
    // -1 : ftp connection is failure 
    // -2 : ftp upload failure
    // ------------------------------
    private int ftpUploadBody(InputStream getDataString) {   	
    	// create a ftp client object
    	FTPClient ftp = new FTPClient();
    	
  		try {
			ftp.connect(ftpHost, ftpPort);
			if(! ftp.login(ftpUser, ftpPwd)) {
				return -1;
			}
			
			// time for ftp keep alive
			ftp.setControlKeepAliveTimeout(ftpKeepAliveTime);
			ftp.setConnectTimeout(ftpKeepAliveTime);
			ftp.setControlKeepAliveReplyTimeout(ftpKeepAliveTime);
			
			// enable passive mode to prevent 500 illegal port number
	        ftp.enterLocalPassiveMode();
	        
	        // upload to the ftp server by input stream
	        if(! ftp.storeFile(ftpFulUploadFilePath, getDataString)) {
	        	// ftp connection close 
		        ftp.disconnect();
	        	return -2;
	        }
	        
	        // ftp connection close 
	        ftp.disconnect();
	        
		} catch (IOException e) {
			// ftp connection is failure 
			return -1;
		}
        
    	return 0;
    }
    
    /*
	 * public member
	 */
    
    // ------------------------------
    // startFTPUpload()
    // desc : start to upload data in FTP
    // return :
    // 0 : success
    // -1 : basic settings are failure
    // -2 : local file did not exist
    // ------------------------------
    public int startFTPUpload() {
    	int ftpStatus = 0;
    	
    	if(checkFTPSettings()) {	
	    	for(int reTryCnt = 0 ; reTryCnt < retryCount ; reTryCnt ++) {
	    		
	    		if(uploadFromFile) {
	    			try {
		    			ftpStatus = ftpUploadBody(new FileInputStream(String.format("%s", ftpFullLocalFilePath)));
		    			
		    			if(ftpStatus == 0) {
		    				// upload successfully
		    				break;
		    			} else if (ftpStatus == -2) {
		    				// directory not found
		    				break;
		    			}
    				} catch (IOException e) {
    					ftpStatus = -2;
	    				break;
    				}
	    		} else {
	    			
	    			// upload data from a string
	    			ftpStatus = ftpUploadBody(new ByteArrayInputStream(ftpDataString.getBytes(StandardCharsets.UTF_8)));
	    			
	    			if(ftpStatus == 0) {
	    				// upload successfully
	    				break;
	    			} else if (ftpStatus == -2) {
	    				// directory not found
	    				break;
	    			}
	    			
	    		}
	    	}
    	} else {
    		ftpStatus = -1;
    	}
    	
    	return ftpStatus;
    }
}




















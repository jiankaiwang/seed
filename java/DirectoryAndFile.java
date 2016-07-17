/* author : JinaKai Wang (http://jiankaiwang.no-ip.biz)
 * github : https://github.com/jiankaiwang/seed
 * classification : Java
 * description : Common Usage
 * defined class :
 * 1. DirectoryAndFile
 * necessary outer resource : none 
 * Example.1 : check a folder but not to create one if it is not existing
	 
	DirectoryAndFile df = new DirectoryAndFile("C:/Users/user/Desktop/demo",false);
	System.out.println(String.format("%d", df.checkDirectoryExist()));
  
 * Example.2 : check a file and try to create one if it is not existing
 
	DirectoryAndFile df = new DirectoryAndFile();
	System.out.println(String.format("%d", df.checkFileExist("C:/Users/user/Desktop/text.txt",true)));
	  
 */

import java.io.File;
import java.io.IOException;

class DirectoryAndFile {
	
	/*
	 * constructor 
	 * 1. getPath : the path for checking whether it is a file or a directory
	 * 2. getTryCreateFlag : if it is not existing, a bollean flag tries to create one
	 */
	
	public DirectoryAndFile() {
		checkPath = "";
		tryCreateIfNotExist = false;
	}
	
	public DirectoryAndFile(String getPath, boolean getTryCreateFlag) {
		checkPath = getPath;
		tryCreateIfNotExist = getTryCreateFlag;
	}
	
	/*
	 * private 
	 */
	
	private String checkPath;
	private boolean tryCreateIfNotExist;
	
	// ------------------------------
	// desc : check needed information is prepared
	// return
	// 0 : success
	// 1 : failure
	// ------------------------------
	private int checkSettingBody() {
		if(checkPath.length() > 0) {
			return 0;
		} else {
			return 1;
		}
	}

	// ------------------------------
	// desc : set information and call checkSettingBody() to check
	// return : the same with checkSettingBody()
	// ------------------------------
	private int checkSetting(String getCheckPath, boolean tryToCreateIfNotExist) {
		checkPath = getCheckPath;
		tryCreateIfNotExist = tryToCreateIfNotExist;
		
		return checkSettingBody();
	}
	
	// ------------------------------
	// checkDirectoryExistBody()
	// desc : check directory exists
	// return 
	// -2 : can not create a new directory
	// -1 : not exist or can not be created
	// 0 : exist and is also directory
	// 1 : exist but it is a file 
	// 2 : unrecognized path type
	// ------------------------------
	private int checkDirectoryExistBody(String checkDirectoryPath, boolean tryToCreateIfNotExist) {
		int checkFolderExist = -1;
		
		// create a file object 
		File directory = new File(checkDirectoryPath);
		
		for(int rtCreatFolder = 0 ; rtCreatFolder < 2 ; rtCreatFolder ++) {
			// loop if it is necessary to try to create
			
			if(directory.exists()) {
				// path exist
				
				if(directory.isDirectory()) {
					// is also directory
					checkFolderExist = 0;
				} else if (directory.isFile()) {
					// not directory but file
					checkFolderExist = 1;
				} else {
					// unrecognized path type
					checkFolderExist = 2;
				}
				break;
				
			} else if (tryToCreateIfNotExist) {
				checkFolderExist = -1;
				
				// trying to create once is enough
				// folder does not exist and try to create folders 
				if(! directory.mkdir()) {
					checkFolderExist = -2;
				}
			}
		}
		
		return checkFolderExist; 
	}
		
	// ------------------------------
	// checkFileExistBody()
	// desc : check local file exists
	// return 
	// -2 : file not exist and can not be created
	// -1 : file not exist
	// 0 : exist and also a file
	// 1 : exist but a directory
	// 2 : unrecognized path type
	// ------------------------------
	private int checkFileExistBody(String getCheckFilePath, boolean tryToCreateIfNotExist) {
		int checkFileExistFlag = -1;
		
		// create a file object
		File checkFile = new File(getCheckFilePath);
		
		for(int reCheckFile = 0 ; reCheckFile < 2 ; reCheckFile ++) {
			// loop if it is necessary to create a file
			
			if(checkFile.exists()) {
				// path exist
				
				if(checkFile.isFile()) {
					// it is also a file
					checkFileExistFlag = 0;
				} else if (checkFile.isDirectory()) {
					// it is a directory
					checkFileExistFlag = 1;
				} else {
					// unrecognized path type
					checkFileExistFlag = 2;
				}
				break;
			} else if (tryToCreateIfNotExist) {
				checkFileExistFlag = -1;

				// trying to create once is enough
				try {
					// file does not exist and try to create a new file 
					if(! checkFile.createNewFile()) {
						checkFileExistFlag = -2;
					}
				} catch (IOException e) {
					checkFileExistFlag = -1;
				}

			}
		}
		
		return checkFileExistFlag;
	}
	
	/*
	 * public 
	 */
	
	// ------------------------------
	// checkDirectoryExist()
	// desc : check directory exists
	// return : 
	// -2 ~ 2 : the same with checkDirectoryExistBody()
	// -99 : parameter error, need checkPath information
	// ------------------------------
	public int checkDirectoryExist() {
		if(checkSettingBody() == 0) {
			return checkDirectoryExistBody(checkPath, tryCreateIfNotExist);
		} else {
			return -99;
		}
	}
	
	public int checkDirectoryExist(String checkDirectoryPath, boolean tryToCreateIfNotExist) {
		if(checkSetting(checkDirectoryPath, tryToCreateIfNotExist) == 0) {
			return checkDirectoryExistBody(checkPath, tryCreateIfNotExist);
		} else {
			return -99;
		}
	}
	
	// ------------------------------
	// checkDirectoryExist()
	// desc : check local file exists
	// return : 
	// -2 ~ 2 : the same with checkDirectoryExistBody()
	// -99 : parameter error, need checkPath information
	// ------------------------------
	public int checkFileExist() {
		if(checkSettingBody() == 0) {
			return checkFileExistBody(checkPath, tryCreateIfNotExist);
		} else {
			return -99;
		}
	}
	
	public int checkFileExist(String getCheckFilePath, boolean tryToCreateIfNotExist) {
		if(checkSetting(getCheckFilePath, tryToCreateIfNotExist) == 0) {
			return checkFileExistBody(getCheckFilePath, tryToCreateIfNotExist);
		} else {
			return -99;
		}
	}
	
}

/* 
 * author : JinaKai Wang (https://welcome-jiankaiwang.rhcloud.com)
 * github : https://github.com/jiankaiwang/seed
 * classification : Java
 * description : Generate a Asymmetric Encryption Key Pair
 * 
 * necessary outer resource (x1) :
 * |- org.bouncycastle.openssl.PEMWriter
 * 
 * Example.1 : generate a key pair and save them into a local path
 * ----------

GenKeyPair genKP = new GenKeyPair("RSA",2048,true,"D:\\code\\java\\java-mars\\SignData\\data\\",true);
Map<String, String> genKPRes = genKP.generateKeyPairToLocalPath();
System.out.println(String.format("%s : %s", genKPRes.get("state"), genKPRes.get("info")));

 * ----------
 * Example.2 : return object containing both public key and private key
 * ----------

GenKeyPair genDSAKP = new GenKeyPair("DSA",1024,false,"",true);
Map<String, String> genDSAKPRes = genDSAKP.genKayPairAndReturnedAsPEMString(); 
System.out.println(String.format("%s : %s", genDSAKPRes.get("state"), genDSAKPRes.get("info")));
System.out.println(String.format("%s \n %s", genDSAKPRes.get("pubkey"), genDSAKPRes.get("prikey")));

 * ----------
 */

import java.util.List;
import java.io.File;
import java.io.FileOutputStream;
import java.io.ObjectOutputStream;
import java.io.StringWriter;
import java.nio.charset.Charset;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.SecureRandom;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import org.bouncycastle.openssl.PEMWriter;

public class GenKeyPair {
	
	private String genKeyAlgorithm = "";
	private int setAlgorithmLength = 0;
	private boolean setOutputToFile = false;
	private boolean setOutputAsPEMFile = false;
	private String outputToFilePath = "";
	
	/*
	 * desc : returned status
	 * retn :
	 * |- state : {success | failure}
	 * |- info : information message
	 */
	private Map<String, String> retStatus(String getStatus, String getInfo) {
		Map<String, String> map = new HashMap<String, String>();
		map.put("state", getStatus);
		map.put("info", getInfo);
		return map;
	}
	
	/*
	 * desc : constructor
	 * inpt : 
	 * |- getKeyAlgorithm : { DiffieHellman | DSA | RSA }
	 * |- getAlgorithmLen : DiffieHellman : 1024, DSA : 1024, RSA : {1024 | 2048}
	 * |- isOutputToFile : whether to output the public and private key
	 * 		|- true : write to the path with pub.key and pri.key
	 * 		|- false : return as KeyPair (including private key and public key)
	 * |- outputFilePath : the output path
	 * |- isPemFormat : whether output as PEM or DER file
	 */
	public GenKeyPair(
			String getKeyAlgorithm, 
			int getAlgorithmLen, 
			boolean isOutputToFile, 
			String outputFilePath,
			boolean isPemFormat
			) {
		genKeyAlgorithm = getKeyAlgorithm.toLowerCase();
		setAlgorithmLength = getAlgorithmLen;
		setOutputToFile = isOutputToFile;
		outputToFilePath = outputFilePath;
		setOutputAsPEMFile = isPemFormat;
	}
	
	/*
	 * desc : check input parameters available
	 * retn :
	 * |- state : {success | failure}
	 * |- info : information message 
	 */	
	public Map<String, String> checkInputParasAvailable() {		
		// check key algorithm
		List<String> keyAlrogithm = Arrays.asList("diffiehellman", "dsa", "rsa"); 
		if(! keyAlrogithm.contains(genKeyAlgorithm)) {
			return retStatus("failure", "Key Algorithm is not available. Supported list : DiffieHellman, DSA, RSA.");
		}
		
		// check key algorithm length
		Map<String, List<Integer>> map = new HashMap<String, List<Integer>>();
		map.put("diffiehellman", Arrays.asList(1024));
		map.put("dsa", Arrays.asList(1024));
		map.put("rsa", Arrays.asList(1024, 2048));
		
		if(! map.get(genKeyAlgorithm).contains(setAlgorithmLength)) {
			return retStatus("failure", "Algorithm is not available. DiffieHellman : 1024, DSA : 1024, RSA : {1024 | 2048}");			
		}
		
		// check output file path
		if(setOutputToFile && outputToFilePath.length() < 1 && (new File(outputToFilePath)).isDirectory()) {
			return retStatus("failure", "Output file path is not available.");
		}
		
		return retStatus("success", "Parameter succeeds.");
	}
	
	/*
	 * desc : generate a key pair and save them to a local path with pri.key and pub.key
	 * retn : 
	 * |- state : {success | failure}
	 * |- info : information message
	 * oupt :
	 * |- file : pub.key
	 * |- file : pri.key
	 */
	public Map<String, String> generateKeyPairToLocalPath() {
		
		Map<String, String> checkStatus = checkInputParasAvailable();
		if(! checkStatus.get("state").equals("success")) {
			return checkStatus;
		}
		
		try {
			KeyPairGenerator genKeyPair = KeyPairGenerator.getInstance(genKeyAlgorithm);
			genKeyPair.initialize(setAlgorithmLength, new SecureRandom()); 
			KeyPair kpKey = genKeyPair.generateKeyPair();
			PrivateKey prKey = kpKey.getPrivate();
			PublicKey puKey = kpKey.getPublic();
			
			if(! setOutputAsPEMFile) {
				ObjectOutputStream osPrivate = new ObjectOutputStream(
			    		new FileOutputStream(String.format("%spri.key", outputToFilePath))
			    );
			    ObjectOutputStream osPublic = new ObjectOutputStream(
			    		new FileOutputStream(String.format("%spub.key", outputToFilePath))
			    );
			    osPrivate.writeObject(prKey);
			    osPublic.writeObject(puKey);
	
			    osPrivate.close();
			    osPublic.close();
			} else {
				// private key
				// PEM file output
				StringWriter pemStrWriter = new StringWriter();
			    PEMWriter pemWriter = new PEMWriter(pemStrWriter);
		        pemWriter.writeObject(prKey);
		        pemWriter.flush();
		        pemWriter.close();
		        // write out the file
		        FileOutputStream prikeyOut = new FileOutputStream(String.format("%spri.key", outputToFilePath));
		        byte[] pemPriStrData = pemStrWriter.toString().getBytes(Charset.forName("UTF-8"));
		        prikeyOut.write(pemPriStrData);
		        prikeyOut.close();
		        //System.out.println(pemStrWriter.toString());
		        
				// public key
				// PEM file output
				StringWriter pemPubStrWriter = new StringWriter();
			    PEMWriter pemPubWriter = new PEMWriter(pemPubStrWriter);
			    pemPubWriter.writeObject(puKey);
			    pemPubWriter.flush();
			    pemPubWriter.close();			   
		        // write out the file
		        FileOutputStream pubkeyOut = new FileOutputStream(String.format("%spub.key", outputToFilePath));
		        byte[] pemPubStrData = pemPubStrWriter.toString().getBytes(Charset.forName("UTF-8"));
		        pubkeyOut.write(pemPubStrData);
		        pubkeyOut.close();	        
		        //System.out.println(pemPubStrWriter.toString());
			}
		}
		catch (Exception e) {
			return retStatus("failure","Generating a key pair is failure.");
		}

		return retStatus("success","Generating a key pair is complete.");
	}
	
	
	/*
	 * desc : generate a key pair without saving them into a local file
	 * retn : 
	 * |- state : {success | failure}
	 * |- info : information message
	 * |- prikey : string
	 * |- pubkey : string
	 */
	public Map<String, String> genKayPairAndReturnedAsPEMString() {
		
		Map<String, String> checkStatus = checkInputParasAvailable();
		if(! checkStatus.get("state").equals("success")) {
			return checkStatus;
		}
		
		if(setOutputToFile) {
			return retStatus("failure","The flag is set as 'output a key pair to the local path'.");
		} else if (! setOutputAsPEMFile) {
			return retStatus("failure","The flag is set as 'not to output a key pair as pem format'.");
		}
		
		try {
			KeyPairGenerator genKeyPair = KeyPairGenerator.getInstance(genKeyAlgorithm);
			genKeyPair.initialize(setAlgorithmLength, new SecureRandom()); 
			KeyPair kpKey = genKeyPair.generateKeyPair();
			PrivateKey prKey = kpKey.getPrivate();
			PublicKey puKey = kpKey.getPublic();
			
			Map<String, String> getRetStatus = retStatus("","");
			
			// private key
			// PEM file output
			StringWriter pemStrWriter = new StringWriter();
		    PEMWriter pemWriter = new PEMWriter(pemStrWriter);
	        pemWriter.writeObject(prKey);
	        pemWriter.flush();
	        pemWriter.close();
	        getRetStatus.put("prikey", pemStrWriter.toString());

			// public key
			// PEM file output
			StringWriter pemPubStrWriter = new StringWriter();
		    PEMWriter pemPubWriter = new PEMWriter(pemPubStrWriter);
		    pemPubWriter.writeObject(puKey);
		    pemPubWriter.flush();
		    pemPubWriter.close();			   
	        // write out the file
		    getRetStatus.put("pubkey", pemPubStrWriter.toString());
		    
		    getRetStatus.remove("state");
		    getRetStatus.put("state", "success");
		    getRetStatus.remove("info");
		    getRetStatus.put("info", "Generating a key pair is complete.");
		    
		    return getRetStatus;
		        
		}
		catch (Exception e) {
			return retStatus("failure","Generating a key pair is failure.");
		}
	
	}
		
}

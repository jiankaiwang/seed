# GenKeyPair.java



### Dependency
---

* org.bouncycastle.openssl.PEMWriter

### Constructor
---

```java
/*
 * desc : constructor
 * inpt : 
 * |- getKeyAlgorithm : { DiffieHellman | DSA | RSA }
 * |- getAlgorithmLen : DiffieHellman : 1024, DSA : 1024, RSA : {1024 | 2048}
 * |- isOutputToFile : whether to output the public and private key
 *     |- true : write to the path with pub.key and pri.key
 *     |- false : return as KeyPair (including private key and public key)
 * |- outputFilePath : the output path
 * |- isPemFormat : whether output as PEM or DER file
 */
public GenKeyPair (
        String getKeyAlgorithm, 
        int getAlgorithmLen, 
        boolean isOutputToFile, 
        String outputFilePath,
        boolean isPemFormat
    )
```

### API description
---

```java
/*
 * desc : check input parameters available
 * retn : 
 * |- state : {success | failure}
 * |- info : information message
 */	
public Map<String, String> checkInputParasAvailable()

/*
 * desc : generate a key pair and save them to a local path with pri.key and pub.key 
 * retn :
 * |- state : {success | failure}
 * |- info : information message 
 * oupt :
 * |- file : pub.key
 * |- file : pri.key
 */
public Map<String, String> generateKeyPairToLocalPath()

/*
 * desc : generate a key pair without saving them into a local file 
 * retn :
 * |- state : {success | failure}
 * |- info : information message 
 * |- prikey : string
 * |- pubkey : string
 */
public Map<String, String> genKayPairAndReturnedAsPEMString()
```

### Example
---

```java
// Example.1 : generate a key pair and save them into a local path
GenKeyPair genKP = new GenKeyPair("RSA",2048,true,"D:\\code\\java\\java-mars\\SignData\\data\\",true);
Map<String, String> genKPRes = genKP.generateKeyPairToLocalPath();
System.out.println(String.format("%s : %s", genKPRes.get("state"), genKPRes.get("info")));

// Example.2 : return object containing both public key and private key
GenKeyPair genDSAKP = new GenKeyPair("DSA",1024,false,"",true);
Map<String, String> genDSAKPRes = genDSAKP.genKayPairAndReturnedAsPEMString(); 
System.out.println(String.format("%s : %s", genDSAKPRes.get("state"), genDSAKPRes.get("info")));
System.out.println(String.format("%s \n %s", genDSAKPRes.get("pubkey"), genDSAKPRes.get("prikey")));
```
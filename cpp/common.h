#include <string>
#include <vector>

namespace std {

    /*
    * description : string is split by delimit words
    * parameter :
    * |- getStr@String : "string prepared for being split"
    * |- delimit@String : "split char in the string"
    * return : vector<string>
    * example :
    * vector<string> getVect = strsplit("string name, name2(string), name3(c-string);","(;");
    */
    vector<string> strsplit(string getStr, string delimit) {
        vector<string> retVect = vector<string>();
        int startIndex = -1;
        bool inDelimit = false;
        int checkIndex = 0;
        for(int charIndex = 0 ; charIndex < getStr.length() ; charIndex ++) {
            if(startIndex == -1) {
                // set the substring beginning index
                startIndex = charIndex;
            }
            // initial flag
            inDelimit = false;
            checkIndex = 0;
            while(checkIndex < delimit.length()) {
                if(getStr[charIndex] == delimit[checkIndex]) {
                    // match the delimit char
                    inDelimit = true;
                    break;
                }
                // move to next character
                checkIndex ++;
            }
            // match delimit character, save the substring to the vector
            if(inDelimit && ((charIndex - startIndex) != 0)) {
                // first find, first output
                retVect.push_back(getStr.substr(startIndex, charIndex-startIndex));
                // initial to find next substring
                startIndex = -1;
            }
            // final word to check the substring
            if(charIndex == getStr.length()-1 && ((charIndex - startIndex) != 0)) {
                // push the final string no matter whether matching or not
                if(charIndex + 1 < getStr.length()) {
                    retVect.push_back(getStr.substr(startIndex, ++charIndex-startIndex));
                }
            }
        }
        return retVect;
    }
}

/*
* author : jiankaiwang (https://welcome-jiankaiwang.rhcloud.com/)
* project : seed (https://github.com/jiankaiwang/seed)
* reference : seed (https://www.gitbook.com/book/jiankaiwang/seed/details)
*/

using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace webapiJsonNet.Models
{
    class googlesheetsapikey
    {

        private string sheetId = "";
        private string range = "";
        private string apikey = "";

        // 0 : [ [column name], [data.1], [data.2], [data.3], ... ]
        // 1 : [ { colname.1 : data-1.column.1, colname.2 : data-1.column.2 }, { colname.1 : data-2.column.1 }, ... ]
        // 99 : original google response
        private int retDataFormat = 0;
        private string usrAddress = "";

        /*
        * desc : fetch raw data from google sheets
        */
        private string[] fetRawData() {

            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(usrAddress);
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();

            // [0] : {success|failure}
            // [1] : data message
            var data = new string[] {"", ""};

            if (response.StatusCode == HttpStatusCode.OK)
            {

                // fetch data as a stream
                Stream receiveStream = response.GetResponseStream();
                StreamReader readStream = null;

                if (response.CharacterSet == null)
                {
                    readStream = new StreamReader(receiveStream);
                }
                else {
                    // fetch data encoding type
                    readStream = new StreamReader(receiveStream, Encoding.GetEncoding(response.CharacterSet));
                }

                data[0] = "success";
                data[1] = readStream.ReadToEnd();

                response.Close();
                readStream.Close();
            }
            else {

                data[0] = "failure";
                data[1] = "";
            }

            return data;
        }

        /*
        * desc : parse the "values" component on raw data into dictionary-based json data
        */
        private string parseIntoDictJsonData(string getData) {
            JObject obj = JsonConvert.DeserializeObject<JObject>(getData);

            // add columns
            DataTable dt = new DataTable();
            int countCol = 0;

            foreach (var colname in obj["values"][0])
            {
                var column = new DataColumn();
                column.DataType = System.Type.GetType("System.String");
                column.ColumnName = colname.ToString();
                column.ReadOnly = true;
                column.Unique = false;
                // Add the Column to the DataColumnCollection.
                dt.Columns.Add(column);
                countCol += 1;
            }

            // them to the DataTable
            bool firstFlag = true;
            foreach (var row in obj["values"])
            {
                if (firstFlag) {
                    firstFlag = false;
                    continue;
                }

                var insertRow = dt.NewRow();

                // prevent the first row is empty
                if (row[0].ToString().Length < 1) {
                    continue;
                }

                for (int i = 0; i < countCol; i++) {
                    insertRow[i] = row[i].ToString();
                }

                // add into the data table
                dt.Rows.Add(insertRow);
            }

            // parese dataTable into json format in dictionary type
            var jsonData = JsonConvert.SerializeObject(dt, Newtonsoft.Json.Formatting.Indented);
            return jsonData;
        }

        /*
        * desc : parse the "values" component on raw data into json data
        */
        private string parseIntoListJsonData(string getData) {
            JObject obj = JsonConvert.DeserializeObject<JObject>(getData);
            return obj["values"].ToString();
        }

        /*
        * desc : constructor
        * inpt : 
        * |- getRetDataFormat : {0 | 1 | 99}
        */
        public googlesheetsapikey(string getSheetId, string getRange, string getApiKey, int getRetDataFormat)
        {
            sheetId = getSheetId;
            range = getRange;
            apikey = getApiKey;

            switch (getRetDataFormat) {
                case 0:
                    retDataFormat = 0;
                    break;
                case 1:
                    retDataFormat = 1;
                    break;
                default:
                case 99:
                    retDataFormat = 99;
                    break;
            }

            // combine components
            usrAddress = string.Format("https://sheets.googleapis.com/v4/spreadsheets/{0}/values/{1}?key={2}", sheetId, range, apikey);
        }

        public HttpResponseMessage fetchData() {

            string[] rawData = fetRawData();
            HttpResponseMessage resp = new HttpResponseMessage();
            StringContent sc = null;

            if (rawData[0].Equals("success"))
            {

                switch (retDataFormat) {
                    case 0:
                        // returning "values" in the dictionary type
                        sc = new StringContent(parseIntoDictJsonData(rawData[1]));
                        break;
                    case 1:
                        // origin response but returning "values" only
                        sc = new StringContent(parseIntoListJsonData(rawData[1]));
                        break;
                    case 99:
                        // origin response
                        sc = new StringContent(rawData[1]);
                        break;
                }
            }
            else {
                sc = new StringContent("{'statue' : 'The api connection status is 200 Ok.', 'error' : 'The google api response is error.'}");
            }

            sc.Headers.ContentType = new MediaTypeHeaderValue("application/json");
            resp.Content = sc;
            return resp;
        }

    }
}
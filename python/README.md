# Python



## py2psql.py
* A class implements select, insert, update and delete operations to postgresql.
* Dependent: psycopg2



## REQUESTMETHOD.py

* A class implements sending GET/POST/PUT/DELETE requests and receiving the server responses.
* Collaboration with PHP (REQUESTMETHOD.php)
* Dependent : urllib, urllib2, json



## REQUESTMETHOD2.py

* A class implements sending GET/POST/PUT/DELETE requests and receiving the server responses.
* Collaboration with PHP (REQUESTMETHOD.php)
* Dependent : urllib2, requests, TEXTCODING(also in seed project)



## TEXTCODING.py

* Several methods transform text among different encoding.



## py2mysql.py

* A class implements select, insert, update and delete operations to mysql.
* Dependent: mysql.connector



## GoogleSheetsApiByOAuth.py

* related to Google Sheet API (v4) by OAuth



##  LineNotify.py

* Send the message, the sticker, and the image to the specific LINE group.




## TF1_FrozenModel.py 

*   We provided several useful tools for using TF frozen model, including listing operations, listing nodes, transforming the model into tflite one, etc. We hope this script can bring you easier way access to the portable model.
*   Dependency: tensorflow (>= 1.13.2)
# TimeCounter.js



### API
---

* The date after adding several days (加上數日後的日期時間)

```javascript
Date currentDateAddDays(var addDays)
```

* The date after adding several hours (加上數小時後的日期時間)

```javascript
Date currentDateAddHours(var addHours)
```

* The date after adding several minutes (加上數分鐘後的日期時間)

```javascript
Date currentDateAddMinutes(var addMinutes)
```

* The date after adding several seconds (加上數秒鐘後的日期時間)

```javascript
Date currentDateAddSeconds(var addSeconds)
```

* The date after adding several days to the specific date (針對某一時刻加上數日後的日期時間)

```javascript
Date addDays(Date getDate, var getDays)
```

* The date after adding several hours to the specific date (針對某一時刻加上數小時後的日期時間)

```javascript
Date addHours(Date getDate, var getHours)
```

* The date after adding several minutes to the specific date (針對某一時刻加上數分鐘後的日期時間)

```javascript
Date addMinutes(Date getDate, var getMinutes)
```

* The date after adding several seconds to the specific date (針對某一時刻加上數秒鐘後的日期時間)

```javascript
Date addSeconds(Date getDate, var getSeconds)
```

* Get the current year (取得今日年份)

```javascript
var getCrtYear(Date getDate)
```

* Get the current month (取得今日月份)

```javascript
var getCrtMonth(Date getDate)
```

* Get the current date (取得今日日期)

```javascript
var getCrtDate(Date getDate)
```

* Get the current hour (取得現在幾時)

```javascript
var getCrtHour(Date getDate)
```

* Get the current minute (取得現在幾分)

```javascript
var getCrtMinute(Date getDate)
```

* Get the current second (取得現在幾秒)

```javascript
var getCrtSecond(Date getDate)
```

* Get the current day (取得今日星期)

```javascript
// return: 0 - 6
var getCrtDay(Date getDate)
```

* Get the current day by alpha (取得今日星期，以英文縮寫回傳)

```javascript
// return: "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"
var getCrtAlphaDay(Date getDate)
```

* Set year, month and date (設定年月日)

```javascript
Date setYearMonthDate(Date getDate, var getYMD)
```

* set hour, minute and second (設定時分秒)

```javascript
Date setHourMinuteSecond(Date getDate, var getHMS)
```

* format seconds to Day:Hour:Minute:Second

```javascript
# inpt
# |- second : total seconds
# |- format : { format | H, HH, M, MM, S, SS, dd:HH:MM:SS, HH:MM:SS, MM:SS }
string formatSecond(second, format)
```



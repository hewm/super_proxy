# super_proxy

## status: In development

## Custom demand list [To be determined]

## API interface

### /proxy_all   
**meaning Get all proxy**

#### parameter 

| key |type  |  val|
| --- | --- | --- |
| type | str | http or https |

### /proxy_random   
**Randomly get a few proxy**

#### parameter 

| key |type  |  val|
| --- | --- | --- |
| amount | int | 1-->n |

### /del_proxy  
**Proactively deleting agents**
#### parameter 
| key |type  |  val|
| --- | --- | --- |
| pl | str | http://xxx.xxx.xxx.xxx:xxxx |


### /add_host  
**Add host**
#### parameter 
| key |type  |  val|
| --- | --- | --- |
| host | str |youtube.com |
| amount | int |1-->n|
| timeout | int |1s-->60s|
| type | str |http or https|

### /del_host
**del host**

| key |type  |  val|
| --- | --- | --- |
| host | str |youtube.com |

## Features

1. get the proxy scripting [all acquisition proxy scripts are placed in a folder, periodically execute the script under the folder to get the agent unified storage]
2. before the storage through the scrap pool, the waste pool storage Baidu request different agents, directly filter before the next storage
3. Cyclically verify all agents. Request for aggressive filtering that already exists and exists in the retirement pool. Baidu can request to leave
4. After the request to add the domain, a new collection is created to arrange a dedicated proxy list for this domain.
5. Continuously check all available agents of the available agent library, arrange the expired agents into the scrap library, and delete them in each domain synchronously.
6. control traffic [control agent number of available library agents] [http and https]
7. one key to read all configurations

## DB
redis

0db

set

set name

| name |type  |  meaning|  Remarks|val|
| --- | --- | --- | --- | --- |
| HTTP_Unprocessed  | set |Unprocessed HTTP proxy  | | |
| HTTPS_Unprocessed   | set |Unprocessed HTTPS proxy  | | |
| HTTP_Processed    | set |Verified HTTP proxy  | | |
| HTTPS_Processed    | set |Verified HTTPS proxy  | | |
| HTTP_Scrapped     | set |Unavailable HTTP [retired library]  |30 days per timeout | |
| HTTPS_Scrapped     | set |Unavailable HTTPS [retired library]  |30 days per timeout | |
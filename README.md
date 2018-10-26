### i4-projekt-wissenstechnologien-tweet2vec version 0.5

Author: Matthias "matthiaskrgr" Krüger

Email: `makru117@hhu.de`

Requirements:


The script will need a twitter access token.
https://dev.twitter.com/oauth/overview/application-owner-access-tokens
The file ````my_config.py```` must look as follows:
````
consumer_key = "xxxxxx"
consumer_secret = "xxxxxxxxxxxxxxxxx"
access_token = "xxxxxxxxxxxxxxxxx"
access_token_secret = "xxxxxxxxxxxxxxxxx"
````

The file my_config.py must be located in the repo root.


External python modules:
````
tweepy  http://docs.tweepy.org/en/v3.5.0/getting_started.html
emoji   https://github.com/carpedm20/emoji/
````

Usage:
````
./tweet2vec.py HHU_de 15
First parameter is the twitter account name/id
Second parameter (optional, defaults to 10) the number of tweets to download
````


License:
Copyright 2018 Matthias Krüger

Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
<LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
option. All files in the project carrying such notice may not be
copied, modified, or distributed except according to those terms.

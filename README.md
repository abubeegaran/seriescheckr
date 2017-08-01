# seriescheckr
Simple script to check updates of your favorite tv series on [https://psarips.com](https://psarips.com) and recieve push notifications through Pushbullet. 

Add/change urls by editing `urls.txt` . 

Prerequisites: 

    requests==2.18.1
	pushbullet.py==0.11.0
	beautifulsoup4==4.6.0

Pushbullet API key: 

 - Navigate to `www.pushbullet.com > My Account > Settings > Account > Access Tokens` . 
 - Generate an API key by clicking  `Create Access Token` . 
 - Paste obtained API key in `config.py` . 
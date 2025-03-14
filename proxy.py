import requests 

# Initialise proxy and url. 
proxy = 'http://41.59.90.171:80'
url = 'https://ipecho.net/plain'

# Send a GET request to the url and 
# pass the proxy as parameter. 
page = requests.get(url, 
					proxies={"http": proxy, "https": proxy}) 

# Prints the content of the requested url. 
print(page.text) 

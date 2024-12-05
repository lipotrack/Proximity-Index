import requests

def values():
    url = "https://api.wto.org/timeseries/v1/data?i=ITS_MTV_AX&subscription-key=1a2d93a67ee94e42a7c1fd26136ef2c0"
    response = requests.get(url).json()
    print (response)


values()
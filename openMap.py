import http.client

server = 'dapi.kakao.com'
key = '5f6281e1df82664b7985e8d65d2c46f5'
header = {'Authorization': 'KakaoAK '+key}

def mapOpen():
    conn = http.client.HTTPSConnection(server)
    conn.request("GET", "/v2/local/geo/coord2regioncode.xml?x=127.1086228&y=37.4012191")
    req = conn.getresponse()


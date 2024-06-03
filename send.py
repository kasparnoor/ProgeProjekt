import requests

url = 'http://192.168.1.205:8080/post'
myobj = {'description': 'gay kissing musi'}

response = requests.post(url, json=myobj)

if response.status_code == 200:
    with open('received_video.mp4', 'wb') as f:
        f.write(response.content)
    print('Video saved as received_video.mp4')
else:
    print(f'Failed to retrieve video. Status code: {response.status_code}')

import requests

server_ip = 'http://3.122.27.254/solution'
file_to_send = open('output', 'r')
fild_dict = {'solution': file_to_send}
r = requests.post(server_ip, data = file_to_send.read())
print(r.text)

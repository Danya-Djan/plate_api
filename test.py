import requests


headers = {"Authorization": "Bearer YOUR_TOKEN"}

print(requests.get('http://79.137.194.54/plates', headers=headers).json())

print("|||||||||||||||||||||||||||||||||||||||||||||")

print(requests.get('http://79.137.194.54/plate/generate/5', headers=headers).json())

print("|||||||||||||||||||||||||||||||||||||||||||||")

print(requests.get('http://79.137.194.54/plates', headers=headers).json())

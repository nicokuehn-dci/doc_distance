from rest_framework.test import APIClient
from django.urls import reverse

c = APIClient()
res = c.post(reverse('word-frequencies'), {"payload": ["h", "e", "l", "l", "o"]}, format='json')
print('status:', res.status_code)
print('content-type:', res['Content-Type'])
print('content:')
print(res.content.decode())

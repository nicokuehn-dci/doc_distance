from distance.serializers import WordFreqSerializer

s = WordFreqSerializer(data={"payload": ["h", "e", "l", "l", "o"]})
print('is_valid:', s.is_valid())
print('errors:', s.errors)
from distance.serializers import WordFreqSerializer
s = WordFreqSerializer(data={payload: [h,e,l,l,o]})
print('is_valid:', s.is_valid())
print('errors:', s.errors)

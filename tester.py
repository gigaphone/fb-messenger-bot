from app import answer
import json

f = open('qa.json')
answers = json.load(f)
f.close()

i = 0
for key in answers.keys():
    i += 1
    print "(" + str(i) + ") " + key
    for j in range(1,20):
        answer(key)
        #print key + ":" + answer(key)
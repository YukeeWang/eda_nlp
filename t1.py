import synonyms
res = synonyms.seg("中文近义词工具包")
print(res[0])
words = synonyms.nearby("人脸")
for word, simliary in zip(words[0],words[1]):
    if simliary >0.8:
        print(word)
simliary = list(filter(lambda x: x>0.8, words[1]))
print(simliary)
newwords = words[0][:len(simliary)]
print(newwords)

print(synonyms.nearby("NOT_EXIST"))
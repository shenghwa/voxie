import jieba
from wordcloud import WordCloud
f = open('inputWord.txt', 'r')
txt = f.read()
words = jieba.lcut(txt)
new_text = ''.join(words)
wordcloud = WordCloud(background_color="#F0F8FF", width=1600, height=900, max_words=50).generate(new_text)
wordcloud.to_file('C:/Users/xw466/Documents/HBuilderProjects/Norma/src/static/wordCloud.jpg')

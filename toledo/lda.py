import pandas as pd
import re
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA

df = pd.read_csv('3000first.csv', engine='python', encoding='utf-8')
df['post_raw'] = df['post'].copy()

# Remove punctuation
print('%s\tRemoving punctuation' % datetime.now().time())
df['post'] = df['post_raw'].map(lambda x: re.sub('[,\\.!?;]', ' ', x))
df['post'] = df['post'].map(lambda x: re.sub('[\'„“‟”’"‘❛❜״]', '', x))

# Remove stopwords
print('%s\tRemoving stopwords' % datetime.now().time())
stopwords = open('stopwords.txt', 'r').read().splitlines()
df['post'] = df['post'].map(lambda x: ' '.join(
    [y for y in x.split() if y not in stopwords]
))

# Remove inflections
print('%s\tRemoving inflections' % datetime.now().time())
df['post'] = df['post'].map(lambda x: x.replace('ן', 'נ'))
df['post'] = df['post'].map(lambda x: x.replace('ם', 'מ'))
df['post'] = df['post'].map(lambda x: x.replace('ך', 'כ'))
df['post'] = df['post'].map(lambda x: x.replace('ף', 'פ'))
df['post'] = df['post'].map(lambda x: x.replace('ץ', 'צ'))
df['post'] = df['post'].map(
    lambda x: re.sub('\\b([^\\s]{3,})(ות|ימ)\\b', '\\g<1>', x))
df['post'] = df['post'].map(
    lambda x: re.sub('\\b(ה|ב|ל)([^\\s]{3,})\\b', '\\g<2>', x))
df['post'] = df['post'].map(
    lambda x: re.sub('\\bו([^\\s]{3,})\\b', '\\g<1>', x))

df_g = df.groupby(['thread'])['post'].apply(' '.join).reset_index()

count_vectorizer = CountVectorizer(
    token_pattern='[^\\s][^\\s]+', max_df=1.0,
    min_df=5)
count_data = count_vectorizer.fit_transform(df_g['post'])
n_topics = 20
lda = LDA(n_components=n_topics, random_state=2)

print('%s\tTraining model' % datetime.now().time())
lda.fit(count_data)
words = count_vectorizer.get_feature_names()
out = open('lda3.txt', 'w', encoding='utf-8')
for topic_idx, topic in enumerate(lda.components_):
    out.write('\n\nTopic #%d:\n    ' % topic_idx)
    out.write('\n    '.join(words[i] for i in topic.argsort()[:-20:-1]))
out.close()
print('%s\tDone' % datetime.now().time())

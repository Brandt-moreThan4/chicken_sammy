from wordcloud import WordCloud
import matplotlib.pyplot as plt
from data_cleaning import word_freqs, tokens_adj
text = ' '.join(tokens_adj)
# Create a list of word



text = ' '.join(tokens_adj)

# Create the wordcloud object
wordcloud = WordCloud(background_color = 'white',
                    width = 512,
                    height = 384
                        ).generate(text)

# Display the generated image:
# fig, ax = plt.subtplots()

plt.imshow(wordcloud)
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()


print('lol')
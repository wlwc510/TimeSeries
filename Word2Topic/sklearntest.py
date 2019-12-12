from sklearn.datasets import fetch_20newsgroups
import pandas as pd
import lda
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold.t_sne import TSNE
import numpy as np
import bokeh.plotting as bp
from bokeh.plotting import save
from bokeh.models import HoverTool
import gensim.models.ldamodel


# we only want to keep the body of the documents!
remove = ('headers', 'footers', 'quotes')

datalines=open("D:/publications/preparing/00blockchain/data/policydatalines.txt", 'r')

c_list=datalines.readlines()

# fetch train and test data
# newsgroups_train = fetch_20newsgroups(subset ='train', remove =remove)
#
# newsgroups_test = fetch_20newsgroups(subset ='test', remove =remove)

# a list of 18,846 cleaned news in string format
# only keep letters & make them all lower case
# news = [' ' .join(filter(str.isalpha, raw .lower() .split())) for raw in newsgroups_train.data + newsgroups_test .data]

news = [' ' .join(filter(str.isalpha, raw .lower() .split())) for raw in c_list]



print("新闻条数",len(news))






#第二阶段 使用LDA进行主题提取
n_topics = 20 # number of topics
n_iter = 500 # number of iterations
# vectorizer: ignore English stopwords & words that occur less than 5 times
cvectorizer = CountVectorizer(min_df =5, stop_words ='chinese')
cvz = cvectorizer .fit_transform(news)
# train an LDA model
# sklearn.discriminant_analysis.LinearDiscriminantAnalysis()
lda_model = lda.LDA(n_topics =n_topics, n_iter =n_iter)
X_topics = lda_model .fit_transform(cvz)

#第三阶段 降维 和 可视化
# a t-SNE model
# angle value close to 1 means sacrificing accuracy for speed
# pca initializtion usually leads to better results
tsne_model = TSNE(n_components =2, verbose =1, random_state =0, angle =.99, init ='pca')
# 20-D -> 2-D
tsne_lda = tsne_model .fit_transform(X_topics)

n_top_words = 5 # number of keywords we show
# 20 colors
colormap = np .array([
"#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
"#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5",
"#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f",
"#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5"
])
_lda_keys = []
for i in range(X_topics .shape[0]):
    _lda_keys+= X_topics[i] .argmax(),
#并获得每个主题的顶级单词：
topic_summaries = []
topic_word = lda_model .topic_word_ # all topic words
vocab = cvectorizer .get_feature_names()
for i, topic_dist in enumerate(topic_word):
    topic_words = np .array(vocab)[np .argsort(topic_dist)][: -(n_top_words + 1): -1] # get!
    topic_summaries .append(' ' .join(topic_words)) # append!

title = '区块链 LDA viz'
num_example = len(X_topics)
plot_lda = bp .figure(plot_width =1400, plot_height =1100,
                      title =title,
                      tools ="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
                      x_axis_type =None, y_axis_type =None, min_border =1)
plot_lda .scatter(x =tsne_lda[:, 0], y =tsne_lda[:, 1],
                  color =colormap[_lda_keys][:num_example],
                  source =bp .ColumnDataSource({
                      "content": news[:num_example],
                      "topic_key": _lda_keys[:num_example]}))

# randomly choose a news (within a topic) coordinate as the crucial words coordinate
topic_coord = np .empty((X_topics .shape[1], 2)) * np .nan
for topic_num in _lda_keys:
    if not np .isnan(topic_coord) .any():
        break
    topic_coord[topic_num] = tsne_lda[_lda_keys .index(topic_num)]
# plot crucial words
for i in range(X_topics .shape[1]):
    plot_lda .text(topic_coord[i, 0], topic_coord[i, 1], [topic_summaries[i]])
    # hover tools
    hover = plot_lda .select(dict(type =HoverTool))
    hover .tooltips = {"content": "@content - topic: @topic_key"}
# save the plot
save(plot_lda, '{}.html' .format(title))



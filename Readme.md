# Chinese passive vocabulary associative analysis

This is a very simple code I developed to analyse my passive vocabulary recordings.

Majority of words in contemporary Chinese consist of two characters. Words, that have a character in common, have an association in meaning too. It is easier to memorize words not one-by-one, but in groups that share a character or have a common meaning.

Also, a set of entities with pairvise relationships sounds like a definition of a graph to me, so, I visualize all words as a graph using Networkx and Jaal.

Here, I used words from [official vocabulary lists for HSK exam](https://mandarinbean.com/new-hsk-vocabulary/). 
But there is even more fun in analyzing your own passive vocabulary. Say, if I read a book, write down every word that looks unfamiliar and then play around with them. For that, function of counting unique words is useful. Word, that occurs many times in such list, is both frequend and difficult to remember.

More sophisticated ways of usage for graph representation are left for further commits.
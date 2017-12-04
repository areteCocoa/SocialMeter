# Overview
Socialmeter is a flexible, extensible sentiment analysis framework.

It is built to provide a baseline framework for executing sentiment analysis,
while maintaining a level of customization that allows tuning
to achieve more accurate classification possible. 

All modules are built to be flexible to the needs of the user, and
are built with this in mind. The class hierarchy is designed to allow
users to drop-in their own modules that extend the baseline modules.

# Usage
(Currently under construction)

# Future Improvements
## Concrete Tasks
- [ ] Further constriction of the `SMeter` class definition
  - [ ] Removal of the `Module` class
  - [ ] Removal and replacement of the `Link` class for more specific use cases
- [ ] Unit testing of feature extractors and preprocessor extractors
- [ ] Better ensemble support
- [ ] Different `SMeter` objects that all feed into one larger `SMeter` objects
- [ ] Better Facebook Graph API implementation and support
- [ ] Option for preprocessors to 'replace' the text attribute for data
- [ ] Better abstraction for column format in conjunction with the `SMeter` object
		and input modules
- [ ] Built-in powerset grid search for feature extractors
- [ ] Remove `FeatureExtractorModule` class and only use the `FeatureExtractor` objects
		handled by a single class.

## Directional Improvements
- What do Data Scientists think of this?
- What do Programmers think of this?
- Do any other sites provide a service like the TwitterStreamAPI?

# References
Here are some sources used to build this project, as well as some references you may want
to use when building your own sentiment analysis project.

## Academic
Twitter Sentiment Classification using Distant Supervision - Alec Go, Richa Bhayani, Lei Huang (2009)
http://www-cs.stanford.edu/people/alecmgo/papers/TwitterDistantSupervision09.pdf

Twitter as a Corpus for Sentiment Analysis and Opinion Mining - Alexander Pak, Patrick Paroubek (2010)
https://pdfs.semanticscholar.org/ad8a/7f620a57478ff70045f97abc7aec9687ccbd.pdf

Semantic Sentiment Analysis of Twitter - Hassan Saif, Yulan He, Harith Alani (2012)
http://oro.open.ac.uk/34929/1/76490497.pdf

Sentiment-Analysis-Twitter - Ayush Pareek (2016)
https://github.com/ayushoriginal/Sentiment-Analysis-Twitter

## Non-Academic
GeeksforGeeks "Twitter Sentiment Analysis using Python"
http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/

Mining Twitter Data with Python (Part 6 – Sentiment Analysis Basics) - Marco Bonzanini
https://marcobonzanini.com/2015/05/17/mining-twitter-data-with-python-part-6-sentiment-analysis-basics/

## Published
Natural Language Processing with Python - Steven Bird, Ewan Klein, Edward Loper
http://victoria.lviv.ua/html/fl5/NaturalLanguageProcessingWithPython.pdf

## Datasets
W3C Wiki for Sentiment Analysis Datasets
https://www.w3.org/community/sentiment/wiki/Datasets#Emoticon_Sentiment_Lexicon

Twitter Sentiment Analysis Training Corpus (Dataset)
http://thinknook.com/twitter-sentiment-analysis-training-corpus-dataset-2012-09-22/

# License

SocialMeter is distributed under the terms of both

- MIT License <https://choosealicense.com/licenses/mit>
- Apache License, Version 2.0 <https://choosealicense.com/licenses/apache-2.0>

at your option.

# Overview
Socialmeter is a flexible, extensible sentiment analysis framework.

It is built to provide a baseline framework for executing sentiment analysis,
while maintaining a level of customization that allows tuning
to achieve more accurate classification possible. This is accomplished using
a middleware-inspired architecture built around modules.

All modules are built to be flexible to the needs of the user, and
are built with this in mind. The class hierarchy is designed to allow
users to drop-in their own modules that extend the baseline modules.

# Chain Architecture
The class structure revolves around the "chain architecture," which is a way
of structuring the sentiment analysis machine in a way that achieves the goal
of both flexible and extensible.

A user will, in most use cases, use a single **Chain** object and a handler for
that object. The Chain object is made up of **Link** objects.

A link object is a grouping of similarly typed **Modules**. It is an internal
class that is responsible for passing data around appropriately.

The core of SocialMeter comes from using, subclassing, and tuning Modules to
the user's needs. Modules all are responsible for taking text data as
an input and outputting some analysis of that input. There are four types
of modules: Input, Preclassification, Classification, Output.

## Input Modules
Input modules technically take no input, but are responsible for "generating"
the data that will be classified. These modules are responsible for formatting
the input data to a pandas Series object.

Here are the currently available input modules:
- TwitterStreamModule: Pulls data from the TwitterStream API and passes it to
the classifier as it is received

## Preclassification Modules
Preclassification modules take the text input and add different features to the
data. These are defined using **FeatureExtractor** subclasses. FeatureExtractors
are wrapped using a default **FeatureExtractorModule** class.

Preclassification modules are also responsible for discretizing there results. This
can be accomplished using the discrete_format feature.

Discrete format is a way to use string formats and corresponding discrete values
to discretize data without needing to write any evaluation code. Check the FeatureExtractor
class documentation for more information.

Many of these modules are made as a proof of concept and may not be useful.

Here are the currently available preclassification modules (all classes are
appended with FE for FeatureExtractor):
- AdjectiveCountFE: Counts the number of adjectives in the text.
- AdjectiveRatioFE: Counts the ratio of positive to negative words using sentiwordnet.
- ExcessiveCapitalsFE: Counts the ratio of words which are all capitals.
- ExcessivePunctuationFE: Counts the number of occurances of excessive (2 or more
consecutive) punctuation.
- NegativeInfluenceFE: Counts odd/even number of negative ("not") words.
- WordCountFE: Counts the number of words.

## Classification Modules
Classification modules take the text and features and classify them. These classes are
mostly wrappers for existing Python classifiers.

Here are the currently available classification modules:
- NBClassifierModule: Uses sklearn's GaussianNB class to classify texts.

## Output Modules
Output modules take the pandas Series object and "do something with it." While the handler
is responsible for returning data to the user, the output module can format it, save it
to a database, or anything that one might want to do with the data.

Here are the currently available output modules:
- OutputModule: Formats the Series object to a dict.

# Usage
(Currently under construction)

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
Twitter Sentiment Analysis Training Corpus (Dataset)
http://thinknook.com/twitter-sentiment-analysis-training-corpus-dataset-2012-09-22/

# License

SocialMeter is distributed under the terms of both

- MIT License <https://choosealicense.com/licenses/mit>
- Apache License, Version 2.0 <https://choosealicense.com/licenses/apache-2.0>

at your option.

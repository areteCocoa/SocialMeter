# demo.py

import socialmeter as sm

import socialmeter.inputs as inp
import socialmeter.preclass as pc
import socialmeter.classif as cl
import socialmeter.output as out

# Define some helper functions


# Loads sentiment-analysis-dataset.csv and returns it in
# list format. Loads n records.
def load_sentiment_dataset(n, preclass_link):
    training_filename = "sentiment-analysis-dataset.csv"
    f = open(training_filename, 'r')
    f.readline()  # Throwaway the column header
    features = list()
    classifications = list()

    for i in range(1, n):
        s = f.readline().split(',')
        sentiment = s[1]
        text = s[3].strip()

        # Run the text through the preclass chain to get
        # the features
        classif = list()
        for mod in preclass_link.mods:
            fe = mod.feature_extractor
            classif.append(fe.extract(text))
        features.append(classif)
        classifications.append(sentiment)

    return (features, classifications)


# The actual demo


# Instantiate the chain
c = sm.Chain()
c.set_column_format(["username", "text", "classification"])

# Load JSON configuration add use it to configure the TSModule
filename = "config.json"
ts = inp.twitterstream.TwitterStreamModule()
ts.load_config(filename)
ts.set_term("thomasjring")
c.add_mod(ts)

# Load the preclassification modules
adjc = sm.FeatureExtractorModule(pc.AdjectiveCounterFE)
adjc.key = "adjective-count"
c.add_mod(adjc)

# Load the classification module with data
# NOTE: We have to prepare the data to fit the classifier by
# cleaning it up and formatting it
nbc = cl.NBClassifierModule()
n_training_entries = 10
nbc.train(c.preclass_link, load_sentiment_dataset(10, c.preclass_link))
c.add_mod(nbc)

# Load the output module
c.add_mod(out.OutputModule())


# Create a dummy handler
def handler(data):
    text = data["text"]
    features = data["features"]
    classif = data["classification"]  # 1 = positive, 0 = negative
    print("Text: \"{}\"\n\tFeatures: \"{}\"\n\tClassification: \"{}\""
          .format(text, features, classif))


c.set_handler(handler)

print("Set the chain's column format to: {}".format(c.column_format))
input("Press enter to start fetching tweets.")

c.start_if_ready()



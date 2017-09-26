# demo.py

import socialmeter as sm

import socialmeter.inputs as inp
import socialmeter.preclass as pc
import socialmeter.classif as cl
import socialmeter.output as out


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
nbc = cl.NBClassifierModule()
training_filename = "sentiment-analysis-dataset.csv"
nbc.train(c.preclass_link, training_filename)
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

input("Press enter to start fetching tweets.")

c.start_if_ready()

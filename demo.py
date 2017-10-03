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

    for i in range(1, n+1):
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


# Create a dummy handler
def handler(data):
    text = data["text"]
    features = data["features"]
    classif = data["classification"]  # 1 = positive, 0 = negative
    print("Text: \"{}\"\n\tFeatures: \"{}\"\n\tClassification: \"{}\""
          .format(text, features, classif))


# The actual demo
# Instantiate the chain
c = sm.Chain()
c.set_column_format(["username", "text", "classification"])
# c1 is instantiated to test two chains against each other
c1 = sm.Chain()
c1.set_column_format(["username", "text", "classification"])

# Load JSON configuration add use it to configure the TSModule
filename = "config.json"
ts = inp.twitterstream.TwitterStreamModule()
ts.load_config(filename)
ts.set_term("thomasjring")
c.add_mod(ts)

# Load the preclassification modules
adjc_fe = pc.AdjectiveCounterFE()
discrete_format = ["0_0", "1_2", "2<"]
discrete_values = [0, 1, 2]
adjc_fe.set_discrete_format(discrete_format, discrete_values)
adjc = sm.FeatureExtractorModule(adjc_fe)
adjc.key = "adjective-count"
c.add_mod(adjc)
c1.add_mod(adjc)

adjr_fe = pc.AdjectiveRatioFE()
discrete_format1 = ["0.0_0.5", "0.5<"]
adjr_fe.set_discrete_format(discrete_format1, [0, 1])
adjr = sm.FeatureExtractorModule(adjr_fe)
adjr.key = "adjective-ratio"
c.add_mod(adjr)
c1.add_mod(adjr)

negi_fe = pc.NegativeInfluenceFE()
negi = sm.FeatureExtractorModule(negi_fe)
negi.key = "negative-influence"
c.add_mod(negi)

excaps_fe = pc.ExcessiveCapitalsFE()
excaps = sm.FeatureExtractorModule(excaps_fe)
excaps.key = "excessive-caps"
c.add_mod(excaps)

expunc_fe = pc.ExcessivePunctuationFE()
expunc = sm.FeatureExtractorModule(expunc_fe)
expunc.key = "excessive-punctuation"
c.add_mod(expunc)

wc_fe = pc.WordCountFE()
wc = sm.FeatureExtractorModule(wc_fe)
wc.key = "word-count"
c.add_mod(wc)
c1.add_mod(wc)

# Load the classification module with data
nbc = cl.NBClassifierModule()
c.add_mod(nbc)
c1.add_mod(nbc)

# We branch at this point to either demo fetching tweets
# or show the test suite
n_e = int(input("How many entries should be loaded from the\
 test dataset?\n"))
training_datas = load_sentiment_dataset(n_e, c.preclass_link)

opt = input("Enter \"tweets\" to get tweets, and \"test\" to test \
the chain.\n")

if opt == "tweets":
    nbc.train(c.preclass_link, training_datas)

    c.add_mod(nbc)
    # Load the output module
    c.add_mod(out.OutputModule())
    c.set_handler(handler)
    c.start_if_ready()
elif opt == "test":
    k_n = input("How many k-folds would you like to perform?\n")
    t = sm.KFoldValidationTest()
    t.set_n_folds(int(k_n))
    print("Now testing chain {} and chain {} against each other.".format(
        c, c1))
    r = t.test_chains([c, c1], training_datas)
    print(r)
else:
    print("Unrecognized input \"{}\"".format(opt))

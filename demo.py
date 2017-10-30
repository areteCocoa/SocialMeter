# demo.py

import socialmeter as sm

import socialmeter.inputs as inp
import socialmeter.preprocess as pp
import socialmeter.preclass as pc
import socialmeter.classif as cl
import socialmeter.output as out

# Define some helper functions


# Loads sentiment-analysis-dataset.csv and returns it in
# list format. Loads n records.
def load_sentiment_dataset(n, preclass_link):
    (texts, classifications) = load_dataset(n)

    features = list()
    for i in range(1, n+1):
        # Run the text through the preclass chain to get
        # the features
        feature = list()
        text = texts[i]
        for mod in preclass_link.mods:
            fe = mod.feature_extractor
            feature.append(fe.extract(text))
        features.append(feature)

    return (features, classifications)


def load_dataset(n):
    training_filename = "datasets/sentiment-analysis-dataset.csv"
    f = open(training_filename, 'r')
    f.readline()  # Throwaway the column header
    texts = list()
    classifications = list()

    for i in range(1, n+1):
        s = f.readline().split(',')
        classifications.append(s[1])
        texts.append(s[3].strip())

    return (texts, classifications)


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
filename = "configs/config.json"
ts = inp.twitterstream.TwitterStreamModule()
ts.load_config(filename)
ts.set_term("thomasjring")
c.add_mod(ts)

# Load the preprocess modules
ngram = sm.PreprocessorExtractorModule(pp.NGramPreprocessor())
c.add_mod(ngram)

# Load the preclassification modules
adjc_fe = pc.AdjectiveCounterFE()
adjc = sm.FeatureExtractorModule(adjc_fe)
c.add_mod(adjc)
c1.add_mod(adjc.deep_copy())

adjr_fe = pc.AdjectiveRatioFE()
adjr = sm.FeatureExtractorModule(adjr_fe)
c.add_mod(adjr)
c1.add_mod(adjr)

negi_fe = pc.NegativeInfluenceFE()
negi = sm.FeatureExtractorModule(negi_fe)
c.add_mod(negi)

excaps_fe = pc.ExcessiveCapitalsFE()
excaps = sm.FeatureExtractorModule(excaps_fe)
c.add_mod(excaps)

expunc_fe = pc.ExcessivePunctuationFE()
expunc = sm.FeatureExtractorModule(expunc_fe)
c.add_mod(expunc)

wc_fe = pc.WordCountFE()
wc = sm.FeatureExtractorModule(wc_fe)
c.add_mod(wc)
c1.add_mod(wc)

# Load the classification module with data
nbc = cl.NBClassifierModule()
c.add_mod(nbc)
c1.add_mod(nbc.deep_copy())

# We branch at this point to either demo fetching tweets
# or show the test suite
n_e = int(input("How many entries should be loaded from the\
 test dataset?\n"))


opt = input("Enter \"tweets\" to get tweets, and \"test\" to test \
the chain.\n")

if opt == "tweets":
    training_datas = load_sentiment_dataset(n_e, c.preclass_link)
    nbc.train(c.preclass_link, training_datas)

    # Load the output module
    c.add_mod(out.OutputModule())
    c.set_handler(handler)
    c.start_if_ready()
elif opt == "test":
    k_n = input("How many k-folds would you like to perform?\n")
    t = sm.KFoldValidationTest()
    t.set_n_folds(int(k_n))

    dataset = load_dataset(n_e)

    r = t.test_chains([c, c1], dataset)
    print(r)
else:
    print("Unrecognized input \"{}\"".format(opt))

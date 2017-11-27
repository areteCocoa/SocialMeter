# demo.py

import itertools as it


import socialmeter as sm

import socialmeter.inputs as inp
import socialmeter.preprocess as pp
import socialmeter.preclass as pc
import socialmeter.classif as cl
import socialmeter.output as out


# Define some helper functions
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
    classif = data["classification"]  # 1 = positive, 0 = negative
    print("Text: \"{}\"\n\tClassification: \"{}\""
          .format(text, classif))


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return it.chain.from_iterable(it.combinations(s, r) for r
                                  in range(1, len(s)+1))


# The actual demo code
def create_smeter():
    meter = sm.SMeter()
    meter.set_column_format(["username", "text", "classification"])

    # Load JSON configuration add use it to configure the TSModule
    twitter_config_filename = "configs/config.json"
    ts = inp.twitterstream.TwitterStreamModule()
    ts.load_config(twitter_config_filename)
    ts.set_term("Donald Trump")
    meter.set_input_mod(ts)

    # Load the preprocess modules
    sw = pp.StopWordsPreprocessor()
    from nltk.corpus import stopwords
    stop = list(stopwords.words('english'))
    sw.add_stop_words(stop)
    meter.add_preprocess_mod(sm.PreprocessorExtractorModule(sw))

    # Load the preclassification modules
    adjc_fe = pc.AdjectiveCounterFE()
    adjc = sm.FeatureExtractorModule(adjc_fe)
    meter.add_preclass_mod(adjc)

    adjr_fe = pc.AdjectiveRatioFE()
    adjr = sm.FeatureExtractorModule(adjr_fe)
    meter.add_preclass_mod(adjr)

    exc_caps = pc.ExcessiveCapitalsFE()
    exc = sm.FeatureExtractorModule(exc_caps)
    meter.add_preclass_mod(exc)

    # Load the classification module with data
    nbc = cl.AdaBoostModule()
    meter.set_class_mod(nbc)

    # Load the output module with data
    out_mod = out.OutputModule()
    meter.set_output_mod(out_mod)

    return meter


def create_smeters():
    m1 = sm.SMeter()
    
    sw = pp.StopWordsPreprocessor()
    import nltk
    stop = list(nltk.corpus.stopwords.words('english'))
    sw.add_stop_words(stop)
    sw_mod = sm.PreprocessorExtractorModule(sw)

    ht = pp.HashtagPreprocessor()
    ht_mod = sm.PreprocessorExtractorModule(ht)

    mn = pp.MentionPreprocessor()
    mn_mod = sm.PreprocessorExtractorModule(mn)

    emo = pc.EmoticonSentimentFE()
    emo.set_file(open("datasets/EmoticonSentimentLexicon.txt", 'r'))
    emo_mod = sm.FeatureExtractorModule(emo)

    ar = pc.AdjectiveRatioFE()
    ar_mod = sm.FeatureExtractorModule(ar)

    hc = pc.HashtagCountFE()
    hc_mod = sm.FeatureExtractorModule(hc)

    classifiers = [cl.AdaBoostModule,
                   cl.DecisionTreeModule,
                   cl.GaussianProcessModule,
                   cl.KNeighborsModule,
                   cl.LinearSVCModule,
                   cl.MultinomialNBModule,
                   cl.NBClassifierModule,
                   cl.MLPModule,
                   cl.NuSVCModule,
                   cl.RadiusNeighborsModule,
                   cl.SVCModule
                   ]

    meters = list()
    for c in classifiers:
        m = sm.SMeter()
        m.add_preprocess_mod(sw_mod)
        m.add_preprocess_mod(ht_mod)
        m.add_preprocess_mod(mn_mod)
        m.add_preclass_mod(emo_mod)
        m.add_preclass_mod(ar_mod)
        m.add_preclass_mod(hc_mod)
        m.set_class_mod(c())

        # We can name the classifier so that when it is printed
        # it doesn't clog everything up.
        c_inst = m.class_mod
        name = str(type(c_inst)).strip("<>'")
        name = name.split('.')
        name = name[len(name) - 1]
        name += " classifier"
        m.name = name

        meters.append(m)

    return meters


def training_data():
    n = 500
    training_datas = load_dataset(n)
    return training_datas

# elif opt == "cmp":
#     preproc  = {pp.HashtagPreprocessor, pp.MentionPreprocessor,
#                 pp.NGramPreprocessor, pp.POSTagPreprocessor,
#                 pp.StopWordsPreprocessor, pp.TokenizerPreprocessor}
#     features = {pc.AdjectiveCounterFE, pc.AdjectiveRatioFE,
#                 pc.EmoticonSentimentFE, pc.ExcessiveCapitalsFE,
#                 pc.ExcessivePunctuationFE, pc.HashtagCountFE,
#                 pc.NegativeInfluenceFE, pc.WordCountFE}
#     classifs = {cl.NBClassifierModule}
#     # iteratively create all the combinations of chains
#     chains = list()
#     # Start with the features only
#     print("Creating generator for feature powerset.")
#     f_combinations = powerset(list(features))
#     print("Feature powerset generator created.")

#     print("Creating generator for preprocessor powerset.")
#     p_combinations = powerset(list(preproc))
#     print("Preprocessor powerset created.")
    
#     print("Creating generator for classifier powerset.")
#     combinations = powerset(list(classifs))
#     print("Classifier powerset created.")

#     print("Creating chains with all sets from the powerset of features.")
#     for f in f_combinations:
#         c = sm.Chain()
#         c.column_format = list()
#         for fe in f:
#             if fe == pc.EmoticonSentimentFE:
#                 inst = fe()

#                 c.add_mod(sm.FeatureExtractorModule(inst))
#             else:
#                 c.add_mod(sm.FeatureExtractorModule(fe()))
#         c.add_mod(cl.NBClassifierModule())
#         chains.append(c)
#     print("Finished creating {} chains from all the sets.".format(len(chains)))
    
#     k_n = input("How many k-folds would you like to perform?\n")
#     t = sm.KFoldValidationTest()
#     t.set_n_folds(int(k_n))

#     dataset = load_dataset(n_e)

#     results = t.test_chains(chains, dataset)

#     for (c, (acc, std)) in results:
#         print("[", end='')
#         for m in c.preclass_link.mods:
#             print("{}".format(m), end='')
#         print("] - {} +- {}\n".format(acc, std))
# else:
#     print("Unrecognized input \"{}\"".format(opt))

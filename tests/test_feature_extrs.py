# tests/fe_tests.py

from socialmeter import preclass as pc


def test_adj_count():
    adjc = pc.AdjectiveCounterFE()
    adjc.discrete_format = None
    errors = list()

    t1 = "This is a funny test sentence."
    t2 = "I am not happy at all to see this stupid movie \
because of my silly little brother."
    t3 = "This has no adjectives."

    if adjc.extract(t1) != 1:
        errors.append("Missed a single adjective in a sentence.")
    if adjc.extract(t2) != 4:
        errors.append("Missed four adjectives in a sentence. Instead found {}.".format(adjc.extract(t2)))
    if adjc.extract(t3) != 0:
        errors.append("Missed no adjectives in a sentence.")

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

    
def test_adj_ratio():
    adjr = pc.AdjectiveRatioFE()
    adjr.discrete_format = None
    errors = list()

    t1 = "This is a funny test sentence"
    t2 = "I am not happy at all to see this stupid movie \
because of my dumb brother."
    t3 = "This has no adjectives."

    if adjr.extract(t1) != 1.0:
        errors.append("Missed 100% positive sentiment, found {}% instead.".format(adjr.extract(t1) * 100))
    if (adjr.extract(t2) > .32 and adjr.extract(t2) < .34) is False:
        errors.append("Missed 33% positive sentiment, found {}% \
 instead.".format(adjr.extract(t2) * 100))
    if adjr.extract(t3) != 0.0:
        errors.append("Missed 0% sentiment, found {}% \
instead.".format(adjr.extract(t3)))

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

    
def test_emoticon():
    e = pc.EmoticonSentimentFE()
    e.set_file(open("datasets/EmoticonSentimentLexicon.txt", 'r'))
    errors = list()

    t1 = "xD" # positive (1)
    t2 = "X_0" # negative (-1)
    t3 = "FF" # neutral (0)

    if e.extract(t1) != 1:
        errors.append("Error detecting {} as positive (1). Instead \
found {}.".format(t1, e.extract(t1)))
    if e.extract(t2) != -1:
        errors.append("Error detecting {} as negative (-1). Instead \
found {}.".format(t2, e.extract(t2)))
    if e.extract(t3) != 0:
        errors.append("Error detecting {} as not found (0). Instead \
found {}.".format(t3, e.extract(t3)))

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_excess_caps():
    ec = pc.ExcessiveCapitalsFE()
    errors = list()

    t1 = "This is a normal sentence."
    t2 = "THIS IS A LOUD SENTENCE. Do not know why though."
    t3 = "THIS IS ONLY LOUD."

    t1r = ec.extract(t1)
    t2r = ec.extract(t2)
    t3r = ec.extract(t3)

    if t1r != 0:
        errors.append("Error detecting 0% capitals. Instead returned \
{}.".format(t1r))
    if t2r != 0.5:
        errors.append("Error detecting 50% capitals. Instead returned \
{}.".format(t2r))
    if t3r != 1.0:
        errors.append("Error detecting 100% capitals. Instead returned \
{}.".format(t3r))

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_excess_punc():
    ep = pc.ExcessivePunctuationFE()
    errors = list()

    t1 = "This is a normal sentence."
    t2 = "This is a loud sentence!!! Oh my god?!?!"
    t3 = "This!!! Has.... So many!!! Oh my god!!!"

    t1r = ep.extract(t1) # 0
    t2r = ep.extract(t2) # 2
    t3r = ep.extract(t3) # 4

    if t1r != 0:
        errors.append("Error detecting 0 excess capitals. Instead \
returned {}.".format(t1r))
    if t2r != 2:
        errors.append("Error detecting 2 excess capitals. Instead \
returned {}.".format(t2r))
    if t3r != 4:
        errors.append("Error detecting 4 excess capitals. Instead \
returned {}.".format(t3r))

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_hashtag_count():
    hc = pc.HashtagCountFE()
    errors = list()

    t1 = "This is a #single hashtag check"  # 1
    t2 = "This #is #a #lot #of #hashtags" # 5
    t3 = "This checks whether # 10 counts (it shouldn't)" # 0
    t4 = "This checks if an unterminated pound sign works #" # 0

    t1r = hc.extract(t1)  # 1
    t2r = hc.extract(t2)  # 5
    t3r = hc.extract(t3)  # 0
    t4r = hc.extract(t4)  # 0

    if t1r != 1:
        errors.append("Error detecting 1 hashtag. Instead \
returned {}.".format(t1r))
    if t2r != 5:
        errors.append("Error detecting 5 hashtags. Instead \
returned {}.".format(t2r))
    if t3r != 0:
        errors.append("Error detecting 0 hashtags. Instead \
returned {}.".format(t3r))
    if t4r != 0:
        errors.append("Error detecting 0 hashtags. Instead \
returned {}.".format(t3r))

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_neg_inf():
    ni = pc.NegativeInfluenceFE()
    errors = list()

    t1 = "This is not a good sentence."
    t2 = "This a good sentence."
    t3 = "This is not a not good sentence."
    t4 = "This is not not not a great sentence."

    t1r = ni.extract(t1)  # 1
    t2r = ni.extract(t2)  # 0
    t3r = ni.extract(t3)  # 0
    t4r = ni.extract(t4)  # 1

    if t1r != 1:
        errors.append("Error detecting odd negatives. Instead \
returned {}.".format(t1r))
    if t2r != 0:
        errors.append("Error detecting even negatives. Instead \
returned {}.".format(t2r))
    if t3r != 0:
        errors.append("Error detecting even. Instead \
returned {}.".format(t3r))
    if t4r != 1:
        errors.append("Error detecting even. Instead \
returned {}.".format(t4r))

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_word_count():
    wc = pc.WordCountFE()
    errors = list()

    t1 = "This has 5 words here."  # 5
    t2 = "This has 4 words."  # 4
    t3 = "This doesn't have 5 words."  # 6

    t1r = wc.extract(t1)
    t2r = wc.extract(t2)
    t3r = wc.extract(t3)

    if t1r != 5:
        errors.append("Error counting 5 words. Returned {}.".format(t1r))
    if t2r != 4:
        errors.append("Error counting 4 words. Returned {}.".format(t2r))
    if t3r != 6:
        errors.append("Error counting 6 words. Returned {}.".format(t3r))

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

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

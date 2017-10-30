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

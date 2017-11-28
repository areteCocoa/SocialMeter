# __main__.py
#
# This file is used to test SMeter configurations, as well
# as to demo various chains.

import argparse
import importlib

from socialmeter.testsuite import kfold, grid_search

parser = argparse.ArgumentParser(
    prog="SocialMeter",
    description='Tools for configuring, testing and demoing various SMeter \
    configurations.'
)

parser.add_argument('filename', metavar='filename', type=str,
                    help='The name of the file to be parsed for testing \
                    or demonstration.')
parser.add_argument('action', metavar='action', type=str,
                    help='The action to be performed on the chain(s). \
                    Availble actions include: \"test\", \"demo\".')
parser.add_argument('--multiple', action='store_const', const='multiple',
                    help='Test multiple meter objects from the file. Note \
                    the file must implement \`create_smeters\'')

args = parser.parse_args()
action = args.action
multiple = args.multiple
filename = args.filename

modulename = filename.split('.')[0]

i = None
try:
    i = importlib.import_module(modulename)
except ModuleNotFoundError:
    parser.error("Could not find python file named {}".format(filename))

# Successfully imported the module (the program will exit before
# this point in the code


# Now look for function create_smeter() and use it to get the
# user's SMeter
def meter_from_file():
    meter = None
    if hasattr(i, "create_smeter"):
        meter = i.create_smeter()
    else:
        parser.error("Could not find function \"create_smeter\" in the input "
                     + "file \"{}\". Please define the function in your file."
                     .format(filename))
    return meter


def meters_from_file():
    meters = None
    if hasattr(i, "create_smeters"):
        meters = i.create_smeters()
    else:
        parser.error(("Could not find function \"create_smeters\" in the input"
                     + " file \"{}\". Please define the function in your"
                     + " file.").format(filename))
    return meters


def training_data_from_file():
    t_datas = None
    if hasattr(i, "training_data"):
        t_datas = i.training_data()
    else:
        parser.error("Could not find function \"training_data\" in the input "
                     + "file \"{}\". Please define the function in your file."
                     .format(filename))
    return t_datas


def grid_search_params():
    params = None
    if hasattr(i, "grid_search_params"):
        params = i.grid_search_params()
    else:
        parser.error("Could not find function \"grid_search_params\" in the \
input file \"{}\". Please define the function in your file".format(filename))
    return params


def test_single_meter():
    meter = meter_from_file()
    t_datas = training_data_from_file()
    print("Starting test with SMeter {}".format(meter))
    kfold_test = kfold.KFoldValidationTest()
    results = kfold_test.test_meter(meter, t_datas)
    print("SMeter has {}% accuracy with a std-dev of {}."
          .format(results[0], results[1]))


def test_multiple_meters():
    meters = meters_from_file()
    t_datas = training_data_from_file()
    print("Starting test with {} SMeters and {} data points."
          .format(len(meters), len(t_datas)))
    k = kfold.KFoldValidationTest()
    results = k.test_meters(meters, t_datas)
    print("Meter testing successful, here are the results (in order):")
    for i in range(len(results)):
        tup = results[i]
        meter = tup[0]
        result = tup[1]
        name = str(meter)
        if meter.name is not None:
            name = meter.name

        print("(#{}) Meter \"{}\": Mean {}, STD-DEV {}.".format(
            i + 1, name, result[0], result[1]))

        diff = len(meters) - len(result)
        if diff != 0:
            print("It seems that {} meters encountered errors in \
            being tested.".format(diff))


def grid_search_meter():
    meter = meter_from_file()
    t_datas = training_data_from_file()
    parameters = grid_search_params()
    print("Starting grid search with SMeter from file.")
    print("Meter object: {}".format(meter))
    grid = grid_search.GridSearch(parameters)

    results = grid.search_meter(meter, t_datas)

    print("Here are the results in descending order, \
sorted by mean_test_score:")
    for i in range(len(results)):
        result = results[i]
        print("(#{}) Params: {},\nmean_test_score: {}, std_dev: {}"
              .format(i, result['params'], result['mean_test_score'],
                      result['std_test_score']))


def run_demo():
    meter = meter_from_file()
    t_datas = training_data_from_file()
    print("Starting demo with SMeter {}".format(meter))
    meter.train(t_datas)

    def handler(data):
        # Check if it is None -- if it is None, it's likely that
        # the output module has taken care of the data
        if data is not None:
            print("({}): {}".format(data["classification"], data["text"]))

    meter.set_handler(handler)
    meter.start_if_ready()


# We have the meter object, now we can see what they want to do
# with it.
if action == "test":
    if multiple is None:
        test_single_meter()
    else:
        test_multiple_meters()
elif action == "grid-search":
    grid_search_meter()
elif action == "demo":
    run_demo()
else:
    parser.error("Unrecognized action \"{}\".".format(action))

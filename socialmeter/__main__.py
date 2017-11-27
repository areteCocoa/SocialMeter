# __main__.py
#
# This file is used to test SMeter configurations, as well
# as to demo various chains.

import argparse
import importlib

from socialmeter.testsuite import kfold

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
    print("Starting test with {} SMeters.".format(len(meters)))
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


def run_demo():
    meter = meter_from_file()
    t_datas = training_data_from_file()
    print("Starting demo with SMeter {}".format(meter))
    meter.train(t_datas)

    def handler(data):
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
elif action == "demo":
    run_demo()
else:
    parser.error("Unrecognized action \"{}\".".format(action))
    

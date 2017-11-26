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


args = parser.parse_args()
action = args.action
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

meter = None
if hasattr(i, "create_smeter"):
    meter = i.create_smeter()
else:
    parser.error("Could not find function \"create_smeter\" in the input " +
                 "file \"{}\". Please define the function in your file."
                 .format(filename))


t_datas = None
if hasattr(i, "training_data"):
    t_datas = i.training_data()
else:
    parser.error("Could not find function \"training_data\" in the input " +
                 "file \"{}\". Please define the function in your file."
                 .format(filename))

# We have the meter object, now we can see what they want to do
# with it.
if action == "test":
    print("Starting test with SMeter {}".format(meter))
    kfold_test = kfold.KFoldValidationTest()
    print("Created KFold validation test.")
    results = kfold_test.test_meter(meter, t_datas)
    print("SMeter has {}% accuracy with a std-dev of {}."
          .format(results[0], results[1]))
elif action == "demo":
    print("Starting demo with SMeter {}".format(meter))
    meter.train(t_datas)

    def handler(data):
        print("({}): {}".format(data["classification"], data["text"]))

    meter.set_handler(handler)

    meter.start_if_ready()
else:
    parser.error("Unrecognized action \"{}\".".format(action))
    

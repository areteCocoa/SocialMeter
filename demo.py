# demo.py

import socialmeter as sm

# Instantiate the chain
c = sm.Chain()
c.set_column_format(["username", "text", "classification", "features"])

# Load JSON configuration add use it to configure the TSModule
filename = "config.json"
ts = sm.TwitterStreamModule()
ts.load_config(filename)
ts.set_term("thomasjring")
c.add_mod(ts)

# Load the preclassification modules
adjc = sm.AdjectiveCountModule()
c.add_mod(adjc)

# Load the classification module with data
nbc = sm.NBClassifierModule()
training_filename = "sentiment-analysis-dataset.csv"
nbc.train(c.preclass_link, training_filename)
c.add_mod(nbc)

# Load the output module
c.add_mod(sm.OutputModule())


# Create a dummy handler
def handler(data):
    print(data)


c.set_handler(handler)

input()

c.start_if_ready()


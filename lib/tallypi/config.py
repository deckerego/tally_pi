import argparse
import json
import os

class Configuration(object):
    config_values = { }

    def __init__(self):
        config_file = open(args.config, 'r')
        self.config_values = json.loads(config_file.read())

    def get(self, name):
        return self.config_values.get(name)

configuration = Configuration()

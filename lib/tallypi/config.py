import argparse
import json

class Configuration(object):
    config_values = { }
    www_directory = '/srv/www'

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', type=str, default='/etc/tallypi.conf', help='path to configuration file')
        parser.add_argument('--wwwdir', type=str, default='/srv/www', help='path to HTML files')
        args = parser.parse_args()

        config_file = open(args.config, 'r')
        self.config_values = json.loads(config_file.read())
        self.config_values['static_file_root'] = args.wwwdir

    def get(self, name):
        return self.config_values.get(name)

configuration = Configuration()

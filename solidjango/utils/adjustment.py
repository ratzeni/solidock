import os.path
import sys
import yaml

from utils.logging import Logging


class ConfigurationFromYamlFile(object):
    """
    Retrieve infrastructure configuration's details from a yaml file
    """
    def __init__(self, yaml_file, loglevel='INFO'):
        self.logger = Logging(self.__class__.__name__, level=loglevel).get_logger()
        if os.path.isfile(yaml_file):
            self.conf = self.__load_config(yaml_file)
        else:
            self.logger.critical('{} not exists'.format(yaml_file))
            sys.exit()

    def __load_config(self, config_file):
        with open(config_file) as cfg:
            conf = yaml.load(cfg, Loader=yaml.FullLoader)
        return conf

    def get(self):
        return self.conf

    def get_remote_section(self, label='remote', subsection=None):
        return self.get_section(label)

    def get_vars_section(self, label='default_vars', subsection=None):
        return self.get_section(label)

    def get_pipelines_section(self, label='pipelines', subsection=None):
        return self.get_section(label)

    def get_section(self, section_label):
        if self.is_section_present(section_label):
            return self.conf[section_label]
        else:
            self.logger.warning('section {} not found'.format(section_label))
            return ''

    def is_section_present(self, section_label):
        if section_label in self.conf:
            return True
        else:
            return False


class YamlFileEditor(object):
    def __init__(self, yaml_file):
        self.yaml_file = yaml_file
        self.handle = ConfigurationFromYamlFile(yaml_file=yaml_file)
        self.yaml_obj = self.handle.get()

    def __edit(self):
        with open(self.yaml_file, 'w') as f:
            yaml.dump(self.yaml_obj, f)

    def edit_vars(self, vars):
        for k, v in vars.items():
            if k in self.yaml_obj:
                self.yaml_obj[k] = v
        self.__edit()

    def get(self):
        return self.yaml_obj

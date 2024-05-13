import configparser
config = configparser.ConfigParser()
config['SETTINGS'] = {'PORT': 8080,
                     'ROOT_DIR': 'files',
                     'MAX_SIZE': 8192}
with open('settings.ini', 'w') as configfile:
  config.write(configfile)
import configparser

def make_ini(root):
    conf = configparser.ConfigParser()
    conf.add_section('GLOBALS')
    conf.set('GLOBALS', 'root', root)
    with open('settings.ini', 'w') as config_file:
        conf.write(config_file)

def get_root():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    root = config.get('GLOBALS', 'root')
    return root
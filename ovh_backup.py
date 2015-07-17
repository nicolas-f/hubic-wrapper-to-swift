import hubic
import ConfigParser
import os
import ConfigParser

# Parse backup config

backup_conf = {'POSTGRESQL' : [['POSTGRE_USER', None], ['POSTGRE_PASSWORD', None]]}


def get_entry(conf, section, name, option):                                                                                       
    try:                                                                                                                                 
	value = conf.get(section, name)                                                                                     
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
	if option:
	    value = option
	else:
	    value = raw_input(name)
    return value

def save_config(conf, config_file):
   self.hubic_config.set('openstack', 'os_token_expire', self.os_token_expire)
   with open(config_file, 'wb') as configfile:
       self.hubic_config.write(configfile)
       os.chmod(config_file, 0600)


config_file = os.path.expanduser('~/.ovhbackup.cfg')
def load_config(backup_conf, config_file):
    # Read stored configuration
    try:
        backup_config = ConfigParser.ConfigParser()
        backup_config.read(config_file)
    except ConfigParser.ParsingError:
        print "Cannot read config file %s" % self.config_file
        sys.exit(1)
    for section, entries in backup_conf
        for entry, defaultValue in entries:
            backup_config.set(section, entry, get_entry(backup_config, section, entry, defaultValue))

load_config(backup_conf, config_file)

save_config(backup_conf, config_file)
# Ask for missing configuration values


def what_to_remove(dirs):
    keep_days = 5
    keep_weeks = 3
    keep_month = 3
    keep_years = 5
    backups = []
    rotate = [['%Y_%m_%d', keep_days], ['%Y_%W', keep_weeks], ['%Y_%m', keep_month], ['%Y', keep_years]]
    fmt = 'backup_%Y_%m_%d'
    for foldername in dirs:
        try:
            conv = time.strptime(foldername,fmt)
            backups.append([conv, foldername])
        except ValueError:
            pass
    # ascending time order
    backups.sort(key = lambda x: x[0])
    for timefmt, keep in rotate:
        cursor = len(backups) - 1
        lastEntry = ''
        while keep > 0 and cursor >= 0:
            conv, foldername = backups[cursor]
            # Remove item if different of lastEntry
            convFmt = time.strftime(timefmt, conv)
            if convFmt != lastEntry:
                lastEntry = convFmt
                keep = keep - 1
                backups.pop(cursor)
            cursor = cursor - 1
    return backups




# Swift configs
class command:
    hubic_access_token = None
    hubic_refresh_token =  None
    verbose = False
    get = None
    os_storage_url = None
    hubic_password = None
    hubic_client_secret = None
    os_refresh = False
    token = False
    refresh = False
    os_auth_token = None
    hubic_username = None
    swift = True
    hubic_client_id = None
    hubic_redirect_uri = None
    post = None
    config = None
    data = None
    delete = None

hubic.options = command()

cloud = hubic.hubic()
cloud.auth()
cloud.token()

args = ['upload', 'default', 'testtransfer.txt']
cloud.swift(args)

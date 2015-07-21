from __future__ import print_function
import hubic
import ConfigParser
import os
import ConfigParser
import shutil
import sys
import subprocess
import time

# Parse backup config

backup_conf = {'POSTGRESQL' : [['POSTGRE_USER', None], ['POSTGRE_PASSWORD', None]], 'GENERAL' : [['TEMPORARY_FOLDER', None]]}


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
   with open(config_file, 'wb') as configfile:
       conf.write(configfile)
       os.chmod(config_file, 0600)


config_file = os.path.expanduser('~/.ovhbackup.cfg')
def load_config(backup_conf, config_file):
    # Read stored configuration
    try:
        backup_config = ConfigParser.ConfigParser()
        backup_config.read(config_file)
    except ConfigParser.ParsingError:
        print("Cannot read config file %s" % self.config_file)
        sys.exit(1)
    for section, entries in backup_conf.iteritems():
        for entry, defaultValue in entries:
            # Create section if not exists
            if not backup_config.has_section(section):
                backup_config.add_section(section)
            backup_config.set(section, entry, get_entry(backup_config, section, entry, defaultValue))
    return backup_config 

# Ask for missing configuration values
configuration = load_config(backup_conf, config_file)

# Save configuration
save_config(configuration, config_file)

# Prepare backup folder
tmpfold = configuration.get('GENERAL','TEMPORARY_FOLDER')

if len(tmpfold) == 0:
    raise ValueError('Backup folder path is empty')

#Make target folder
if os.path.exists(tmpfold):
    # Clear folder
    shutil.rmtree(tmpfold)
os.mkdir(tmpfold, 0750)

###################BACKUP OPERATIONS###################################
# Store /etc/ git folder

subprocess.call(["tar","-zcvf", tmpfold+"etc.tar.gz", "/home/backup/configs/etc2/","--exclude","/home/backup/configs/etc2/.git/config"])
 
# Backup PostgreSQL

#os.environ["PGPASSWORD"] = configuration.get('POSTGRESQL','POSTGRE_PASSWORD')
#f = open(tmpfold+"pgdump.gz", "wb")
#ps = subprocess.Popen(("pg_dumpall","-U","pgbackup"), stdout=subprocess.PIPE)
#output = subprocess.call(('gzip'), stdin=ps.stdout, stdout=f)
#ps.wait()

##
# Rotate folder by removing outdated ones (within each time intervals)
# fmt Folder time format
# dirs Folder list
def what_to_remove(fmt, dirs):
    keep_days = 3
    keep_weeks = 1
    keep_month = 2
    keep_years = 3
    backups = []
    rotate = [['%Y_%m_%d', keep_days], ['%Y_%W', keep_weeks], ['%Y_%m', keep_month], ['%Y', keep_years]]
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
        last_entry = ''
        last_keep = None
        while cursor >= 0 and (keep > 0 or (last_keep is not None and time.strftime(timefmt, backups[cursor][0])
            == time.strftime(timefmt, last_keep[0]))):
            conv, foldername = backups[cursor]
            # Remove item if different of lastEntry
            convFmt = time.strftime(timefmt, conv)
            if keep > 0 and convFmt != last_entry:
                #print(convFmt,keep,"keep",foldername)
                last_entry = convFmt
                keep = keep - 1
                backups.pop(cursor)
                last_keep = [conv, foldername]
            elif last_keep is not None and convFmt == last_entry:
                # Similar time on the current time range, should keep the older one for the same range
                #print(convFmt,keep,"Remove ",last_keep[1],"keep",foldername)
                backups.pop(cursor)
                backups.insert(cursor,last_keep)
                last_keep = [conv, foldername]
            cursor = cursor - 1
    return [foldername for timedate, foldername in backups]



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
fmt = 'backup_%Y_%m_%d'
todayfolder = time.strftime(fmt)
args = ['upload', 'default', tmpfold, '--object-name', 'backupovh/'+todayfolder+"/"]
# Transfer new folder
print(cloud.swift(args))

#Compute removal of old folders
args = ['list', 'default', '--prefix', 'backupovh/']
hubic_backup_folders = dict()
for file in cloud.swift(args).strip().split("\n"):
    foldertime = file.split(os.sep)[1]
    if not hubic_backup_folders.has_key(foldertime):
        hubic_backup_folders[foldertime] = []
    hubic_backup_folders[foldertime].append(file)

remove_lst = what_to_remove(fmt, hubic_backup_folders.keys())
# Effectively remove folders
for remove_fold in remove_lst:
    filesinfold = hubic_backup_folders[remove_fold]
    filesinfold.reverse()
    args = (['delete', 'default'] + filesinfold)
    print(cloud.swift(args))


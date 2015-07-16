import hubic

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

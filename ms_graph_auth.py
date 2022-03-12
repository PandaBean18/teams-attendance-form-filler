#This file in particular has been taken from microsoft azure auth samples on github 
#I have wrapped the code in a class because i thought it would be more managable like that. 
#I have also tried to keep most comments from original example so that what I have done makes sense (hopefully)

import sys
import json
import logging
import requests
import msal

class MsGraphAuth:

    def __init__(self, params_file):
        self.config = json.load(open(params_file))
        self.app = msal.ClientApplication(self.config["client_id"], authority=self.config["authority"],client_credential=self.config.get("client_secret"))
                        # token_cache=...  # Default cache is in memory only.
                       # You can learn how to use SerializableTokenCache from
                       # https://msal-python.readthedocs.io/en/latest/#msal.SerializableTokenCache
        
        self.result = None 
        self.accounts = self.app.get_accounts(username = self.config['username']) #Checking the cache to see if user has signed in before

    def log_in(self):
        #Checking the cache to see if user has signed in before
        if self.accounts: 
            logging.info("Account(s) exists in cache, probably with token too. Let's try.")
            print('Account exists in cache.')
            self.result = self.app.acquire_token_silent(self.config["scope"], account=accounts[0])
        
        if not self.result: 
            logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
            print('Account does not exist in cache, we will need to get a new token.')
            # See this page for constraints of Username Password Flow.
            # https://github.com/AzureAD/microsoft-authentication-library-for-python/wiki/Username-Password-Authentication
            self.result = self.app.acquire_token_by_username_password(
                self.config["username"], self.config["password"], scopes=self.config["scope"])
        
        if "access_token" in self.result:
            # Calling graph using the access token
            # graph_data = requests.get(  # Use token to call downstream service
            #     self.config["endpoint"],
            #     headers={'Authorization': 'Bearer ' + self.result['access_token']},).json()
            #print("Graph API call result: %s" % json.dumps(graph_data, indent=2))
            print('access token received.')
            return True 
        else:
            print(self.result.get("error"))
            print(self.result.get("error_description"))
            print(self.result.get("correlation_id"))  # You may need this when reporting a bug
            if 65001 in self.result.get("error_codes", []):  # Not mean to be coded programatically, but...
                # AAD requires user consent for U/P flow
                print("Visit this to consent:", self.app.get_authorization_request_url(self.config["scope"]))

            return False 

    def get_data(self):
        endpoint = self.config['endpoint']
        data = requests.get(endpoint, headers = {'Authorization': 'Bearer ' + self.result['access_token']}).json()
        print('Data received from api.')
        return data

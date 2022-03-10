#
# Billtrust Collections Library
#
# Set of Python functions to make interacting with the
# Billtrust Collections APIs simpler
#

#
# Changelog
#
# DATE         AUTHOR   COMMENTS
# -----------  -------  ---------
# 2021-12-29   JJ Lay   Initial version
#

#
# References:
# [1] Billtrust documentation. https://api-docs.aws-prod.billtrust.com/
#

import requests
import sys
import json
import os
from inspect import currentframe, getframeinfo
import logging


#########################################################################
#
# Function: login()
#
# Parameters:
#    email : email address of account (str)
#    password : password for the account (str)
#
# Returns:
#    accessToken for session
#
# See also:
#    Billtrust Python Code Samples
#    https://api-docs.aws-prod.billtrust.com/examples/python/
#
# TODO:
#    - Adding logging
#
#########################################################################

def login(email, password) -> str :
    login_uri = "https://arc-aegis.billtrust.com/authentication/v1/login"
    login_headers = {"Accept":"application/json", "Content-Type":"application/json"}
    login_request = {"email":email, "password":password}
    login_response = requests.post(login_uri, json=login_request, headers=login_headers)
    login_response.raise_for_status()
    login_resp_json = login_response.json()

    return login_resp_json["accessToken"]


#########################################################################
#
# Function: logout()
#
# Parameters:
#    access_token : access token for session (str)
#
# Returns:
#    nothing
#
# See also:
#    Billtrust Python Code Samples
#    https://api-docs.aws-prod.billtrust.com/examples/python/
#
# TODO:
#    - Adding logging
#
#########################################################################

def logout(access_token):
    logout_uri = "https://arc-aegis.billtrust.com/authentication/v1/logout"
    logout_headers = {"Accept":"application/json", "Content-Type":"application/json"}
    logout_request = {'accessToken':access_token}
    logout_response = requests.post(logout_uri, json=logout_request, headers=logout_headers)
    logout_response.raise_for_status()
    return


#########################################################################
#
# Function: get_users_for_tenant()
#
# Parameters:
#    access_token : access token for session (str)
#    tenant_id : tenant id to query (str)
#
# Returns:
#    json with a list of users
#
# See also:
#    Billtrust Python Code Samples
#    https://api-docs.aws-prod.billtrust.com/examples/python/
#
# TODO:
#    - Adding logging
#
#########################################################################

def get_users_for_tenant(access_token, tenant_id) -> json :
    users_uri = f"https://arc-aegis.billtrust.com/user/v1/tenants/{tenant_id}/users"
    users_headers = {"Accept":"application/json", "X-Billtrust-Auth":access_token}
    users_response = requests.get(users_uri, headers=users_headers)
    users_response.raise_for_status()
    
    return users_response.json()


#########################################################################
#
# Function: get_accounts_for_tenant()
#
# Parameters:
#    access_token : access token for session (str)
#    tenant_id : tenant id to query (str)
#
# Returns:
#    json with a list of accounts
#
# See also:
#    Billtrust Python Code Samples
#    https://api-docs.aws-prod.billtrust.com/examples/python/
#
# TODO:
#    - Adding logging
#
#########################################################################

def get_accounts_for_tenant(access_token, tenant_id) -> json :
    accounts_uri = f"https://arc-aegis.billtrust.com/collections/api/v1/tenants/{tenant_id}/collectioncustomers?page=1&pageSize=100000"
    accounts_headers = {"Accept":"application/json", "X-Billtrust-Auth":access_token}
    accounts_response = requests.get(accounts_uri, headers=accounts_headers)
    accounts_response.raise_for_status()
    
    return accounts_response.json()


#########################################################################
#
# Function: get_contacts_for_account()
#
# Parameters:
#    access_token : access token for session (str)
#    tenant_id : tenant id to query (str)
#    account_number : customer account number (not Billtrust accountid) 
#
# Returns:
#    json with a list of contacts
#
# See also:
#    Billtrust Python Code Samples
#    https://api-docs.aws-prod.billtrust.com/examples/python/
#
# TODO:
#    - Adding logging
#
#########################################################################

def get_contacts_for_account(access_token, tenant_id, account_number) -> json :
    contacts_uri = f"https://arc-aegis.billtrust.com/collections/api/v1/tenants/{tenant_id}/collectioncustomers/accountnumber/{account_number}/collectioncontacts"
    contacts_headers = {"Accept":"application/json", "Content-Type": "application/json", "X-Billtrust-Auth":access_token}
    contacts_response = requests.get(contacts_uri, headers=contacts_headers)
    contacts_response.raise_for_status()

    return contacts_response.json()


#########################################################################
#
# Function: add_contact_to_account()
#
# Parameters:
#    access_token : access token for session (str)
#    tenant_id : tenant id to query (str)
#    account_number : customer account number (not Billtrust accountid) (str)
#    first_name : (str)
#    last_name : (str)
#    language : (str)
#    timezone : (str)
#    notes : (str)
#    email : (str)
#    officePhone : (str)
#    cellPhone : (str)
#    fax : (str)
#    title : (str)
#    address1 : (str)
#    address2 : (str)
#    city : (str)
#    state : (str)
#    zip : (str)
#    country : (str)
#    updatedOn : (str)
#    updatedBy : (str)
#    includeInCorrespondence : (str)
#
# Returns:
#    json with the response from the API
#
# See also:
#    Billtrust Python Code Samples
#    https://api-docs.aws-prod.billtrust.com/examples/python/
#
# TODO:
#    - Use the updatedOn and updatedBy fields
#    - Clean up logging
#    - Gracefully handle the apostrophe and backslash in strings
#
#########################################################################

def add_contact_to_account(access_token, tenant_id, account_number, first_name, 
                           last_name, language, timezone, notes, email, officePhone,
                           cellPhone, fax, title, address1, address2, city, state, zip,
                           country, updatedOn, updatedBy, includeInCorrespondence) -> json :

    notes = notes.replace('"', '')
    notes = notes.replace("'", '')

    if len(language) < 2 :
        language = 'en'

    if len(timezone) < 4 :
        timezone = 'America/Chicago'

    return_value = ''

    try :
        first_name = first_name.replace("\\", "\\\\")
        last_name = last_name.replace("\\", "\\\\")
        contact_body_string =  '{ ' + '"firstName" : "{}", '.format(first_name) + \
                            '  "lastName"  : "{}", '.format(last_name) + \
                            '  "language"  : "{}", '.format(language) + \
                            '  "notes"  : "{}", '.format(notes) + \
                            '  "email"  : "{}", '.format(email) + \
                            '  "officePhone"  : "{}", '.format(officePhone) + \
                            '  "cellPhone"  : "{}", '.format(cellPhone) + \
                            '  "fax"  : "{}", '.format(fax) + \
                            '  "title"  : "{}", '.format(title) + \
                            '  "address1"  : "{}", '.format(address1) + \
                            '  "address2"  : "{}", '.format(address2) + \
                            '  "timezone"  : "{}", '.format(timezone) + \
                            '  "IncludeInCorrespondence" : "{}" '.format(includeInCorrespondence) + \
                            ' }'
        contact_body = json.loads(contact_body_string)
        contact_uri = f"https://arc-aegis.billtrust.com/collections/api/v1/tenants/{tenant_id}/collectioncustomers/accountNumber/{account_number}/collectioncontacts"

        contact_headers = {"Accept":"application/json", "X-Billtrust-Auth":access_token}

        contact_response = requests.post(contact_uri, headers=contact_headers, json=contact_body)
        contact_response.raise_for_status()
        return_value = contact_response.json()

    except Exception as error:
        frame = getframeinfo(currentframe())
        filename = frame.filename
        line = str(frame.lineno)

        logging.error('\n===== INSERT CONTACT =====')
        logging.error('   Failed to insert contact')
        logging.error('   File: ' + filename)
        logging.error('   Function: ' + __name__)
        logging.error('   Line: ' + line)
        logging.error('   Account: ' + account_number)
        logging.error('   First Name: ' + first_name)
        logging.error('   Last Name: ' + last_name)
        logging.error('   Email: ' + email)
        logging.error('\n')
        logging.error(contact_body)
        logging.error('\n')
        logging.error(str(error))
        logging.error('\n')
        if len(return_value) > 0 :
            logging.error(json.dumps(return_value, indent=3))
        logging.error('----------------------------------------------------\n\n')

    return contact_response.json()



#########################################################################
#
# Function: contact_internalid_lookup()
#
# Parameters:
#    access_token : access token for session (str)
#    tenant_id : tenant id to query (str)
#    account_number : customer account number (not Billtrust accountid) (str)
#    first_name : (str)
#    last_name : (str)
#
# Returns:
#    string with the internal Billtrust Contact Id if found or empty 
#    string if not
#
# See also:
#    Billtrust Python Code Samples
#    https://api-docs.aws-prod.billtrust.com/examples/python/
#
# TODO:
#    - Gracefully handle the apostrophe and backslash in strings
#
#########################################################################

def contact_internalid_lookup(access_token, tenant_id, account_number, firstname, lastname) -> str :
    try:
        contact_list = get_contacts_for_account(access_token, tenant_id, account_number)

        for contact in contact_list:
            if contact['firstName'] == firstname and contact['lastName'] == lastname :
                return contact['id']

    except Exception as error:
        logging.warning('Failed to find contact internal id for Account Number: ' + account_number + ', First Name: ' + firstname + ', Last Name: ' + lastname)

    return ''


#########################################################################
#
# Function: account_internalid_lookup()
#
# Parameters:
#    access_token : access token for session (str)
#    tenant_id : tenant id to query (str)
#    account_number : customer account number (not Billtrust accountid) (str)
#
# Returns:
#    string with the internal Billtrust Account Id if found or empty 
#    string if not
#
# Comments:
#    You will need to change the field name of the account number to
#    match your Billtrust configuration. In the code below, the 
#    customer's number is in a field called "custNo".
#
# See also:
#    Billtrust Python Code Samples
#    https://api-docs.aws-prod.billtrust.com/examples/python/
#
# TODO:
#    - Gracefully handle the apostrophe and backslash in strings
#
#########################################################################

def account_internalid_lookup(access_token, tenant_id, account_number) -> str :
    try:
        accounts_uri = f"https://arc-aegis.billtrust.com/collections/api/v1/tenants/{tenant_id}/customermasters/customernumber/{account_number}"
        accounts_headers = {"Accept":"application/json", "Content-Type": "application/json", "X-Billtrust-Auth":access_token}
        accounts_response = requests.get(accounts_uri, headers=accounts_headers)
        accounts_response.raise_for_status()
        accounts_json = accounts_response.json()

        this_tenant = accounts_json['tenantId']
        this_id = accounts_json['id']
        this_customer = accounts_json['custNo']  # Update if needed

        return this_id

    except Exception as error:
        logging.warning('Failed to find account internal id for Account Number: ' + account_number)


    return ''


#########################################################################
#
# Function: contact_delete()
#
# Parameters:
#    access_token : access token for session (str)
#    tenant_id : tenant id to query (str)
#    account_number : customer account number (not Billtrust accountid) (str)
#    contact_id : internal Billtrust contact id (str)
#
# Returns:
#    nothing
#
# See also:
#    Billtrust Python Code Samples
#    https://api-docs.aws-prod.billtrust.com/examples/python/
#
# TODO:
#    - Gracefully handle the apostrophe and backslash in strings
#
#########################################################################

def contact_delete(access_token, tenant_id, account_number, contact_id):
    try:
        
        accounts_uri = f"https://arc-aegis.billtrust.com/collections/api/v1/tenants/{tenant_id}/collectioncustomers/accountNumber/{account_number}/collectioncontacts/{contact_id}"
        accounts_headers = {"Accept":"application/json", "Content-Type": "application/json", "X-Billtrust-Auth":access_token}
        accounts_response = requests.delete(accounts_uri, headers=accounts_headers)
        accounts_response.raise_for_status()
        accounts_json = accounts_response.json()
        return 

    except Exception as error:
        frame = getframeinfo(currentframe())
        filename = frame.filename
        line = str(frame.lineno)

        logging.error('\n===== DELETE CONTACT =====')
        logging.error('   Failed to delete contact')
        logging.error('   File: ' + filename)
        logging.error('   Function: ' + __name__)
        logging.error('   Line: ' + line)
        logging.error('   Account: ' + account_number)
        logging.error('   ContactId: ' + contact_id)
        logging.error(str(error))
        logging.error('\n')
        logging.error('----------------------------------------------------\n\n')

    return 


#########################################################################
#
# Function: contact_update()
#
# Parameters:
#    access_token : access token for session (str)
#    tenant_id : tenant id to query (str)
#    account_number : customer account number (not Billtrust accountid) (str)
#    first_name : (str)
#    last_name : (str)
#    language : (str)
#    timezone : (str)
#    notes : (str)
#    email : (str)
#    officePhone : (str)
#    cellPhone : (str)
#    fax : (str)
#    title : (str)
#    address1 : (str)
#    address2 : (str)
#    city : (str)
#    state : (str)
#    zip : (str)
#    country : (str)
#    updatedOn : (str)
#    updatedBy : (str)
#    includeInCorrespondence : (str)
#    
# Returns:
#    nothing
#
# Comments:
#    You may need to change field names to match your installation.
#
# See also:
#    Billtrust Python Code Samples
#    https://api-docs.aws-prod.billtrust.com/examples/python/
#
# TODO:
#    - Gracefully handle the apostrophe and backslash in strings
#    - Clean up logging
#    - Update only fields that changed
#
#########################################################################

def contact_update(access_token, tenant_id, account_number, contact_id, first_name, 
                           last_name, language, timezone, notes, email, officePhone,
                           cellPhone, fax, title, address1, address2, city, state, zip,
                           country, updatedOn, updatedBy, includeInCorrespondence) -> json :

    notes = notes.replace('"', '')
    notes = notes.replace("'", '')

    if len(language) < 2 :
        language = 'en'

    if len(timezone) < 4 :
        timezone = 'America/Chicago'

    try :
        update_body_string =  \
            '[{' + \
            '"value" : "' + format(first_name) + '", ' + \
            '"path" : "FirstName", ' + \
            '"op" : "replace" ' + \
            '}, ' + \
            '{' + \
            '"value" : "' + format(last_name) + '", ' + \
            '"path" : "LastName", ' + \
            '"op" : "replace" ' + \
            '}, ' + \
            '{' + \
            '"value" : "' + format(language) + '", ' + \
            '"path" : "Language", ' + \
            '"op" : "replace"' + \
            '}, ' + \
            '{' + \
            '"value" : "' + format(notes) + '", ' + \
            '    "path" : "Notes", ' + \
            '    "op" : "replace" ' + \
            '  }, ' + \
            '  {  ' + \
            '    "value" : "' + format(email) + '", ' + \
            '    "path" : "Email", ' + \
            '    "op" : "replace" ' + \
            '  }, ' + \
            '  {  ' + \
            '    "value" : "' + format(officePhone) + '", ' + \
            '    "path" : "OfficePhone", ' + \
            '    "op" : "replace" ' + \
            '  }, ' + \
            ' {' + \
            '    "value" : "' + format(cellPhone) + '", ' + \
            '    "path" : "CellPhone", ' + \
            '    "op" : "replace" ' + \
            '},  ' + \
            ' {' + \
            '    "value" : "' + format(fax) + '", ' + \
            '    "path" : "Fax", ' + \
            '    "op" : "replace" ' + \
            '},  ' + \
            '  {  ' + \
            '    "value" : "' + format(title) + '", ' + \
            '    "path" : "Title", ' + \
            '    "op" : "replace" ' + \
            '},  ' + \
            '  {  ' + \
            '    "value" : "' + format(address1) + '", ' + \
            '    "path" : "Address1", ' + \
            '    "op" : "replace" ' + \
            '},  ' + \
            '  {  ' + \
            '    "value" : "' + format(address2) + '", ' + \
            '    "path" : "Address2", ' + \
            '    "op" : "replace" ' + \
            '},  ' + \
            '  {  ' + \
            '    "value" : "' + format(city) + '", ' + \
            '    "path" : "City", ' + \
            '    "op" : "replace" ' + \
            '},  ' + \
            '  {  ' + \
            '    "value" : "' + format(state) + '", ' + \
            '    "path" : "State", ' + \
            '    "op" : "replace" ' + \
            '},  ' + \
            '  {  ' + \
            '    "value" : "' + format(zip) + '", ' + \
            '    "path" : "Zip", ' + \
            '    "op" : "replace" ' + \
            '},  ' + \
            '  {  ' + \
            '    "value" : "' + format(country) + '", ' + \
            '    "path" : "Country", ' + \
            '    "op" : "replace" ' + \
            '},  ' + \
            '  {  ' + \
            '    "value" : "' + format(timezone) + '", ' + \
            '    "path" : "TimeZone", ' + \
            '    "op" : "replace" ' + \
            '},  ' + \
            '  {  ' + \
            '    "value" : "' + format(includeInCorrespondence) + '", ' + \
            '    "path" : "IncludeInCorrespondence", ' + \
            '    "op" : "replace" ' + \
            '}]'

        update_body = json.loads(update_body_string)
        update_uri = f"https://arc-aegis.billtrust.com/collections/api/v1/tenants/{tenant_id}/collectioncustomers/accountNumber/{account_number}/collectioncontacts/{contact_id}"
        update_headers = {"Accept":"application/json", "X-Billtrust-Auth":access_token}

        return_value = ''
    
        update_response = requests.patch(update_uri, headers=update_headers, json=update_body)
        update_response.raise_for_status()
        return_value = update_response.json()

    except Exception as error:
        frame = getframeinfo(currentframe())
        filename = frame.filename
        line = str(frame.lineno)

        logging.error('\n===== UPDATE CONTACT =====')
        logging.error('   Failed to update contact')
        logging.error('   File: ' + filename)
        logging.error('   Function: ' + __name__)
        logging.error('   Line: ' + line)
        logging.error('   Account: ' + account_number)
        logging.error('   First Name: ' + first_name)
        logging.error('   Last Name: ' + last_name)
        logging.error('   Email: ' + email)
        logging.error(str(error))
        logging.error('\n')
        if len(return_value) > 0 :
            logging.error(json.dumps(return_value, indent=3))
        logging.error('----------------------------------------------------\n\n')

    return return_value

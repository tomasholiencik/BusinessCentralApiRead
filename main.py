import requests
from msal import ConfidentialClientApplication

def get_bc_data(access_token, company_id, environment_name, endpoint, query=None):
    '''
    Returns the data from the specified endpoint in Business Central.
    Returrns data in JSON format.
    '''
    #contruct the url for request
    base_url = f'https://api.businesscentral.dynamics.com/v2.0/{environment_name}/api/v2.0/'
    company = f'companies({company_id})/'
    
    url =  base_url + company + endpoint
    #add expand to display cost centers in case of generalLedgerEntries endpoint and ads query at the end
    if endpoint == 'generalLedgerEntries':
        expand = '$expand=dimensionSetLines'
        url += '?' + expand
        if query:
            url += "&" + query
   
    #add query if provided
    elif query:
        url += "" + query

    # Make the request    
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
        # Process the data as needed
    else:
        print(f"Error: {response.status_code} - {response.text}")

def auth_msal_bc(client_id,client_secret,tenant_id):
    '''
    authenticates with MSAL and returns the access token
    '''
    # Set the MSAL parameters
    authority = "https://login.microsoftonline.com/" + tenant_id
    scope = ["https://api.businesscentral.dynamics.com/.default"]
    
    # Get the access token
    app = ConfidentialClientApplication(
        client_id, authority=authority, client_credential=client_secret
    )
    
    response = app.acquire_token_for_client(scopes=scope)

    if "access_token" in response:
        return response["access_token"]
    else:
        print(f"Error: {response.status_code} - {response.text}")
              
def main():
    # Set the authorization parameters
    client_id = 'your_entraId_app_client_id'
    client_secret = 'your_entraId_app_client_id'
    tenant_id = 'your_tenant_id'
    
    # Get the access token
    access_token = auth_msal_bc(client_id,client_secret,tenant_id)

    # Set the parameters for the data request
    company_id = 'your_company_id'
    environment_name = 'your_environment_name'
    endpoint = 'your_endpoint'
    #do not add ? at the beginning of the query since this already in constructor, begin with $filter
  
    query="$filter=lastModifiedDateTime ge 2023-07-30T00:00:00Z and lastModifiedDateTime lt 2023-07-31T00:00:00Z" 
    #this does not work with Z at the end despite optional in documentation

    #alternative query to filter on documentNumber
    #query="$filter=documentNumber eq '04-2023/0001-00338'" 

    # Get the data
    data = get_bc_data(access_token, company_id, environment_name, endpoint, query)

    return data

if __name__ == "__main__":
    
    data= main()

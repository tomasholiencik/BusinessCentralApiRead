# Dynamics365 Business Central Data Extraction Application

This application is designed for extracting data from Dynamics 365 Business Central for corporate controlling purposes.

## Table of Contents

- [Overview](#overview)
- [Functions](#functions)
    - [get_bc_data](#get_bc_data-function-documentation)
    - [auth_msal_bc](#auth_msal_bc-function-documentation)
- [Usage Example](#usage-example)
    - [code usage example](#code-usage-example)
    - [return data example](#return-data-example-generalLedgerEntries-endpoint)

## Overview

This Python application provides two main functions for extracting data from Dynamics 365 Business Central (D365BC). The `get_bc_data` function retrieves data from a D365BC API endpoint, while the `auth_msal_bc` function is responsible for obtaining an access token for authentication with the D365BC API. These functions are designed to facilitate data extraction and analysis for corporate controlling purposes.

## Functions

### `get_bc_data` Function Documentation

#### Description

The `get_bc_data` function retrieves data from a Dynamics 365 Business Central API endpoint using an access token obtained from the `auth_msal_bc` function. It requires company-specific parameters and allows for optional query parameters. This function manages the HTTP request to the specified API endpoint and returns the response data when the HTTP status code is 200. If the status code is different from 200, it prints an error message and returns `None`.

#### Parameters

- `access_token` (str): The access token required for authenticating with the Dynamics 365 Business Central API, which is obtained from the `auth_msal_bc` function.

- `company_id` (str): The identifier for the company within the Business Central environment. Provided by D365BC admin.

- `environment_name` (str): The name of the Dynamics 365 Business Central environment. Provided by D365BC admin.

- `endpoint` (str): The specific endpoint or path for the API resource you wish to access. You can find a list of available endpoints in the [official documentation](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/api-reference/v2.0/). Use [generalLedgerEntries](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/api-reference/v2.0/resources/dynamics_generalledgerentry) to obtain general ledger entries. Only endpoint generalLedgerEntries will be automatically expanded with dimensionSetLines containing cost center data (see [return data example](#return-data-example-generalLedgerEntries-endpoint) )

- `query` (str, optional): Additional query parameters to include in the request URL. The default is `None`. These parameters can be used to reduce the response size or enable incremental refresh, particularly in conjunction with the 'lastModifiedDateTime' field. For more details, refer to the [official documentation](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-connect-apps-filtering).

#### Returns

- `dict` or `None`: If the HTTP response status code is 200, the function returns the JSON data obtained from the API. In case the status code is different from 200, the function will print an error message and return `None`.

### Dependencies

This function relies on the Python `requests` library for making HTTP requests to the Dynamics 365 Business Central API. You can install this library using the following command:

```bash
pip install requests
```

### `auth_msal_bc` Function Documentation

#### Description

The `auth_msal_bc` function is designed to obtain an access token for Microsoft Business Central (BC) using the Microsoft Authentication Library (MSAL) and Azure Active Directory (Azure AD) authentication. This access token can be used to authenticate and make authorized API calls to Microsoft Business Central.

#### Parameters

- **client_id** (str): The client ID of the Azure AD application registered in the Azure portal. This is a unique identifier for your application.

- **client_secret** (str): The client secret of the Azure AD application. This secret is used as a credential to authenticate the application.

- **tenant_id** (str): The Azure AD tenant ID or directory ID where the application is registered. This identifies the Azure AD directory that contains the application.

#### Return Value

If the function successfully obtains an access token, it returns the access token as a string.

If an error occurs during the token acquisition process, the function prints an error message and returns `None`.

#### Dependencies

This function relies on the `ConfidentialClientApplication` class, which should be provided by the MSAL library. Ensure you have the MSAL library installed and configured in your project.

- MSAL library documentation: [MSAL ConfidentialClientApplication](https://learn.microsoft.com/en-us/python/api/msal/msal.application.confidentialclientapplication?view=msal-py-latest)

## Usage Example

Example of extract of general ledger entries increment for day 30.07.2023

### Code usage example
```python
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
    query="?$filter=lastModifiedDateTime ge 2023-07-30T00:00:00Z and lastModifiedDateTime lt 2023-07-31T00:00:00Z" 

    #this does not work with Z at the end despite optional in documentation

    # Get the data
    data = get_bc_data(access_token, company_id, environment_name, endpoint, query)

    return data

```

### Return data example `generalLedgerEntries` endpoint

```json
{
  "@odata.context": "https://api.businesscentral.dynamics.com/v2.0/AT/api/v2.0/$metadata#companies(bfd3d48a-7b14-ee11-8f6e-6045bd9dec5b)/generalLedgerEntries",
  "value": [
    {
      "@odata.etag": "W/\"JzE5Ozg3NTYwMDU2MjU5MjMyNjY9MzM1OzAwOyc=\"",
      "id": "ca6ceb25-172f-ee11-9cbf-6045bd92547f",
      "entryNumber": 4319,
      "postingDate": "2023-01-31",
      "documentNumber": "01-2023/0002-LV",
      "documentType": "_x0020_",
      "accountId": "647d3708-7c14-ee11-8f6e-6045bd9dec5b",
      "accountNumber": "37900",
      "description": "LV",
      "debitAmount": 0,
      "creditAmount": 259.31,
      "lastModifiedDateTime": "2023-07-30T20:24:57.213Z",
      "dimensionSetLines": [
        {
          "@odata.etag": "W/\"JzIwOzEwMTU3MTU1MDQ3ODUxOTM3MTYyMTswMDsn\"",
          "id": "4a0db8ab-8014-ee11-8f6e-6045bd9dec5b",
          "code": "COSTCENTER",
          "parentId": "ca6ceb25-172f-ee11-9cbf-6045bd92547f",
          "parentType": "General_x0020_Ledger_x0020_Entry",
          "displayName": "Cost Center",
          "valueId": "560db8ab-8014-ee11-8f6e-6045bd9dec5b",
          "valueCode": "780109",
          "valueDisplayName": "Bergbahnen /Führung"
        }
      ]
    }
  ]
}
```

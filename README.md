# Dynamics365 Business Central Data Extraction Application

This application is designed for extracting data from Dynamics 365 Business Central for corporate controlling purposes.

## Table of Contents

- [Overview](#overview)
- [Functions](#functions)
    - [get_bc_data](#get_bc_data-function-documentation)
    - [auth_msal_bc](#auth_msal_bc-function-documentation)
- [Usage example with lastModifiedDateTime parameter](#usage-example-with-filter-on-lastmodifieddatetime)
    - [code usage](#code-with-filter-on-lastmodifieddatetime)
    - [return data](#return-data-with-filter-on-lastmodifieddatetime)
- [Usage example with documentNumber parameter](#usage-example-with-filter-on-documentnumber)
    - [parameter setting](#filter-parameter)
    - [return data example](#return-data-with-filter-on-documentnumber)

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

- `endpoint` (str): The specific endpoint or path for the API resource you wish to access. You can find a list of available endpoints in the [official documentation](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/api-reference/v2.0/).
  
    Use [generalLedgerEntries](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/api-reference/v2.0/resources/dynamics_generalledgerentry) endpoint to obtain general ledger entries. One document (posting) in accounting consists of two or more general ledger entries (posting rows).

  Only endpoint `generalLedgerEntries` will be automatically expanded with `dimensionSetLines` containing dimensions data e.g. Cost Center, CAPEX (see [return data example](##return-data-with-filter-on-lastmodifieddatetime) ). Only dimensions with values assigned are shown under dimensionSetLines of ledger entry: e.g. if ledger entry has cost center assigned, but no capex , there will be only one item (cost center) shown in dimensionSetLines list (see [return data example](#return-data-with-filter-on-documentNumber))

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

## Usage example with filter on lastModifiedDateTime 

Example of extract of general ledger entries created or modified on 16.11.2023 using `lastModifiedDateTime` parameter in filter.

lastModifiedDateTime key shows datetime of creation or any changes in ledger entry (posting row). Therefore query by paramater lastModifiedDateTime may deliver not only new entries but also updated entries. Such an update could be also correction in dimension valueslie in the emaple case like in this case.


### Code with filter on lastModifiedDateTime
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
    query="?$query="$filter=lastModifiedDateTime ge 2023-11-16T00:00:00Z and lastModifiedDateTime lt 2023-11-17T00:00:00Z" 

    #this does not work with Z at the end despite optional in documentation

    # Get the data
    data = get_bc_data(access_token, company_id, environment_name, endpoint, query)

    return data

```

### Return data with filter on lastModifiedDateTime

```json
{
  "@odata.context": "https://api.businesscentral.dynamics.com/v2.0/AT/api/v2.0/$metadata#companies(bfd3d48a-7b14-ee11-8f6e-6045bd9dec5b)/generalLedgerEntries",
  "value": [
    {
      "@odata.etag": "W/\"JzIwOzE3MjIyMTQ1MjY1MTY4OTE3ODg4MTswMDsn\"",
      "id": "13fd87a0-8414-ee11-8f6e-6045bd9dec5b",
      "entryNumber": 1897,
      "postingDate": "2023-04-28",
      "documentNumber": "04-2023/0001-00338",
      "documentType": "Invoice",
      "accountId": "f6eb300e-7c14-ee11-8f6e-6045bd9dec5b",
      "accountNumber": "72102",
      "description": "Hydraulik Blasy G.m.b.H",
      "debitAmount": 46.17,
      "creditAmount": 0,
      "lastModifiedDateTime": "2023-11-16T15:44:53.277Z",
      "dimensionSetLines": [
        {
          "@odata.etag": "W/\"JzIwOzEzNjUxMzM2ODQwMjYwMDA5OTQzMTswMDsn\"",
          "id": "4a0db8ab-8014-ee11-8f6e-6045bd9dec5b",
          "code": "COSTCENTER",
          "parentId": "13fd87a0-8414-ee11-8f6e-6045bd9dec5b",
          "parentType": "General_x0020_Ledger_x0020_Entry",
          "displayName": "Cost Center",
          "valueId": "580db8ab-8014-ee11-8f6e-6045bd9dec5b",
          "valueCode": "780111",
          "valueDisplayName": "Muttereralmbahn"
        },
        {
          "@odata.etag": "W/\"JzE5Ozg1NDY3MjU4NDUyMjAxOTIxNjUxOzAwOyc=\"",
          "id": "4b0db8ab-8014-ee11-8f6e-6045bd9dec5b",
          "code": "CAPEX",
          "parentId": "13fd87a0-8414-ee11-8f6e-6045bd9dec5b",
          "parentType": "General_x0020_Ledger_x0020_Entry",
          "displayName": "Capex Code",
          "valueId": "18535a54-9684-ee11-817a-00224880b3d4",
          "valueCode": "12456",
          "valueDisplayName": "axess system"
        }
      ]
    }
  ]
}

```

## Usage example with filter on documentNumber 

Example of extraction of ledger entries (posting rows) for given document (posting) 

### Filter parameter
Using the code from [example in previous section](#code-with-filter-on-lastmodifieddatetime), query can be adapted to get all ledger entries for document. Please note that only dimension with values assigned are shown. 

```python
    ...
    query="$filter=documentNumber eq '04-2023/0001-00338'" 
    ...
```

### Return data with filter on documentNumber
```json
{
  "@odata.context": "https://api.businesscentral.dynamics.com/v2.0/AT/api/v2.0/$metadata#companies(bfd3d48a-7b14-ee11-8f6e-6045bd9dec5b)/generalLedgerEntries",
  "value": [
    {
      "@odata.etag": "W/\"JzIwOzE3MjIyMTQ1MjY1MTY4OTE3ODg4MTswMDsn\"",
      "id": "13fd87a0-8414-ee11-8f6e-6045bd9dec5b",
      "entryNumber": 1897,
      "postingDate": "2023-04-28",
      "documentNumber": "04-2023/0001-00338",
      "documentType": "Invoice",
      "accountId": "f6eb300e-7c14-ee11-8f6e-6045bd9dec5b",
      "accountNumber": "72102",
      "description": "Hydraulik Blasy G.m.b.H",
      "debitAmount": 46.17,
      "creditAmount": 0,
      "lastModifiedDateTime": "2023-11-16T15:44:53.277Z",
      "dimensionSetLines": [
        {
          "@odata.etag": "W/\"JzIwOzEzNjUxMzM2ODQwMjYwMDA5OTQzMTswMDsn\"",
          "id": "4a0db8ab-8014-ee11-8f6e-6045bd9dec5b",
          "code": "COSTCENTER",
          "parentId": "13fd87a0-8414-ee11-8f6e-6045bd9dec5b",
          "parentType": "General_x0020_Ledger_x0020_Entry",
          "displayName": "Cost Center",
          "valueId": "580db8ab-8014-ee11-8f6e-6045bd9dec5b",
          "valueCode": "780111",
          "valueDisplayName": "Muttereralmbahn"
        },
        {
          "@odata.etag": "W/\"JzE5Ozg1NDY3MjU4NDUyMjAxOTIxNjUxOzAwOyc=\"",
          "id": "4b0db8ab-8014-ee11-8f6e-6045bd9dec5b",
          "code": "CAPEX",
          "parentId": "13fd87a0-8414-ee11-8f6e-6045bd9dec5b",
          "parentType": "General_x0020_Ledger_x0020_Entry",
          "displayName": "Capex Code",
          "valueId": "18535a54-9684-ee11-817a-00224880b3d4",
          "valueCode": "12456",
          "valueDisplayName": "axess system"
        }
      ]
    },
    {
      "@odata.etag": "W/\"JzIwOzEyNzYyNzg3NTc0MTA0NTI0MDE3MTswMDsn\"",
      "id": "16fd87a0-8414-ee11-8f6e-6045bd9dec5b",
      "entryNumber": 1898,
      "postingDate": "2023-04-28",
      "documentNumber": "04-2023/0001-00338",
      "documentType": "Invoice",
      "accountId": "4d7d3708-7c14-ee11-8f6e-6045bd9dec5b",
      "accountNumber": "33000",
      "description": "Hydraulik Blasy G.m.b.H",
      "debitAmount": 0,
      "creditAmount": 55.4,
      "lastModifiedDateTime": "2023-07-30T18:11:59.583Z",
      "dimensionSetLines": [
        {
          "@odata.etag": "W/\"JzE5Ozg1MzYwMjM4NjcxMTkyODgyNzkxOzAwOyc=\"",
          "id": "4a0db8ab-8014-ee11-8f6e-6045bd9dec5b",
          "code": "COSTCENTER",
          "parentId": "16fd87a0-8414-ee11-8f6e-6045bd9dec5b",
          "parentType": "General_x0020_Ledger_x0020_Entry",
          "displayName": "Cost Center",
          "valueId": "580db8ab-8014-ee11-8f6e-6045bd9dec5b",
          "valueCode": "780111",
          "valueDisplayName": "Muttereralmbahn"
        }
      ]
    },
    {
      "@odata.etag": "W/\"JzE5OzI4NTY4NDc5OTgyNjM4OTU4ODQxOzAwOyc=\"",
      "id": "12fd87a0-8414-ee11-8f6e-6045bd9dec5b",
      "entryNumber": 1896,
      "postingDate": "2023-04-28",
      "documentNumber": "04-2023/0001-00338",
      "documentType": "Invoice",
      "accountId": "2d7d3708-7c14-ee11-8f6e-6045bd9dec5b",
      "accountNumber": "25000",
      "description": "Hydraulik Blasy G.m.b.H",
      "debitAmount": 9.23,
      "creditAmount": 0,
      "lastModifiedDateTime": "2023-07-30T18:11:59.58Z",
      "dimensionSetLines": [
        {
          "@odata.etag": "W/\"JzE5OzMwNTg2MTE3ODIxNjcyMTYwODcxOzAwOyc=\"",
          "id": "4a0db8ab-8014-ee11-8f6e-6045bd9dec5b",
          "code": "COSTCENTER",
          "parentId": "12fd87a0-8414-ee11-8f6e-6045bd9dec5b",
          "parentType": "General_x0020_Ledger_x0020_Entry",
          "displayName": "Cost Center",
          "valueId": "580db8ab-8014-ee11-8f6e-6045bd9dec5b",
          "valueCode": "780111",
          "valueDisplayName": "Muttereralmbahn"
        }
      ]
    }
  ]
}
```

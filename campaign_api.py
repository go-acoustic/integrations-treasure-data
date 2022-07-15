import requests
import os


def get_token():
    url = f"https://{os.environ['CA_API_SERVER']}/oauth/token"
    payload = f'grant_type=refresh_token&client_id={os.environ["CA_CLIENT_ID"]}&client_secret={os.environ["CA_CLIENT_SECRET"]}&refresh_token={os.environ["CA_REFRESH_TOKEN"]}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"Get token rest api call returned response with code: {response.status_code}")
    return response.json()['access_token']


def bulk_import(token, source_file, map_file):
    url = f"https://{os.environ['CA_API_SERVER']}/XMLAPI"
    payload = f"""
    <Envelope>
        <Body>
            <ImportList>
            <MAP_FILE>{map_file}</MAP_FILE>
            <SOURCE_FILE>{source_file}</SOURCE_FILE>
            </ImportList>
        </Body>
    </Envelope>
    """
    headers = {
        'Content-Type': 'text/xml',
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(f"Bulk import rest api call returned response with code: {response.status_code}")

"""Tool used to replicate any APIv3 500 error codes on test environments"""

from getpass import getpass
import warnings
import requests
from requests.auth import HTTPBasicAuth

# Constants
CONSOLE_URL = "https://bane2.vuln.lax.rapid7.com:3780"
ENDPOINT = "solutions"
USER = input("Enter the local console username: ")
PSWD = getpass("Enter the local console password: ")
# Size and page the customer was experiencing 5xx codes
CUSTOMER_SIZE = 1
CUSTOMER_PAGE = 0
# Calculates which resources to test based on the original size and page above
PAGE_START = CUSTOMER_SIZE * CUSTOMER_PAGE
PAGE_END = CUSTOMER_SIZE * (CUSTOMER_PAGE + 1)

def get_response_code(page_num:int = 0) -> int:
    """Handles the request auth and query params.
    Needs a page number,otherwise starts on page 0."""
    # Keep size = 1 for testing individual resources
    size = 1
    query_params = f"size={size}&page={page_num}"
    url = f"{CONSOLE_URL}/api/3/{ENDPOINT}?{query_params}"
    print(f"Sending request to {url}...")
    code = requests.get(url, auth=HTTPBasicAuth(USER, PSWD), verify=False).status_code
    print(f"Status code: {code}")
    return code

def main():
    """Loops through the original page 1 resource at a time.
    Prints any resources that responded with a 5xx code.
    Terminates the loop on any 4xx codes."""
    bad_resources = []
    current_page = max(0, PAGE_START)
    while current_page < PAGE_END:
        # Passes current page to use as a query parameter
        response_code = get_response_code(current_page)
        if response_code >= 500:
            bad_resources.append(current_page)
        elif response_code >= 400:
            print("Client-side error. Exiting test.")
            return
        current_page += 1

    # If the list isn't empty, print the bad resources found.
    if bad_resources:
        print(f"Bad resources found in size={CUSTOMER_SIZE}&page={CUSTOMER_PAGE}:\n{bad_resources}")

# Ignore the warning from requesting a self-signed certificate.
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    if __name__ == "__main__":
        main()

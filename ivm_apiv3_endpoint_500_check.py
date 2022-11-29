"""Tool used to replicate any APIv3 500 error codes on test environments"""

import warnings
import concurrent.futures as cf
import os
import requests
from requests.auth import HTTPBasicAuth

# Constants
CONSOLE_URL = os.environ["CONSOLE_URL"]
ENDPOINT = os.environ["ENDPOINT"]
USER = os.environ["CONSOLE_USER"]
PSWD = os.environ["CONSOLE_PASS"]
# Size and page the customer was experiencing 5xx codes
CUSTOMER_SIZE = os.environ["CUST_SIZE"]
CUSTOMER_PAGE = os.environ["CUST_PAGE"]
THREAD_COUNT = 10
# Calculates which resources to test based on the customer's query params
PAGE_START = CUSTOMER_SIZE * CUSTOMER_PAGE
PAGE_END = CUSTOMER_SIZE * (CUSTOMER_PAGE + 1)

def get_response_code(page_num:int = 0) -> int:
    """Handles the request auth and query params.
    Terminates the loop on any 4xx codes."""
    query_params = f"size=1&page={page_num}"
    url = f"{CONSOLE_URL}/api/3/{ENDPOINT}?{query_params}"
    print(f"Sending request to {url}...")
    code = requests.get(url, auth=HTTPBasicAuth(USER, PSWD), verify=False, timeout=90).status_code
    print(f"Status code: {code}")
    if 400 <= code < 500:
        print(f"Client-side error. Status Code {code}.\nExiting test.")
        exit()
    return code

def main():
    """Loops through the original page 1 resource at a time.
    Prints any resources that responded with a 5xx code."""
    bad_resources = []
    with cf.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        if THREAD_COUNT > 5:
            print("Thread count exceeds recommended number of 5.\
                \nServer responses may slow down as a result.")
        print(f"Sending {THREAD_COUNT} requests at a time to resources {PAGE_START}-{PAGE_END}...")
        results_dict = {
            # Dict in {Future:page_num} form.
            executor.submit(get_response_code, current_page): current_page
            for current_page in range (PAGE_START, PAGE_END)
            }
        # Iterates through results_dict's Futures to check for 500 or 400 Status
        for future in cf.as_completed(results_dict):
            # Future.result() contains the status code from get_response_code().
            response_code = future.result()
            if response_code >= 500:
                bad_resources.append(results_dict[future])
    print("Requests complete.")
    # If the list isn't empty, print the bad resources found.
    if bad_resources:
        print(f"Bad resources found in size={CUSTOMER_SIZE}&page={CUSTOMER_PAGE}:\n{bad_resources}")
    else:
        print(f"No bad resources found in size={CUSTOMER_SIZE}&page={CUSTOMER_PAGE}")

# Ignore the warning from requesting a self-signed certificate.
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    if __name__ == "__main__":
        main()

#TODO - Exception (KeyError) catching for env variables
#TODO - make into cli tool with passable args for CUSTOMER_SIZE, CUSTOMER_PAGE
#TODO - Replace warnings.simplefilter() with with urllib3 warning handling

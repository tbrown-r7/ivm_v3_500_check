# ivm_v3_500_check
Tool used to replicate any APIv3 500 error codes on test environments

Replace the ENDPOINT, CUSTOMER_SIZE, and CUSTOMER_PAGE values with the values the customer is experiencing issues with.

For example, if my customer is receiving a 500 status code when calling /api/3/solutions on page 46, size 500, I would do as follows:

ENDPOINT = "solutions"
CUSTOMER_SIZE = 500
CUSTOMER_PAGE = 46

This will calculate the 500 resources returned on page 46, then go through them individually and print the resources that return a 5xx status code.
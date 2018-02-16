#!/usr/bin/env python3

import requests
import json

# text
# U2FsdGVkX1+oinYiLwBHFWqde8jgZ1EKAIHgAVIjvG8duKGVrHRS51GA/IJllXw8V2Jej9olWjWUFPIDDk2t4KQcRtfU3bCwkpREdULuRgE9YK96A43tz4XeJ81jROK5GuGwGtOuQa6Fy63SMlz0sfANIzzlWJnEe6ftwqhOnC82q7+HIbeJghayfNZXlIcH5+8g+PP0VzGE1SCITGnPDdGHfGkg9CCzaQU3oZspSChyjHZVKgtitJkx+sfHPXLlL4f/ImSRekG6w2rjuZS6+s/v26MZb2ih/WTiTeUaQ0edn5xUmtgnMLng3ng9rxpU2Ias0HOzczs2yT/mMFTsul0YcGAIDUQXBGbSbmuGe9EtQ6eEBbcm6PjSNeOv4lj8oPFdwoI2l2gxqaxIJUw8YbpYtH/npKLzjk/o33nPM+Obi8X7NUQlsQ6XXtT14RKSc9HAzZwRJlD3jPU6bA5VOZf4miGmNCjgUezXp9Hgdi33U5PSWhAmUMM6pPMam22drJ/b8D5Fi1aMktUq098ljWlAGk7OVUaSrfpVvNSpoyU+Uu0SxzF2TiqiPlLuixwiAVHE/0phvBpUW6HoyhusB5FWpByTVXJNIYQYn2skUcS9lkHccoVCpwUTtH/3/bYUTulNseGYS+vQfShJmzGi++2lIVlmxPYFdr9DWldGGHiEFuhFCXx6eSSKqUNDkToFE0SjDTJKYFH79ouuLtur0T9QylCBz7rQSgZHEArxiEg=

# window.serialNumber + "@" + window.seller)
# C02SDDLEFVH3@yezi -> fb5832d83b3399a42cb50b8e1941641a

if __name__ == '__main__':
    data = requests.get('http://password.aollio.com')
    accounts = json.loads(data.text)
    print(accounts)

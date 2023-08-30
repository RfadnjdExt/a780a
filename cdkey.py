"""
CodeScribe
Total time: 29 minute
CD Key Information Retrieval Module

This module contains functions to retrieve CD key information using the provided parameters. It defines the following functions:

- get_cdkey_info(uid: int, cdkey: str, cookie: str, region: str, game_biz_parameter: str) -> str:
  Retrieves CD key information for a specific user, CD key, and region.

- main(cdkey: str, cookie: str) -> str:
  Main function to retrieve and display CD key information for various regions.

Usage:
1. Make sure to have the `requests` library installed using: `pip install requests`.
2. Call the `main` function with user ID, CD key, and cookie to fetch CD key information.

Requirements:
- Python 3.x
- The `requests` library

API Endpoints Used:
- `webExchangeCdkey` endpoint from "https://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/"

Note: This code is designed to retrieve CD key information from different regions and handle possible return codes.

"""
import requests

URL = "https://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey"


def get_cdkey_info(
    uid: int, cdkey: str, cookie: str, region: str, game_biz_parameter: str
) -> str:
    """
    Retrieve CD key information for a specific user, CD key, and region.

    This function makes a GET request to the CD key information retrieval API using the provided parameters.
    It processes the response and returns a string indicating the status of the CD key.

    Args:
        uid (int): User ID.
        cdkey (str): The CD key to exchange.
        cookie (str): User's cookie for authentication.
        region (str): Region to claim the CD key.
        game_biz_parameter (str): Additional game business parameter.

    Returns:
        str: A string indicating the status of the CD key.
            Possible return values: "success", "expired", "invalid", "already in use", "unknown".

    Note:
        The function requires the 'requests' library to be installed. Make sure to have it installed using:
        `pip install requests`.

    API Endpoint Used:
        'webExchangeCdkey' endpoint from "https://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/"
    """
    params = {
        "uid": uid,
        "region": region,
        "lang": "en",
        "cdkey": cdkey,
        "game_biz": game_biz_parameter,
        "sLangKey": "en-us",
    }
    headers = {"Cookie": cookie}
    with requests.get(URL, params=params, headers=headers, timeout=1) as response:
        cdkey_info = response.json()

    return {
        0: "success",
        -2001: "expired",
        -2003: "invalid",
        -2017: "already in use",
    }.get(cdkey_info["retcode"], "unknown")


def main(cdkey: str, cookie: str) -> str:
    """
    Main function to retrieve and display CD key information for various regions.

    This function iterates through a list of regions and makes requests to retrieve user game roles.
    For each region, it retrieves the first user game role and uses it to call the 'get_cdkey_info' function
    to fetch CD key information. The CD key information status is returned.

    Args:
        cdkey (str): The CD key to exchange.
        cookie (str): User's cookie for authentication.

    Returns:
        str: A string indicating the status of the CD key information.
            Possible return values: "success", "expired", "invalid", "already in use", "unknown".

    Note:
        The function requires the 'requests' library to be installed. Make sure to have it installed using:
        `pip install requests`.

    API Endpoint Used:
        'getUserGameRolesByCookieToken' endpoint from "https://api-account-os.hoyoverse.com/account/binding/api/"

    Dependencies:
        - The 'get_cdkey_info' function defined in this module.
    """
    regions = ["os_usa", "os_euro", "os_asia", "os_cht"]
    for region in regions:
        url = (
            "https://api-account-os.hoyoverse.com/account/binding/api/"
            "getUserGameRolesByCookieToken"
        )

        response = requests.get(
            url,
            {
                "lang": "en",
                "region": region,
                "game_biz": "hk4e_global",
                "sLangKey": "en-us",
            },
            headers={"Cookie": cookie},
            timeout=1,
        ).json()

        user_game_roles_data = response["data"]["list"]

        if user_game_roles_data:
            first_user_game_role = user_game_roles_data[0]
            cdkey_info = get_cdkey_info(
                first_user_game_role["game_uid"],
                cdkey,
                cookie,
                region,
                first_user_game_role["game_biz"],
            )
            return cdkey_info

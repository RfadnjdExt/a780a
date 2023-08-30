"""
CD Key Information Retrieval Module

This module contains functions to retrieve CD key information using the provided parameters.
It defines the following functions:

- get_cdkey_status(session: requests.Session, user_id: int, cd_key: str, target_region: str, game_biz_parameter: str) -> str:
  Retrieves CD key information status for a specific user, CD key, and region.

- main(cd_key: str, auth_cookie: str) -> dict:
  Main function to retrieve and display CD key information statuses for various regions and users.

Usage:
1. Make sure to have the `requests` and `dotenv` libraries installed using: `pip install requests python-dotenv`.
2. Call the `main` function with the CD key and authentication cookie to fetch CD key information statuses.

Requirements:
- Python 3.x
- The `requests` library
- The `dotenv` library

API Endpoints Used:
- `webExchangeCdkey` endpoint from "https://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/"
- 'getUserGameRolesByCookieToken' endpoint from "https://api-account-os.hoyoverse.com/account/binding/api/"

Note: This code is designed to retrieve CD key information from different regions and handle possible return codes.

"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()
CDKEY_API_URL = "https://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey"


def get_cdkey_status(
    session: requests.Session,
    user_id: int,
    cd_key: str,
    target_region: str,
    game_biz_parameter: str,
) -> str:
    """
    Retrieve CD key information status for a specific user, CD key, and region.

    Args:
        session (requests.Session): The active requests session.
        user_id (int): User ID.
        cd_key (str): The CD key to exchange.
        target_region (str): Region to claim the CD key.
        game_biz_parameter (str): Additional game business parameter.

    Returns:
        str: A string indicating the status of the CD key.
            Possible return values: "success", "expired", "invalid", "already in use", "unknown".
    """
    request_params = {
        "uid": user_id,
        "region": target_region,
        "lang": "en",
        "cdkey": cd_key,
        "game_biz": game_biz_parameter,
        "sLangKey": "en-us",
    }

    with session.get(CDKEY_API_URL, params=request_params, timeout=1) as response:
        cd_key_info = response.json()

    return {
        0: "success",
        -2001: "expired",
        -2003: "invalid",
        -2017: "already in use",
    }.get(cd_key_info["retcode"], "unknown")


def main(cd_key: str, auth_cookie: str) -> dict:
    """
    Retrieve and display CD key information statuses for various regions and users.

    This function iterates through a list of regions and makes requests to retrieve user game roles.
    For each region, it retrieves the first user game role and uses it to call the 'get_cdkey_info' function
    to fetch CD key information. The CD key information statuses are returned in a dictionary.

    Args:
        cd_key (str): The CD key to exchange.
        auth_cookie (str): User's cookie for authentication. account_id_v2 & cookie_token_v2 required!

    Returns:
        dict: A nested dictionary containing CD key information statuses for various regions and users.
    """
    cd_key_statuses = None
    session = requests.Session()
    session.headers.update({"Cookie": auth_cookie})
    target_regions = ["os_usa", "os_euro", "os_asia", "os_cht"]

    for target_region in target_regions:
        user_roles_url = (
            "https://api-account-os.hoyoverse.com/account/binding/api/"
            "getUserGameRolesByCookieToken"
        )

        response = session.get(
            user_roles_url,
            params={
                "lang": "en",
                "region": target_region,
                "game_biz": "hk4e_global",
                "sLangKey": "en-us",
            },
            timeout=2,
        ).json()

        data = response["data"]

        if not data:
            print(f"No data for region: {target_region}")
            continue

        user_game_roles_data = data["list"]

        for user_game_role in user_game_roles_data:
            game_uid = user_game_role["game_uid"]
            print(f"Fetching CD key status for user {game_uid} in region {target_region}")

            cd_key_status = get_cdkey_status(
                session,
                game_uid,
                cd_key,
                target_region,
                user_game_role["game_biz"],
            )

            if not cd_key_statuses:
                cd_key_statuses = {}

            if not target_region in cd_key_statuses:
                cd_key_statuses[target_region] = {}

            cd_key_statuses[target_region][game_uid] = cd_key_status

    print("CD key status retrieval completed.")
    return cd_key_statuses

token = ""
cd_key = "NS92PG6DB52M"

print(
    main(
        cd_key,
        token,
    )
)

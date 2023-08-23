import logging

from requests import Session


class Starling:
    def __init__(self, access_token: str, sandbox: bool = False) -> None:
        self.session = Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
        )
        self.base_url = "https://api.starlingbank.com/api/v2" if not sandbox else "https://api-sandbox.starlingbank.com/api/v2"


    def get_request(self, route: str, params=None) -> dict:
        response = self.session.get(
            url=f"{self.base_url}/{route}",
            params=params
        )
        
        if not response.ok:
            print(f"STATUS - {response.status_code}, ROUTE {route}")
            response_body = None
        else:
            response_body = response.json()
        
        return {
            "status": response.status_code,
            "body": response_body
        }
            


    def get_accounts(self) -> list[str]:
        response = self.get_request("accounts")
        if response is None:
            return []
        return [account["accountUid"] for account in response["accounts"]]

    def get_spaces(self, account_uid: str):
        return self.get_request(f"/account/{account_uid}/spaces")

    def get_balance(self, account_uid: str):
        return self.get_request(f"accounts/{account_uid}/balance") 
    

    def get_transactions(self, account_uid, start, end):
        route = f"feed/account/{account_uid}/settled-transactions-between"
        params = {
            "minTransactionTimestamp": start,
            "maxTransactionTimestamp": end
        }
        return self.get_request(route, params=params) 

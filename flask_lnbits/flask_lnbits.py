from datetime import datetime
from decimal import Decimal
import json
import requests
from typing import Any, Dict, Optional, Tuple
from flask import Flask


class LNbits:
    """A flask LNbits wrapper class.

    Attributes:
        app: The flask application.
        host: THe host URL.
        read_key: The read-only key.
        webhook: Webhook to execute on success.
        session: The request session connected to the host.
    """

    def __init__(self, app: Optional[Flask] = None):
        self.app = app
        self.host = ""
        self.read_key = ""
        self.webhook = ""
        self.session = requests.session()
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.host = app.config.get("LNBITS_HOST", "")
        self.read_key = app.config.get("LNBITS_READ_KEY", "")
        self.webhook = app.config.get("LNBITS_WEBHOOK", "")
        if ".onion" in self.host:
            self.session.proxies["http"] = "socks5h://0.0.0.0:9050"
            self.session.proxies["https"] = "socks5h://0.0.0.0:9050"

    @property
    def headers(self) -> Dict[str, str]:
        return {"X-Api-Key": self.read_key, "Content-type": "application/json"}

    @property
    def wallet_host(self) -> str:
        return f"{self.host}/api/v1"

    @property
    def lnurl_host(self) -> str:
        return f"{self.host}/lnurlp/api/v1"

    def get_wallet(self) -> Dict[str, str]:
        response = self.session.get(f"{self.wallet_host}/wallet", headers=self.headers)
        data = response.json()
        return data

    def create_invoice(
        self,
        amount: int,
        memo: str = "",
        unit: str = "sat",
    ) -> Dict[str, Any]:
        """Creates and returns an invoice.

        Args:
            amount: The amount for the invoice.
            memo: The memo for the invoice.
            unit: The unit for the invoice, sat.
        Returns:
            An invoice.
        """
        print(__name__, "create_invoice")
        data_out = {
            "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "amount": amount,
            "unit": unit,
            "payment_request": "",
            "payment_hash": "",
        }
        try:
            data_in = {
                "out": False,  # invoice is for incoming, not outgoing, payment.
                "amount": int(amount),
                "memo": memo,
                "unit": unit,
                "webhook": self.webhook,
                "internal": False,  # use the fake wallet if the invoice is for internal use only.e
            }
            response = self.session.post(
                f"{self.wallet_host}/payments",
                headers=self.headers,
                data=json.dumps(data_in),
            )
            data = response.json()
        except:
            pass
        else:
            data_out["payment_request"] = data["payment_request"]
            data_out["payment_hash"] = data["payment_hash"]
        return data_out

    def get_invoice(self, payment_hash: str) -> Dict[str, Any]:
        # curl -X GET https://legend.lnbits.com/api/v1/payments/<payment_hash> -H "X-Api-Key: " -H "Content-type: application/json"
        pass

    def get_lnurlp(self, pay_id: Optional[int] = None) -> Dict[str, Any]:
        """Gets and returns an LNURL pay link.

        Args:
            pay_id: Return a pay link with a given ID.
        Returns:
            A dictionary containing an LNURL pay link.
        """
        print(__name__, "get_lnurlp")
        data_out = {
            "pay_id": -1,
            "description": "description",
            "min_sats": "min_sats",
            "max_sats": "max_sats",
            "lnurl": "lnurl",
        }
        try:
            response = self.session.get(
                f"{self.lnurl_host}/links", headers=self.headers
            )
            data = response.json()
            if pay_id is None:  # take the first link if no ID is given.
                data = data[0]
            else:
                data = [d for d in data if d["id"] == pay_id][0]
        except:
            pass
        else:
            data_out["pay_id"] = int(data["id"])
            data_out["description"] = data["description"]
            data_out["min_sats"] = int(data["min"])
            data_out["max_sats"] = int(data["max"])
            data_out["lnurl"] = data["lnurl"]
        return data_out

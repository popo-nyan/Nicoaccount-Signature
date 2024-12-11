import hashlib
import hmac
import datetime
import httpx
from urllib.parse import urlparse

API_KEY = "A1jjnnqfvt7r5vdzhben"
API_SECRET_KEY = "n27s7v7ih654i2uqtehgipv2qfb2b8kb8jvgy9fv"


def signature_calculation(nico_account_date: str, http_method: str, uri: str) -> str:
    signature_1 = hashlib.sha256("".encode()).hexdigest()
    signature_2 = hashlib.sha256(
        (
            http_method.upper()
            + "\n"
            + urlparse(uri).path
            + "\n\nhost:"
            + urlparse(uri).netloc
            + "\nx-nicoaccount-date:"
            + nico_account_date
            + "\n\n"
            + signature_1
        ).encode()
    ).hexdigest()
    signature_3 = hmac.new(
        key=("nicoaccount1" + API_SECRET_KEY).encode(),
        msg=nico_account_date[:8].encode(),
        digestmod=hashlib.sha256,
    )
    signature_4 = hmac.new(
        key=signature_3.digest(),
        msg="nicoaccount1_request".encode(),
        digestmod=hashlib.sha256,
    )
    nico_account_signature = hmac.new(
        key=signature_4.digest(),
        msg=(
            "NICOACCOUNT1-HMAC-SHA256\n" + nico_account_date + "\n" + signature_2
        ).encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()
    return nico_account_signature


def main() -> None:
    nico_account_date = datetime.datetime.now(tz=datetime.timezone.utc).strftime(
        "%Y%m%dT%H%M%S+0000"
    )
    response = httpx.post(
        "https://account.nicovideo.jp/api/v1/register/account_passport",
        headers={
            "Host": "account.nicovideo.jp",
            "X-Frontend-Version": "8.9.0",
            "X-Nicoaccount-Date": nico_account_date,
            "X-Frontend-Id": "1",
            "X-Nicoaccount-Signature": signature_calculation(
                nico_account_date,
                "post",
                "https://account.nicovideo.jp/api/v1/register/account_passport",
            ),
            "User-Agent": "Niconico/1.0 (Linux; U; Android 14; ja-jp; nicoandroid Pixel 6a) Version/8.9.0",
            "X-Request-With": "nicoandroid",
            "Accept-Language": "ja-jp",
            "X-Nicoaccount-Api-Key": API_KEY,
            "Content-Type": "text/plain; charset=utf-8",
        },
    )
    print(response, response.json())
    user_id, user_session, account_passport = (
        response.json()["data"]["user_id"],
        response.json()["data"]["user_session"],
        response.json()["data"]["account_passport"],
    )
    print(user_id, user_session, account_passport)


if __name__ == "__main__":
    main()

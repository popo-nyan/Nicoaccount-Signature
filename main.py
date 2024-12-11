import hashlib
import hmac
import datetime
from urllib.parse import urlparse

API_KEY = "A1jjnnqfvt7r5vdzhben"
API_SECRET_KEY = "n27s7v7ih654i2uqtehgipv2qfb2b8kb8jvgy9fv"
NICO_ACCOUNT_DATE = datetime.datetime.now(tz=datetime.timezone.utc).strftime(
    "%Y%m%dT%H%M%S+0000"
)


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


if __name__ == "__main__":
    print(
        signature_calculation(
            NICO_ACCOUNT_DATE,
            "post",
            "https://account.nicovideo.jp/api/v1/register/account_passport",
        )
    )

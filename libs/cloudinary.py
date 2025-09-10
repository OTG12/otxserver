import hashlib
import time
import mimetypes
import http.client
import uuid
import orjson
from typing import Union, IO
from config.env import CLOUDNAME, CLOUDKEY, CLOUDSECRET


def sign(params: dict, secret: str) -> str:
    """Generate Cloudinary API signature (SHA1)."""
    sorted_params = sorted([(k, v) for k, v in params.items() if v is not None])
    query = "&".join(f"{k}={v}" for k, v in sorted_params)
    to_sign = f"{query}{secret}"
    return hashlib.sha1(to_sign.encode("utf-8")).hexdigest()


class MediaService:
    DOMAIN = "api.cloudinary.com"
    PATH = f"/v1_1/{CLOUDNAME}"

    @classmethod
    def upload(cls, file: Union[str, IO[bytes]], resource_type: str = "auto") -> str:
        """
        Upload file to Cloudinary using http.client and return secure_url.
        file: URL (str) or file-like object
        """
        timestamp = int(time.time())
        params = {"timestamp": timestamp}
        signature = sign(params, CLOUDSECRET)

        boundary = uuid.uuid4().hex
        CRLF = b"\r\n"

        # Build multipart body
        body = b""
        fields = {
            "timestamp": str(timestamp),
            "api_key": CLOUDKEY,
            "signature": signature,
        }

        # Add normal fields
        for key, value in fields.items():
            body += f"--{boundary}\r\n".encode()
            body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode()
            body += f"{value}\r\n".encode()

        # Add file field
        if isinstance(file, str):
            filename = file.split("/")[-1]
            mimetype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
            with open(file, "rb") as f:
                file_content = f.read()
        else:
            filename = getattr(file, "name", "upload.bin")
            mimetype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
            file_content = file.read()
            file.seek(0)

        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode()
        body += f"Content-Type: {mimetype}\r\n\r\n".encode()
        body += file_content + CRLF
        body += f"--{boundary}--\r\n".encode()

        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
        }

        conn = http.client.HTTPSConnection(cls.DOMAIN)
        conn.request(
            "POST",
            f"{cls.PATH}/{resource_type}/upload",
            body=body,
            headers=headers,
        )
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
        result = orjson.loads(data)
        return result.get("secure_url")

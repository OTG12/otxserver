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
        Upload file to Cloudinary and return the secure_url.
        - file: URL (str) or file-like object (IO[bytes])
        - resource_type: "image", "video", "raw", or "auto"
        """
        timestamp = int(time.time())
        params = {"timestamp": timestamp}
        signature = sign(params, CLOUDSECRET)

        boundary = uuid.uuid4().hex
        body_parts = []

        # Required fields
        fields = {
            "timestamp": str(timestamp),
            "api_key": CLOUDKEY,
            "signature": signature,
        }

        for key, value in fields.items():
            body_parts.append(f"--{boundary}\r\n")
            body_parts.append(f'Content-Disposition: form-data; name="{key}"\r\n\r\n')
            body_parts.append(f"{value}\r\n")

        # File field
        if isinstance(file, str):
            body_parts.append(f"--{boundary}\r\n")
            body_parts.append('Content-Disposition: form-data; name="file"\r\n\r\n')
            body_parts.append(f"{file}\r\n")
        else:
            filename = getattr(file, "name", "upload.bin")
            mimetype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
            file_content = file.read()

            body_parts.append(f"--{boundary}\r\n")
            body_parts.append(
                f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            )
            body_parts.append(f"Content-Type: {mimetype}\r\n\r\n")
            body_parts.append(file_content)
            body_parts.append("\r\n")

        body_parts.append(f"--{boundary}--\r\n")

        body = b"".join(
            part.encode("utf-8") if isinstance(part, str) else part
            for part in body_parts
        )

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

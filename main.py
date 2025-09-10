import io
from libs.cloudinary import MediaService  # adjust import path if needed

def test_upload_file_path():
    """
    Test uploading a local file by path.
    """
    try:
        file_path = "SUNDAY-DARE-2.jpg"  # replace with your local test file
        url = MediaService.upload(file_path)
        print("Upload by path successful! URL:", url)
    except Exception as e:
        print("Upload by path failed:", str(e))


def test_upload_file_like_object():
    """
    Test uploading a file-like object (e.g., BytesIO)
    """
    try:
        with open("SUNDAY-DARE-2.jpg", "rb") as f:
            file_like = io.BytesIO(f.read())
            file_like.name = "SUNDAY-DARE-2.jpg"  # required for upload
            url = MediaService.upload(file_like)
            print("Upload via file-like object successful! URL:", url)
    except Exception as e:
        print("Upload via file-like object failed:", str(e))


if __name__ == "__main__":
    print("Testing Cloudinary upload...")
    test_upload_file_path()
    test_upload_file_like_object()

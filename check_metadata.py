from PIL import Image
from PIL.ExifTags import TAGS

def get_exif(path):
    try:
        img = Image.open(path)
        exif = img._getexif()
        if not exif:
            return {}
        return {TAGS.get(key, key): val for key, val in exif.items()}
    except Exception as e:
        return {"error": str(e)}

files = ["Picture_UAS_Steganografi.jpg", "Picture_UAS_Steganografi_fixnodata.jpg"]

for f in files:
    print(f"Metadata for {f}:")
    exif = get_exif(f)
    for k, v in exif.items():
        print(f"  {k}: {v}")
    print("-" * 20)

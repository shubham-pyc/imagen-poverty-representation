import os
import getpass
import concurrent.futures
import pandas as pd
import dotenv
dotenv.load_dotenv()
# os.environ['GOOGLE_API_KEY'] = "AIzaSyB6C4BvUNSbkc75QMA6D-D28R6SZYZz4_o"


from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

client = genai.Client(
    api_key = os.environ['GOOGLE_API_KEY'],
)

# write me a function which would take an image as an input
# and ask ai if this image is of south asian origin or not
# if it is, return True, otherwise return False
def generate_single(image: Image.Image) -> bool:
    try:
        prompt = "Is this image of a south asian origin? Answer in yes or no. Do not give any other text."
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=[prompt, image],
        )
        return response.candidates[0].content.parts[0].text == "yes" or response.candidates[0].content.parts[0].text == "Yes"
    except Exception as e:
        print(e)
        return None

# read all the images in the images folder
# create a dataframe with the image path and the label
import concurrent.futures

processed_df = pd.read_csv("south_asian_images.csv")
already_processed = processed_df["image_path"].tolist()
pth = "raw/poor"

image_paths = [os.path.join(pth, name) for name in os.listdir(pth) if name not in already_processed]
# print(image_paths)
# image_paths = image_paths[:10]
# print(image_paths)

def classify(path: str) -> dict[str, str | bool]:
    img = Image.open(path)
    return {"image_path": os.path.basename(path), "label": generate_single(img)}

rows = []
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    for result in pool.map(classify, image_paths):
        rows.append(result)
df = pd.DataFrame(rows)
processed_df = pd.concat([processed_df, df])
processed_df.to_csv("south_asian_images_updated.csv", index=False)
# df.to_csv("south_asian_images.csv", index=False)
# if __name__ == "__main__":
#     image = Image.open("images/poor_family_100.jpg")
#     print(generate_single(image))
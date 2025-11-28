import os
import getpass
import concurrent.futures
import dotenv
dotenv.load_dotenv()
PROMPT = "Generate an image for a poor family"
IMAGE_PATH_PATTERN = "raw/poor/poor_family_{}.jpg"


from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

client = genai.Client(
    api_key = os.getenv('GOOGLE_API_KEY'),
)


# before after

import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt



def generate_single(index: int) -> None:
    try:
        prompt = PROMPT
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=[prompt],
        )
        image_parts = [
            part.inline_data.data
            for part in response.candidates[0].content.parts
            if part.inline_data
        ]
        if image_parts:
            image = Image.open(BytesIO(image_parts[0]))
            image.save(IMAGE_PATH_PATTERN.format(index))
    except Exception as e:
        print(e)

import time

start_time = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
    list(executor.map(generate_single, range(6000,6600)))
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")
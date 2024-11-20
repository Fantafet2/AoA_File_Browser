import os 
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


#setting the environment variables
try:
    endpoint = "https://imagesummary.cognitiveservices.azure.com/"
    key = "EtZDMQ3buqw0eRrWWtlWAMuuLcjeon71QAJLloAzaaYzFi1Wy7KTJQQJ99AKACYeBjFXJ3w3AAAFACOGBfO0"
except KeyError:
    print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
    print("Set them before running this sample.")
    exit()

# Create an ImageAnalysisClient
client = ImageAnalysisClient(
    endpoint = endpoint, 
    credential=AzureKeyCredential(key)
)

def get_visual_features(path,filename):
    image_path = os.path.join(path,filename)

    #getting the caption for the image
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()  # Read image as binary data

    result = client._analyze_from_image_data(
        image_data=image_data,
        visual_features=[VisualFeatures.CAPTION, VisualFeatures.READ],
        gender_neutral_caption=True,  # Optional
    )
    # Process the result
    if "captionResult" in result and result["captionResult"]:
        caption = result["captionResult"]["text"]
        return caption
    else:
        return "No caption found."


def main():
   get_visual_features()

if __name__ == "__main__":
    main()

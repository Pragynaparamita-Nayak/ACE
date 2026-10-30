from langsmith import traceable
from ddgs import DDGS


@traceable(name="Image Tool")
def search_image(query):
    try:
        with DDGS() as ddgs:
            results = list(
                ddgs.images(
                    query,
                    max_results=1
                )
            )

            if results:
                image_url = results[0].get("image")

                print("IMAGE URL =", image_url)

                return image_url

            return None

    except Exception as e:
        print("Image Search Error:", e)
        return None
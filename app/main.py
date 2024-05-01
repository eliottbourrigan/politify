from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from lyricsgenius import Genius
import replicate
import os

app = FastAPI()


@app.get("/analyze")
async def analyze(song_url: str):

    # Get the lyrics
    genius_token = os.environ.get("GENIUS_API_TOKEN")
    genius = Genius(genius_token)
    lyrics = genius.lyrics(song_url=song_url)

    # Create the prompt
    with open("utils/prompt.txt", "r") as file:
        prompt = file.read() + "\n\n"
    prompt += lyrics
    
    # Give the prompt to Llama3
    api_token = os.environ.get("REPLICATE_API_TOKEN")
    print(api_token)
    api = replicate.Client(api_token=api_token)
    input = {"prompt": prompt,
        "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",}
    output = "".join(api.run(
        "meta/meta-llama-3-70b-instruct",
        input=input
    ))

    # Parse the output
    if output.startswith("NoLyricsProvidedError"):
        return JSONResponse(content={"output": "NoLyricsProvidedError"})
    output = output.split("|")
    output = {"val_x": output[0], "lyr_x": output[1], "val_y": output[2], "lyr_y": output[3]}
    return JSONResponse(content=output)

@app.get("/search")
async def search(query):
    genius_token = os.environ.get("GENIUS_API_TOKEN")
    print(genius_token)
    genius = Genius(genius_token)
    songs = genius.search_songs(query)
    songs = [song['result'] for song in songs['hits']]
    songs = [{key: song[key] for key in ['artist_names', 'header_image_thumbnail_url', 'title', 'path', 'id', 'url']} for song in songs]    
    return JSONResponse(content={"songs": songs})
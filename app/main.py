from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from lyricsgenius import Genius
from pydantic import BaseModel
import replicate

app = FastAPI()


class LyricsInput(BaseModel):
    lyrics: str


@app.post("/analyze")
async def analyze(lyrics_input: LyricsInput):

    # Create the prompt
    with open("utils/prompt.txt", "r") as file:
        prompt = file.read() + "\n\n"
    prompt += lyrics_input.lyrics
    
    # Give the prompt to Llama3
    api = replicate.Client(api_token="XXX")
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

def search_song(query):
    genius = Genius("your_token_here")
    songs = genius.search_songs(query)
    return songs


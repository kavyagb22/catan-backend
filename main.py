from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from typing import Optional

from fastapi import Body

from board_setup import generate_complete_board

app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/board-setup")
async def board_setup(number_of_players: int = Body(..., embed=True)):
    return generate_complete_board(number_of_players)
    
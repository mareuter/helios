# Copyright 2023 Michael Reuter. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

__all__ = ["app"]

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict:
    return {"msg": "This is a web service, nothing to see here."}

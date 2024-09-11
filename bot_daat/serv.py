from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse


app = FastAPI()

def html_generator(path):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Check</title>
        </head>
    <body>
        <center><h1>-Check-</h1></center>
        <center><img src="Users/evgenii/Desktop/code/Develop/Dev/bot_raschet/bot_daat/images/img58131209.jpg" alt = "{path}"></center>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/{path}", response_class=FileResponse)
async def test(path):
    return FileResponse(f"/Users/evgenii/Desktop/code/Develop/Dev/bot_raschet/bot_daat/images/{path}.jpg")


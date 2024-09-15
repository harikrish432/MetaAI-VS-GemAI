import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.generativeai as genai
from meta_ai_api import MetaAI  # Import MetaAI

app = FastAPI()

# Configure Google Gemini AI
#GOOGLE_GEMINI_API_KEY = ""
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY", "")
GOOGLE_GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=GOOGLE_GEMINI_API_KEY"
if not GOOGLE_GEMINI_API_KEY:
    raise ValueError("Google Gemini API key not found. Please set the GOOGLE_GEMINI_API_KEY environment variable.")
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize MetaAI (assuming no API key is needed)
meta_ai = MetaAI()

class TopicRequest(BaseModel):
    topic: str

@app.get("/", response_class=HTMLResponse)
async def get_form():
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meta AI vs Gemini AI</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nexa:wght@400;700&family=Nexa+Condensed:wght@700&display=swap">
    <style>
        body {
            background-image: url('https://images.pexels.com/photos/7135019/pexels-photo-7135019.jpeg?cs=srgb&dl=pexels-codioful-7135019.jpg&fm=jpg');
            background-size: cover;
            background-position: center;
            margin: 0;
            font-family: 'Nexa', sans-serif;
            color: black;
            text-align: center;
        }
        h1 {
            margin-top: 50px;
            font-family: 'Nexa Condensed', sans-serif;
            font-size: 3em;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        .description {
            margin: 20px auto;
            font-size: 1.2em;
            font-weight: 400;
            max-width: 800px;
            line-height: 1.6;
            color: #f8f9fa;
            padding: 20px;
            background: rgba(0, 0, 0, 0.4);
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        form {
            display: inline-block;
            margin-top: 30px;
            padding: 20px;
            background: rgba(0, 0, 0, 0.6);
            border-radius: 10px;
        }
        label {
            display: block;
            margin-bottom: 10px;
            font-size: 1.2em;
            font-weight: 400;
        }
        input[type="text"] {
            padding: 10px;
            font-size: 1em;
            border-radius: 5px;
            border: 1px solid #ddd;
            width: 100%;
            max-width: 500px;
        }
        input[type="submit"] {
            padding: 10px 20px;
            font-size: 1em;
            border: none;
            border-radius: 5px;
            background-color: #007BFF;
            color: white;
            cursor: pointer;
            transition: background-color 0.3s;
            font-weight: 700;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <h1>Meta AI vs Gemini AI</h1>
    <div class="description">
        Welcome to our debate platform! This site allows you to initiate engaging discussions between Meta AI and Gemini AI. Submit your topics or prompts, and watch as Meta AI promtes questions to Gemini AI, and vice versa. Enjoy the dynamic exchange of ideas and gain insights from these advanced AI systems.
    </div>
    <form action="/ask/" method="get">
        <label for="message">Enter your Topic For debate:</label>
        <input type="text" id="message" name="message" size="50">
        <input type="submit" value="Submit">
    </form>
</body>
</html>

    

            

    """

@app.get("/ask/", response_class=HTMLResponse)
async def ask_ai(message: str):
    """
    This endpoint receives a message, sends it to both MetaAI and Google Gemini AI, and displays
    their responses side-by-side.
    """
    try:
        # Initial message from the user to Meta AI
        meta_response = meta_ai.prompt(message)
        meta_response_text = meta_response

        # Response from Meta AI is sent to Google Gemini AI
        gemini_response = gemini_model.generate_content(f"Respond to the following message: '{meta_response_text}'")
        gemini_response_text = gemini_response.text

        # Response from Google Gemini AI is sent back to Meta AI
        final_meta_response = meta_ai.prompt(gemini_response_text)
        final_meta_response_text = final_meta_response

        final_gemini_response = gemini_model.generate_content(f"Respond to the following message: '{final_meta_response_text}'")
        final_gemini_response_text = final_gemini_response.text

        return f"""
        <html>
            <body style="background-image: url('https://images.pexels.com/photos/7135019/pexels-photo-7135019.jpeg?cs=srgb&dl=pexels-codioful-7135019.jpg&fm=jpg'); background-size: cover; margin: 0; padding: 0; font-family: Arial, sans-serif;">
                
                <h1 style="text-align: center; padding: 20px 0; color: black;">Meta AI VS Gemini AI</h1>
                
                <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                    <form action="/ask/" method="get" style="background-color: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 10px;">
                        <label for="message" style="color: black;">Enter your message:</label><br><br>
                        <input type="text" id="message" name="message" size="50" value="{message}" style="padding: 10px; width: 100%;"><br><br>
                        <input type="submit" value="Submit" style="padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    </form>
                </div>
                
                <h2 style="text-align: center; color: black;">Conversation:</h2>
                
                <div style="display: flex; justify-content: space-between; margin: 20px; padding: 20px; background-color: rgba(0, 0, 0, 0.5); border-radius: 10px; gap: 20px;">
                    <div style="width: 45%; text-align: center; color: white;">
                        <h3><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Meta_Platforms_Inc._logo.svg/800px-Meta_Platforms_Inc._logo.svg.png" alt="Meta AI Image" style="max-width: 30%;"></h3>
                        <p style="text-align: left; margin: 0; line-height: 1.5; white-space: normal;">{meta_response_text}</p>
                    </div>
                    <div style="width: 45%; text-align: center; color: white;">
                        <h3><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/344px-Google_Gemini_logo.svg.png" alt="Google Gemini AI Image" style="max-width: 20%;"></h3>
                        <p style="text-align: left; margin: 0; line-height: 1.5; white-space: normal;">{gemini_response_text}</p>
                    </div>
                </div>
                
                <div style="text-align: center; padding: 20px; color: black;">
                    <h2><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Meta_Platforms_Inc._logo.svg/800px-Meta_Platforms_Inc._logo.svg.png" alt="Meta AI Image" style="max-width: 10%;"></h2>
                    <h3>Meta Final Response</h3>
                    <p style="margin: 0; line-height: 1.5; white-space: normal;">{final_meta_response_text}</p>
                </div>
                
                <div style="text-align: center; padding: 20px; color: black;">
                    <h2><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/344px-Google_Gemini_logo.svg.png" alt="Google Gemini AI Image" style="max-width: 10%;"></h2>
                    <h3>Gemini Final Response</h3>
                    <p style="margin: 0; line-height: 1.5; white-space: normal;">{final_gemini_response_text}</p>
                </div>
                
                <div style="text-align: center; padding: 20px;">
                    <button onclick="history.back()" style="padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">Go Back</button>
                </div>
                
            </body>
        </html>


        
        """
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

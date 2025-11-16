from fastapi import FastAPI, Request
from pydantic import BaseModel
from ai_generator import generate_response
from competitor_scrapper import analyze_competitors
from seo_analyser import seo_recommendations
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

#  Create the FastAPI app first
app = FastAPI()

#  static files and set up templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

#  homepage route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Pydantic model
class ClientRequest(BaseModel):
    industry: str
    style: str
    goals: str
    competitors: list

# AI endpoint
@app.post("/generate-portfolio-advice")
async def generate_portfolio_advice(data: ClientRequest):
    ai_text = generate_response(data.industry, data.style, data.goals)
    competitor_data = analyze_competitors(data.competitors)
    seo_data = seo_recommendations(data.industry)

    return {
        "copywriting": ai_text,
        "competitor_analysis": competitor_data,
        "seo_tips": seo_data,
        "design_guidelines": [
            "Use responsive design (CSS Grid/Flexbox)",
            "Optimize images for fast loading",
            "Implement accessibility (WCAG standards)"
        ]
    }

#  Run locally with: python app.py
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

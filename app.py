import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from ai_generator import generate_response
from competitor_scrapper import analyze_competitors
from seo_analyser import seo_recommendations

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

#Fast API
app = FastAPI()
#  static files and set up templates
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

#  homepage route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Pydantic model
class ClientRequest(BaseModel):
    industry: str
    style: str
    goals: str
    competitors: list[str]

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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)

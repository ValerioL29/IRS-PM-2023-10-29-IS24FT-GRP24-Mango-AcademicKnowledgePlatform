from fastapi import FastAPI
from mango_server.search.routes import search_router
from mango_server.paper.routes import paper_router
from mango_server.recommend.routes import recommend_router

app = FastAPI(
    title="Project 🥭Mango",
    description="A research paper knowledge platform.",
    version="2.0.0"
)
# Add the routers to the app
app.include_router(search_router)
app.include_router(paper_router)
app.include_router(recommend_router)


@app.get("/")
async def root():
    return {"message": "Greetings Mango!"}

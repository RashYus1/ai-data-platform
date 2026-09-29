from fastapi import FastAPI # pyright: ignore[reportMissingImports]

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "AI Data Pipeline & Annotation Platform API is running"
    }
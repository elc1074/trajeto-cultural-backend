# routers/acervo.py
from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/acervo", tags=["acervo"])

@router.get("/get_lista")
async def get_lista():
    url = ("https://tainacan.ufsm.br/acervo-artistico/wp-json/tainacan/v2/"
           "collection/2174/items?perpage=24&paged=1&fetch_only=title,description,thumbnail,document,author_name")

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url)
        if r.status_code == 404:
            raise HTTPException(404, "Coleção/itens não encontrados no Tainacan.")
        r.raise_for_status()
        data = r.json()

    if isinstance(data, list):
        items = data
    elif isinstance(data, dict) and "items" in data:
        items = data["items"]
    else:
        items = []

    def render(v):
        return v.get("rendered") if isinstance(v, dict) else v

    return [
        {
            "id": it.get("id"),
            "title": render(it.get("title")),
            "description": render(it.get("description")),
            "author_name": it.get("author_name"),
            "thumbnail": it.get("thumbnail"),
            "document": it.get("document"),
            "url": it.get("url"),
        }
        for it in items
    ]


@router.get("/get_obra/{item_id}")
async def get_obra(item_id: int):
    url = (
        f"https://tainacan.ufsm.br/acervo-artistico/wp-json/tainacan/v2/items/{item_id}"
        "?fetch_only=title,description,thumbnail,document,author_name,url"
    )

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url)
        if r.status_code == 404:
            raise HTTPException(404, f"Obra {item_id} não encontrada no Tainacan.")
        r.raise_for_status()
        data = r.json()

    def render(v):
        return v.get("rendered") if isinstance(v, dict) else v

    return {
        "id": data.get("id"),
        "title": render(data.get("title")),
        "description": render(data.get("description")),
        "author_name": data.get("author_name"),
        "thumbnail": data.get("thumbnail"),
        "document": data.get("document"),
        "url": data.get("url"),
    }
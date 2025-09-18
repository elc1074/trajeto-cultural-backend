# routers/acervo.py
from fastapi import APIRouter, HTTPException, Query
import httpx

router = APIRouter(prefix="/acervo", tags=["acervo"])

@router.get("/get_lista")
def get_lista(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200)
):
    url = "https://tainacan.ufsm.br/wp-json/tainacan/v2/collection/2174/items"
    response = requests.get(url, params={"perpage": per_page, "paged": page})
    data = response.json()

    obras = []
    for item in data:
        meta = item.get("metadata", {})
        georef = meta.get("georeferenciamento", {}).get("value_as_string", "")
        latitude, longitude = (None, None)
        if georef:
            try:
                latitude, longitude = georef.split(",")
            except Exception:
                pass

        obras.append({
            "id": item.get("id"),
            "title": item.get("title"),
            "author_name": item.get("author_name"),
            "thumbnail": item.get("thumbnail"),
            "url": item.get("url"),
            "latitude": latitude,
            "longitude": longitude,
        })

    return obras




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
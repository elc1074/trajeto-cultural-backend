import requests
from fastapi import APIRouter, HTTPException, Query
import httpx


router = APIRouter(prefix="/acervo", tags=["acervo"])

@router.get("/get_lista")
async def get_lista():
    base_url = (
        "https://tainacan.ufsm.br/acervo-artistico/wp-json/tainacan/v2/"
        "collection/2174/items?perpage=100"
    )

    items = []
    page = 1

    async with httpx.AsyncClient(timeout=30) as client:
        while True:
            url = f"{base_url}&paged={page}"
            r = await client.get(url)
            if r.status_code == 404:
                raise HTTPException(404, "Coleção/itens não encontrados no Tainacan.")
            r.raise_for_status()
            data = r.json()

            page_items = []
            if isinstance(data, list):
                page_items = data
            elif isinstance(data, dict) and "items" in data:
                page_items = data["items"]

            if not page_items:  # acabou as páginas
                break

            items.extend(page_items)
            page += 1

    def render(v):
        return v.get("rendered") if isinstance(v, dict) else v

    obras = []
    for it in items:
        # pega o campo georeferenciamento
        meta = it.get("metadata", {})
        coords = None
        if "georeferenciamento" in meta:
            field = meta["georeferenciamento"]
            if isinstance(field, dict):
                coords = field.get("value") or field.get("value_as_string")
            elif isinstance(field, str):
                coords = field

        latitude, longitude = None, None
        if coords and isinstance(coords, str) and "," in coords:
            parts = [p.strip() for p in coords.split(",")]
            if len(parts) == 2:
                latitude, longitude = parts

        obras.append({
            "id": it.get("id"),
            "title": render(it.get("title")),
            "description": render(it.get("description")),
            "author_name": it.get("author_name"),
            "thumbnail": it.get("thumbnail"),
            "document": it.get("document"),
            "url": it.get("url"),
            "latitude": latitude,
            "longitude": longitude,
        })

    return obras




@router.get("/get_obra/{item_id}")
async def get_obra(item_id: int):
    url = f"https://tainacan.ufsm.br/acervo-artistico/wp-json/tainacan/v2/items/{item_id}"

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url)
        if r.status_code == 404:
            raise HTTPException(404, f"Obra {item_id} não encontrada no Tainacan.")
        r.raise_for_status()
        data = r.json()

    def render(v):
        return v.get("rendered") if isinstance(v, dict) else v

    meta = data.get("metadata", {})
    coords = None
    if "georeferenciamento" in meta:
        field = meta["georeferenciamento"]
        if isinstance(field, dict):
            coords = field.get("value") or field.get("value_as_string")
        elif isinstance(field, str):
            coords = field

    latitude, longitude = None, None
    if coords and isinstance(coords, str) and "," in coords:
        parts = [p.strip() for p in coords.split(",")]
        if len(parts) == 2:
            latitude, longitude = parts

    return {
        "id": data.get("id"),
        "title": render(data.get("title")),
        "description": render(data.get("description")),
        "author_name": data.get("author_name"),
        "thumbnail": data.get("thumbnail"),
        "document": data.get("document"),
        "url": data.get("url"),
        "latitude": latitude,
        "longitude": longitude,
    }

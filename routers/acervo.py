import requests
from fastapi import APIRouter, HTTPException, Query
import httpx
import re
import asyncio


router = APIRouter(prefix="/acervo", tags=["acervo"])

@router.get("/get_lista")
async def get_lista(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200)
):
    base_url = (
        "https://tainacan.ufsm.br/acervo-artistico/wp-json/tainacan/v2/"
        "collection/2174/items"
    )

    async with httpx.AsyncClient(timeout=30) as client:
        url = f"{base_url}?perpage={per_page}&paged={page}"
        r = await client.get(url)
        if r.status_code == 404:
            raise HTTPException(404, "Coleção/itens não encontrados no Tainacan.")
        r.raise_for_status()
        data = r.json()

        items = []
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict) and "items" in data:
            items = data["items"]

    def render(v):
        return v.get("rendered") if isinstance(v, dict) else v

    obras = []
    for it in items:
        latitude, longitude = None, None
        meta = it.get("metadata", {})
        coords = None
        if "georeferenciamento" in meta:
            field = meta["georeferenciamento"]
            if isinstance(field, dict):
                coords = field.get("value") or field.get("value_as_string")
            elif isinstance(field, str):
                coords = field

        if coords and isinstance(coords, str) and "," in coords:
            parts = [p.strip() for p in coords.split(",")]
            if len(parts) == 2:
                latitude, longitude = parts

        obras.append({
            "id": it.get("id"),
            "title": render(it.get("title")),
            "latitude": latitude,
            "longitude": longitude,
        })

    return obras





@router.get("/get_obra/{item_id}")
async def get_obra(item_id: int):
    url_basic = (
        f"https://tainacan.ufsm.br/acervo-artistico/wp-json/tainacan/v2/items/{item_id}"
        "?fetch_only=title,description,thumbnail,document,author_name"
    )
    url_detail = f"https://tainacan.ufsm.br/acervo-artistico/wp-json/tainacan/v2/items/{item_id}"

    async with httpx.AsyncClient(timeout=30) as client:
        r_basic = await client.get(url_basic)
        if r_basic.status_code == 404:
            raise HTTPException(404, f"Obra {item_id} não encontrada no Tainacan.")
        r_basic.raise_for_status()
        data_basic = r_basic.json()

        r_detail = await client.get(url_detail)
        r_detail.raise_for_status()
        data_detail = r_detail.json()

    def render(v):
        return v.get("rendered") if isinstance(v, dict) else v

    latitude, longitude = None, None
    meta = data_detail.get("metadata", {})
    if "georeferenciamento" in meta:
        field = meta["georeferenciamento"]
        coords = None
        if isinstance(field, dict):
            coords = field.get("value") or field.get("value_as_string")
        elif isinstance(field, str):
            coords = field
        if coords and isinstance(coords, str) and "," in coords:
            parts = [p.strip() for p in coords.split(",")]
            if len(parts) == 2:
                latitude, longitude = parts

    thumb_url = None
    thumb = data_basic.get("thumbnail")
    if isinstance(thumb, dict):
        if "medium" in thumb and isinstance(thumb["medium"], list):
            thumb_url = thumb["medium"][0]
        elif "full" in thumb and isinstance(thumb["full"], list):
            thumb_url = thumb["full"][0]

    return {
        "id": data_basic.get("id"),
        "title": render(data_basic.get("title")),
        "description": render(data_basic.get("description")),
        "author_name": data_basic.get("author_name"),
        "thumbnail": thumb_url,
        "document": data_basic.get("document"),
        "url": data_basic.get("url"),
        "latitude": latitude,
        "longitude": longitude,
    }


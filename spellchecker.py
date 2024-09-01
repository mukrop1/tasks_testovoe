from typing import List
import httpx

YANDEX_SPELLER_API = "https://speller.yandex.net/services/spellservice.json/checkTexts"
# texts: Список текстов для проверки.
async def check_spelling(texts: List[str]) -> List[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.post(YANDEX_SPELLER_API, data={"text": texts})
        response.raise_for_status()
        return response.json() # список результатов проверки -> List[dict]

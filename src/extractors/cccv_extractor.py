import os
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Optional

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


MONTHS_PT_BR = {
    "janeiro": 1,
    "fevereiro": 2,
    "março": 3,
    "marco": 3,
    "abril": 4,
    "maio": 5,
    "junho": 6,
    "julho": 7,
    "agosto": 8,
    "setembro": 9,
    "outubro": 10,
    "novembro": 11,
    "dezembro": 12,
}


COFFEE_TYPES = {
    "arabica_dura": "Arábica bebida dura",
    "arabica_rio": "Arábica bebida rio",
    "conilon": "Conilon",
}


def get_cccv_url() -> str:
    """
    Retorna a URL da página de cotação da CCCV.

    Primeiro tenta ler do arquivo .env.
    Se não encontrar, usa a URL padrão.
    """
    return os.getenv("CCCV_COTACAO_URL", "https://www.cccv.org.br/cotacao/")


def fetch_html(url: str) -> str:
    """
    Baixa o HTML da página informada.

    Alguns sites recusam requisições sem headers de navegador.
    Por isso enviamos User-Agent e Accept headers.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text


def parse_brazilian_decimal(value: str) -> Optional[Decimal]:
    """
    Converte valores no formato brasileiro para Decimal.

    Exemplos:
    "1.013,00" -> Decimal("1013.00")
    "984,00"   -> Decimal("984.00")
    "---"      -> None
    ""         -> None
    """
    if value is None:
        return None

    cleaned_value = value.strip()

    if not cleaned_value or cleaned_value == "---":
        return None

    cleaned_value = cleaned_value.replace(".", "").replace(",", ".")

    try:
        return Decimal(cleaned_value)
    except InvalidOperation:
        return None


def extract_reference_month_year(text: str) -> tuple[int, int]:
    """
    Extrai mês e ano do texto da página.

    Exemplo esperado:
    'Cotação do café referente ao mês de Março de 2026'

    Retorno:
    (3, 2026)
    """
    normalized_text = text.lower()

    pattern = r"m[eê]s de ([a-zçã]+) de (\d{4})"
    match = re.search(pattern, normalized_text)

    if not match:
        raise ValueError("Não foi possível identificar mês e ano da cotação.")

    month_name = match.group(1)
    year = int(match.group(2))

    month = MONTHS_PT_BR.get(month_name)

    if not month:
        raise ValueError(f"Mês não reconhecido: {month_name}")

    return month, year


def extract_page_text(html: str) -> str:
    """
    Extrai o texto limpo do HTML.
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n", strip=True)


def parse_cccv_current_prices(html: str, source_url: str) -> list[dict]:
    """
    Faz o parse da página atual da CCCV.

    A página pode apresentar os dados em linhas completas ou com quebras
    entre dia e preços. Por isso usamos regex no texto completo.
    """
    page_text = extract_page_text(html)
    reference_month, reference_year = extract_reference_month_year(page_text)

    extracted_at = datetime.utcnow().isoformat()
    records = []

    price_pattern = re.compile(
        r"(?<!\d)"
        r"(\d{1,2})\s+"
        r"(\d{1,3}(?:\.\d{3})*,\d{2})\s+"
        r"(\d{1,3}(?:\.\d{3})*,\d{2})\s+"
        r"(\d{1,3}(?:\.\d{3})*,\d{2})"
    )

    for match in price_pattern.finditer(page_text):
        day = int(match.group(1))

        if day < 1 or day > 31:
            continue

        arabica_dura_price = parse_brazilian_decimal(match.group(2))
        arabica_rio_price = parse_brazilian_decimal(match.group(3))
        conilon_price = parse_brazilian_decimal(match.group(4))

        price_date = datetime(reference_year, reference_month, day).date().isoformat()

        prices_by_type = {
            "arabica_dura": arabica_dura_price,
            "arabica_rio": arabica_rio_price,
            "conilon": conilon_price,
        }

        for coffee_type, price in prices_by_type.items():
            if price is None:
                continue

            records.append(
                {
                    "price_date": price_date,
                    "coffee_type": coffee_type,
                    "coffee_description": COFFEE_TYPES[coffee_type],
                    "price_brl": price,
                    "source_url": source_url,
                    "extracted_at": extracted_at,
                }
            )

    return records


def extract_current_cccv_prices() -> list[dict]:
    """
    Função principal do extractor.

    Busca a página da CCCV e retorna os registros estruturados.
    """
    url = get_cccv_url()
    html = fetch_html(url)
    return parse_cccv_current_prices(html, source_url=url)


if __name__ == "__main__":
    prices = extract_current_cccv_prices()

    print(f"Total de registros extraídos: {len(prices)}")

    for price in prices[:10]:
        print(price)

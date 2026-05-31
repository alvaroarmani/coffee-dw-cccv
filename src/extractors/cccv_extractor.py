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


COFFEE_PRICE_COLUMNS = [
    {
        "coffee_type": "arabica_dura",
        "coffee_description": 'Arábica bebida "dura", bica corrida',
        "harvest_year": "2025/2026",
        "position": 1,
    },
    {
        "coffee_type": "arabica_rio",
        "coffee_description": 'Arábica bebida "rio", bica corrida',
        "harvest_year": "2025/2026",
        "position": 2,
    },
    {
        "coffee_type": "arabica_dura",
        "coffee_description": 'Arábica bebida "dura", bica corrida',
        "harvest_year": "2026/2027",
        "position": 3,
    },
    {
        "coffee_type": "arabica_rio",
        "coffee_description": 'Arábica bebida "rio", bica corrida',
        "harvest_year": "2026/2027",
        "position": 4,
    },
    {
        "coffee_type": "conilon",
        "coffee_description": "Conilon bica corrida, tipo 7/8",
        "harvest_year": "2025/2026",
        "position": 5,
    },
    {
        "coffee_type": "conilon",
        "coffee_description": "Conilon bica corrida, tipo 7/8",
        "harvest_year": "2026/2027",
        "position": 6,
    },
]


def get_cccv_url() -> str:
    """
    Retorna a URL da página de cotação da CCCV.
    """
    return os.getenv("CCCV_COTACAO_URL", "https://www.cccv.org.br/cotacao/")


def fetch_html(url: str) -> str:
    """
    Baixa o HTML da página informada.

    Alguns sites recusam requisições sem headers de navegador.
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
    "-"        -> None
    "---"      -> None
    ""         -> None
    """
    if value is None:
        return None

    cleaned_value = value.strip()

    if not cleaned_value or cleaned_value in {"-", "---"}:
        return None

    cleaned_value = cleaned_value.replace(".", "").replace(",", ".")

    try:
        return Decimal(cleaned_value)
    except InvalidOperation:
        return None


def extract_reference_month_year(text: str) -> tuple[int, int]:
    """
    Extrai mês e ano do texto da página.

    Exemplo:
    'Cotação do café referente ao mês de Maio de 2026'
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

    A ordem das colunas de preço na página é:

    1. Arábica bebida dura - safra 2025/2026
    2. Arábica bebida rio  - safra 2025/2026
    3. Arábica bebida dura - safra 2026/2027
    4. Arábica bebida rio  - safra 2026/2027
    5. Conilon             - safra 2025/2026
    6. Conilon             - safra 2026/2027

    Valores "-", "–", "—", "−" e vazios são ignorados.
    """
    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(separator="\n", strip=True)

    reference_month, reference_year = extract_reference_month_year(page_text)
    extracted_at = datetime.utcnow().isoformat()

    records = []

    def normalize_cell(value: str) -> str:
        return (
            value.replace("\xa0", " ")
            .replace("–", "-")
            .replace("—", "-")
            .replace("−", "-")
            .strip()
        )

    def add_record(
        day: int,
        raw_values: list[str],
    ) -> None:
        if day < 1 or day > 31:
            return

        price_date = datetime(reference_year, reference_month, day).date().isoformat()

        normalized_values = [normalize_cell(value) for value in raw_values[:6]]

        while len(normalized_values) < 6:
            normalized_values.append("-")

        prices = [parse_brazilian_decimal(value) for value in normalized_values]

        for coffee_metadata, price in zip(COFFEE_PRICE_COLUMNS, prices):
            if price is None:
                continue

            records.append(
                {
                    "price_date": price_date,
                    "coffee_type": coffee_metadata["coffee_type"],
                    "coffee_description": coffee_metadata["coffee_description"],
                    "harvest_year": coffee_metadata["harvest_year"],
                    "price_brl": price,
                    "source_url": source_url,
                    "extracted_at": extracted_at,
                }
            )

    # Estratégia principal: ler linhas da tabela HTML
    for row in soup.find_all("tr"):
        cells = [
            normalize_cell(cell.get_text(separator=" ", strip=True))
            for cell in row.find_all(["td", "th"])
        ]

        if not cells:
            continue

        first_cell = cells[0]

        if not re.fullmatch(r"\d{1,2}", first_cell):
            continue

        day = int(first_cell)
        raw_values = cells[1:7]

        add_record(day=day, raw_values=raw_values)

    if records:
        return records

    # Fallback: caso a página venha sem tabela clara, tenta ler por tokens
    normalized_text = (
        page_text.replace("\xa0", " ")
        .replace("–", "-")
        .replace("—", "-")
        .replace("−", "-")
    )

    token_pattern = r"\d{1,3}(?:\.\d{3})*,\d{2}|-|\d{1,2}"
    tokens = re.findall(token_pattern, normalized_text)

    value_pattern = re.compile(r"^(?:\d{1,3}(?:\.\d{3})*,\d{2}|-)$")

    index = 0

    while index <= len(tokens) - 7:
        possible_day = tokens[index]

        if not re.fullmatch(r"\d{1,2}", possible_day):
            index += 1
            continue

        next_values = tokens[index + 1 : index + 7]

        if all(value_pattern.fullmatch(value) for value in next_values):
            add_record(day=int(possible_day), raw_values=next_values)
            index += 7
            continue

        index += 1

    return records


def extract_current_cccv_prices() -> list[dict]:
    """
    Função principal do extractor.
    """
    url = get_cccv_url()
    html = fetch_html(url)
    return parse_cccv_current_prices(html, source_url=url)


if __name__ == "__main__":
    prices = extract_current_cccv_prices()

    print(f"Total de registros extraídos: {len(prices)}")

    for price in prices[:10]:
        print(price)

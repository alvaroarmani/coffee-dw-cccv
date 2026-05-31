from src.extractors.cccv_extractor import extract_current_cccv_prices
from src.loaders.postgres_loader import load_raw_cccv_daily_prices


def main() -> None:
    print("Iniciando pipeline CCCV...")

    records = extract_current_cccv_prices()
    print(f"Registros extraídos: {len(records)}")

    loaded_rows = load_raw_cccv_daily_prices(records)
    print(f"Registros carregados/atualizados: {loaded_rows}")

    print("Pipeline finalizado com sucesso.")


if __name__ == "__main__":
    main()

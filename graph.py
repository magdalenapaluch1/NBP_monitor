from API_details import get_currencies_from_period, get_gold_from_period

def create_graph_currencies():

    start_date = input("Podaj datę startu(RRRR-MM-DD): ")
    end_date = input("Podaj datę zakończenia(RRRR-MM-DD): ")
    code = input("Podaj 3-literowy kod waluty: ")

    result = get_currencies_from_period(code, start_date, end_date)

    graph_date = list(result.keys())
    graph_rates = list(result.values())

    return graph_date, graph_rates


def create_graph_gold():

    start_date = input("Podaj datę startu(RRRR-MM-DD): ")
    end_date = input("Podaj datę zakończenia(RRRR-MM-DD): ")

    result = get_gold_from_period(start_date, end_date)

    graph_date = list(result.keys())
    graph_rates = list(result.values())

    return graph_date, graph_rates

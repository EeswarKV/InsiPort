from src.utils.stock_details import get_stock_details_cap


def get_stock_details(stock_info):
    stock_symbol = stock_info.get('symbol')
    customers_info = []
    _, _, current_price, _ = get_stock_details_cap(stock_symbol + '.NS')
    total_invested = float(stock_info.get('entry_price')) * float(stock_info.get('quantity'))
    current_total = float(current_price) * float(stock_info.get('quantity'))
    customer_dict = {
        'symbol': stock_info.get('symbol'),
        'exchange': stock_info.get('exchange'),
        'price': stock_info.get('entry_price'),
        'quantity': stock_info.get('quantity'),
        'entryDate': stock_info.get('entry_date'),
        'totalInvested': total_invested,
        'currentTotal': current_total
    }
    customers_info.append(customer_dict)


    print(customers_info)
    return customers_info

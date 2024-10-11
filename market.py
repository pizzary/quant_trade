import traceback

from tigeropen.common.consts import Language, Market, TimelinePeriod, QuoteRight
from tigeropen.common.response import TigerResponse
from tigeropen.quote.quote_client import QuoteClient
from tigeropen.quote.request import OpenApiRequest
from tigeropen.tiger_open_client import TigerOpenClient
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.common.util.signature_utils import read_private_key
from tigeropen.common.consts.service_types import ACCOUNTS
from tigeropen.trade.request.model import AccountsParams
from tigeropen.trade.trade_client import TradeClient


def get_client_config():
    """
    :return:
    """
    is_sandbox = False
    client_config = TigerOpenClientConfig(sandbox_debug=is_sandbox)
    client_config.private_key = read_private_key('your private key file path')
    client_config.tiger_id = 'your tiger id'
    client_config.account = 'your account'
    client_config.language = Language.en_US
    return client_config


def get_account_info():
    client_config = get_client_config()
    openapi_client = TigerOpenClient(client_config)
    account = AccountsParams()
    account.account = 'DU575569'
    request = OpenApiRequest(method=ACCOUNTS, biz_model=account)

    response_content = None
    try:
        response_content = openapi_client.execute(request)
    except Exception as e:
        print(traceback.format_exc())
    if not response_content:
        print("failed to execute")
    else:
        response = TigerResponse()
        response.parse_response_content(response_content)
        if response.is_success():
            print("get response data:" + response.data)
        else:
            print(response.code + "," + response.msg + "," + response.data)


def get_trade_apis():
    client_config = get_client_config()
    trade_client = TradeClient(client_config)
    trade_client.get_managed_accounts()


def get_quote_apis():
    client_config = get_client_config()
    quote_client = QuoteClient(client_config)
    quote_client.get_market_status(Market.US)
    quote_client.get_briefs(symbols=['AAPL', '00700', '600519'], include_ask_bid=True, right=QuoteRight.BR)
    quote_client.get_timeline(['AAPL'], period=TimelinePeriod.DAY, include_hour_trading=True)
    quote_client.get_bars(['AAPL'])


def get_option_quote():
    client_config = get_client_config()
    quote_client = QuoteClient(client_config)
    symbol = 'AAPL'
    expirations = quote_client.get_option_expirations(symbols=[symbol])
    if len(expirations) > 1:
        expiry = int(expirations[expirations['symbol'] == symbol].at[0, 'timestamp'])
        quote_client.get_option_chain(symbol, expiry)

    quote_client.get_option_briefs(['AAPL  190104C00121000'])
    quote_client.get_option_bars(['AAPL  190104P00134000'])
    quote_client.get_option_trade_ticks(['AAPL  190104P00134000'])


def get_future_quote():
    client_config = get_client_config()
    quote_client = QuoteClient(client_config)
    exchanges = quote_client.get_future_exchanges()
    print(exchanges)
    quote_client.get_future_bars(['CN1901'], begin_time=-1, end_time=1545105097358)
    quote_client.get_future_trade_ticks(['CN1901'])
    quote_client.get_future_contracts('CME')
    quote_client.get_future_trading_times('CN1901', trading_date=1545049282852)
    quote_client.get_future_brief(['ES1906', 'CN1901'])

# 자동매매종목 = Rise종목만 진행 



# STEP04: 자동매매를 위한 종목선정
market_values = [entry['market'] for entry in ticker_info]
print("\nSTEP03: 최종선정된 자동매매 종목들")
print(market_values)
#=======================================
def analyze_market_change(ticker_info):
    rise_tickers = []
    even_tickers = []
    fall_tickers = []
    for entry in ticker_info:
        if 'change' in entry:
            market_code = entry['market']
            change_value = entry['change']

            if change_value == 'RISE':
                rise_tickers.append(market_code)
            elif change_value == 'EVEN':
                even_tickers.append(market_code)
            elif change_value == 'FALL':
                fall_tickers.append(market_code)
    return rise_tickers, even_tickers, fall_tickers

rise_tickers, even_tickers, fall_tickers = analyze_market_change(ticker_info)
print("\nSTEP05: 상승종목, 보합종목, 하락종목 분류 결과")
print("\n상승종목:")
print(rise_tickers)
print("\n보합종목:")
print(even_tickers)
print("\n하락종목:")
print(fall_tickers)
#====================================
# STEP06: 상승보합하락 기준으로 종목선정
def print_analysis_results(rise_tickers, even_tickers, fall_tickers):
    num_rise_tickers = len(rise_tickers)
    num_even_tickers = len(even_tickers)
    num_fall_tickers = len(fall_tickers)
    total_coins = num_rise_tickers + num_even_tickers + num_fall_tickers
    if total_coins == 0:
        print("No coins found for analysis.")
        return
    rise_percentage = (num_rise_tickers / total_coins) * 100
    even_percentage = (num_even_tickers / total_coins) * 100
    fall_percentage = (num_fall_tickers / total_coins) * 100

    print("\nSTEP06: 상승, 보합, 하락 종목 비율 계산 결과")
    print(f"상승종목 비율: {rise_percentage:.2f}%")
    print(f"보합종목 비율: {even_percentage:.2f}%")
    print(f"하락종목 비율: {fall_percentage:.2f}%")

print_analysis_results(rise_tickers, even_tickers, fall_tickers)
#=========================================================
#STEP07 거래량, 거래대금 분석 
#=======================================
from datetime import datetime, timezone
# 함수 추가: timestamp를 UTC로 변환하는 함수
def convert_timestamp_to_utc(timestamp):
    return datetime.fromtimestamp(timestamp / 1000.0, timezone.utc)
#========================
trade_volume_ranking = []
for entry in sorted(ticker_info, key=lambda x: x.get('trade_volume', 0), reverse=True):
    if 'trade_volume' in entry:
        market_code = entry['market']
        timestamp_utc = convert_timestamp_to_utc(entry['timestamp'])
        trade_volume_info = f"{market_code} : {entry['trade_volume']} , timestamp:{timestamp_utc.strftime('%Y-%m-%d %H:%M:%S')}"
        trade_volume_ranking.append(trade_volume_info)
# trade_volume를 기준으로 코인을 내림차순으로 정렬하여 저장된 코인 출력
print("\nSTEP07_1: trade_volume 기준 => 가장 최근 거래량으로 종목분석")  
print(trade_volume_ranking)
#===============================
# STEP07_2: acc_trade_volume_24h 
# acc_trade_volume_24h 값이 높은 순서대로 [ ]에 저장한다.
acc_trade_volume_24h_ranking = []
for entry in sorted(ticker_info, key=lambda x: x.get('acc_trade_volume_24h', 0), reverse=True):
    if 'acc_trade_volume_24h' in entry:
        market_code = entry['market']
        timestamp_utc = convert_timestamp_to_utc(entry['timestamp'])
        acc_trade_volume_24h_info = f"{market_code} : {entry['acc_trade_volume_24h']} , timestamp:{timestamp_utc.strftime('%Y-%m-%d %H:%M:%S')}"
        acc_trade_volume_24h_ranking.append(acc_trade_volume_24h_info)

# acc_trade_volume_24h를 기준으로 코인을 내림차순으로 정렬하여 저장된 코인 출력
print("\nSTEP07_2: acc_trade_volume_24h=> 24시간 누적 거래대금기준으로 종목분석")  
print(acc_trade_volume_24h_ranking)
#===========================================
# STEP07_3: acc_trade_volume 
# acc_trade_volume 값이 높은 순서대로 [ ]에 저장한다.
# 저장양식은 [ KRW-BTC : acc_trade_volume , timestamp:1524047026072 ]
acc_trade_volume_ranking = []
for entry in sorted(ticker_info, key=lambda x: x.get('acc_trade_volume', 0), reverse=True):
    if 'acc_trade_volume' in entry:
        market_code = entry['market']
        timestamp_utc = convert_timestamp_to_utc(entry['timestamp'])
        acc_trade_volume_info = f"{market_code} : {entry['acc_trade_volume']} , timestamp:{timestamp_utc.strftime('%Y-%m-%d %H:%M:%S')}"
        acc_trade_volume_ranking.append(acc_trade_volume_info)
print("\nSTEP07_3: acc_trade_volume=> 누적 거래량(UTC 0시 기준)기준으로 종목분석")  
print(acc_trade_volume_ranking)
#===========================================
# STEP07_4: acc_trade_price 
# acc_trade_price 값이 높은 순서대로 [ ]에 저장한다.
# 저장양식은 [ KRW-BTC : acc_trade_price , timestamp:1524047026072 ]
acc_trade_price_ranking = []
for entry in sorted(ticker_info, key=lambda x: x.get('acc_trade_price', 0), reverse=True):
    if 'acc_trade_price' in entry:
        market_code = entry['market']
        timestamp_utc = convert_timestamp_to_utc(entry['timestamp'])
        acc_trade_price_info = f"{market_code} : {entry['acc_trade_price']} , timestamp:{timestamp_utc.strftime('%Y-%m-%d %H:%M:%S')}"
        acc_trade_price_ranking.append(acc_trade_price_info)

# acc_trade_price를 기준으로 코인을 내림차순으로 정렬하여 저장된 코인 출력
print("\nSTEP07_4: acc_trade_price=> 누적 거래대금(UTC 0시 기준) 기준으로 종목분석")  
print(acc_trade_price_ranking)
#===========================================
acc_trade_price_24h_ranking = []
for entry in sorted(ticker_info, key=lambda x: x.get('acc_trade_price_24h', 0), reverse=True):
    if 'acc_trade_price_24h' in entry:
        market_code = entry['market']
        timestamp_utc = convert_timestamp_to_utc(entry['timestamp'])
        acc_trade_price_24h_info = f"{market_code} : {entry['acc_trade_price_24h']} , timestamp:{timestamp_utc.strftime('%Y-%m-%d %H:%M:%S')}"
        acc_trade_price_24h_ranking.append(acc_trade_price_24h_info)
print("\nSTEP07_5: acc_trade_price_24h=> 24시간 누적 거래대금 기준으로 종목분석")  
print(acc_trade_price_24h_ranking)

def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                print(f"STEP14a: {ticker}    => Balance: {float(b['balance'])}")
                return float(b['balance'])
            else:
                print(f"STEP14b: {ticker}: => Balance: 0")
                return 0
    print(f"STEP14c: {ticker}:   => 보유잔고 = 0")
    return 0



def calculate_profit(ticker):
    avg_buy_price = upbit.get_avg_buy_price(ticker) # 보유 중인 암호화폐의 평균 매수가격 계산
    current_price = get_current_price(ticker) # 현재 가격 조회
    # 현재 수익률 계산
    if avg_buy_price == 0:  # 매수한 내역이 없을 경우
        return 0
    else:
        profit_percentage = ((current_price - avg_buy_price) / avg_buy_price) * 100
        return profit_percentage


# def visualize_backtest_results(df_results, ticker):
#     plt.plot(df_results['k'], df_results['total_profit'], marker='o')
#     last_profit_value = df_results['total_profit'].iloc[-1]
#     plt.text(plt.xlim()[1], last_profit_value, ticker, fontsize=8, ha='left', va='bottom')  # 오른쪽 끝에 텍스트 추가
#     plt.title('Total Profit vs. k')
#     plt.xlabel('k')
#     plt.ylabel('Total Profit')
#     plt.pause(0.1)

def backtest_strategy(ticker, k_values):
    results = []

    for k in k_values:
        total_profit = 0
        historical_data = pyupbit.get_ohlcv(ticker, interval="day", count=100)

        for i in range(1, len(historical_data)):
            previous_close = historical_data.iloc[i - 1]['close']
            price_range = historical_data.iloc[i - 1]['high'] - historical_data.iloc[i - 1]['low']
            target_price = previous_close + price_range * k

            if historical_data.iloc[i]['close'] > target_price:
                total_profit += (historical_data.iloc[i]['open'] / previous_close - 1)

        results.append({'k': k, 'total_profit': total_profit})
        #print(f"BackTest02: {ticker} => k={k:.1f}: total_profit = {total_profit:.6f}")

    df_results = pd.DataFrame(results)
    optimal_k = df_results.loc[df_results['total_profit'].idxmax()]['k']
    print(f"STEP03: {ticker} => BacKTest Optimal k: {optimal_k:.1f}")

    # visualize_backtest_results(df_results, ticker)

    return optimal_k

def find_optimal_k(ticker):
    k_candidates = np.arange(0.1, 2.1, 0.1)
    optimal_k_value = backtest_strategy(ticker, k_candidates)
    return optimal_k_value

upbit = pyupbit.Upbit(access, secret)
print("\nAutotrade start")

market_values = [entry['market'] for entry in ticker_info]
tickers = market_values

while True:
    try:
        now = datetime.datetime.now()
        print(f"\nAutotrade start => Current Time: {now}")
        market_values = [entry['market'] for entry in ticker_info]
        tickers = market_values
        print(f"\nAutotrade 종목")
        print(f"{tickers}")

        for ticker in tickers:
            start_time = get_start_time(ticker)
            end_time = start_time + datetime.timedelta(days=1)
            print(f"STEP02: {ticker} => AutoTrade Start Time: {start_time} ~ End Time: {end_time}")

            if start_time < now < end_time - datetime.timedelta(seconds=10):
                optimal_k = find_optimal_k(ticker)
                target_price = get_target_price(ticker, optimal_k)
                ma5 = get_ma5(ticker)
                ma15 = get_ma15(ticker)
                ema5 = get_ema5(ticker)
                ema15 = get_ema15(ticker)
                ema20 = get_ema20(ticker)
                ema50 = get_ema50(ticker)
                ema90 = get_ema90(ticker)
                ema120 = get_ema120(ticker)
                ema200 = get_ema200(ticker)
                current_price = get_current_price(ticker)
                balance = get_balance(ticker.split('-')[-1]) #보유잔고확인
                print(f"STEP15: {ticker} => AutoTrade Target Price: {target_price:,.0f}, current_price: {current_price:,.0f}")
                print(f"STEP15: {ticker} => AutoTrade MA05:{ma5:,.0f}, MA15:{ma15:,.0f}")
                print(f"STEP15: {ticker} => AutoTrade EMA05:{ema5:,.0f}, EMA15:{ema15:,.0f}, EMA20:{ema20:,.0f}, EMA50:{ema50:,.0f}, EMA120:{ema120:,.0f}, EMA200:{ema200:,.0f}")
                
                profit_percentage = calculate_profit(ticker)
                print(f"STEP16: {ticker} => 현재 수익률: {profit_percentage:.2f}%")
                
                # 현재 보유 중인 경우 매수를 수행하지 않음
                if balance > 0:
                    evaluation_amount = balance * current_price
                    print(f"STEP17: {ticker} => 평가금액: {evaluation_amount:,.0f} 원 = 현재가격 {current_price:,.0f} 원 * 보유량 {balance:.10f}")

                    # 추가된 부분: 수익률이 -2% 이하이면서 평가금액이 5500 KRW 이상인 경우 전량 매도
                    if profit_percentage <= -2 and evaluation_amount >= 5500:
                        sell_amount = balance * 0.9995
                        upbit.sell_market_order(ticker, sell_amount)
                        print(f"STEP18: {ticker} => 평가금액: {evaluation_amount:,.0f} > 5500원, 수익률: {profit_percentage:.2f} < -2.0% 이므로 전량 매도 수행")
                    continue
                
                if target_price < current_price and ema15 < current_price:
                    evaluation_amount = balance * current_price
                    krw = get_balance("KRW")
                    print(f"STEP19: {ticker} => AutoTrade 매수실행 {krw:,.0f} KRW")
                    print(f"STEP19: {ticker} => AutoTrade 매수실행 {target_price} < {current_price} 이고 {ema15} < {current_price}")
                    if evaluation_amount < 50000: # 보유종목에 대해서 추가매수를 금지하기위해서 만듬
                        print(f"STEP20: {ticker} => AutoTrade 매수실행 {krw:,.0f} KRW")
                        buy_amount = krw * 0.2
                        if krw > 20000:  # 조건 추가
                            upbit.buy_market_order(ticker, buy_amount)
                            print(f"STEP21: {ticker} => AutoTrade 매수완료 {buy_amount} = {krw} * 0.2")
                    else:
                        print(f"STEP23: {ticker} => 평가금액: {evaluation_amount} > 50,000원 이상이므로 추가매수를 안합니다!")
                
                elif (target_price > current_price and ema5 > current_price and ema15 > current_price) or profit_percentage <= -2:
                    sell_amount = balance * 0.9995
                    upbit.sell_market_order(ticker, sell_amount)
                    if target_price > current_price and ema5 > current_price and ema15 > current_price:
                        print(f"STEP24: {ticker} => 매도종목: {target_price:,.0f} > {current_price:,.0f} 이고 ema5: {ema5:,.0f} > ema15: {ema15:,.0f} > {current_price:,.0f} ")
                    elif profit_percentage <= -2:
                        print(f"STEP24: {ticker} => 매도종목: {profit_percentage:,.0f} <= -2.0% ")
                        
                # Golden Cross and Death Cross Signals
                elif (current_price > ema15 and current_price > ema20 and current_price > ema50 and current_price > ema200):  # 정배열
                    # Golden Cross: Buy Signal
                    krw_balance = get_balance("KRW")
                    print(f"STEP25: {ticker} => Golden Cross Buy Signal: {krw_balance:,.0f} KRW")                

                    # 매수 조건 추가 (예: KRW 잔고가 20000 이상일 때에만 매수 주문 실행)
                    if krw_balance > 20000:
                        buy_amount = krw_balance * 0.2
                        upbit.buy_market_order(ticker, buy_amount)
                        print(f"STEP26: {ticker} => {current_price:,.0f} > ema20{ema20:,.0f} > ema20{ema20:,.0f} > ema50{ema50:,.0f} > ema90{ema90:,.0f} > ema120{ema120:,.0f} > ema200{ema200:,.0f}") 
                        print(f"STEP26: {ticker} => Golden Cross Buy Signal")    
                        print(f"STEP26: {ticker} => {krw_balance} > 20,000원")   
                        print(f"STEP26: {ticker} => AutoTrade 매수완료 {buy_amount} = {krw_balance} * 0.2")

                elif current_price < ema15 and current_price < ma15 and current_price < ma5:
                    # Death Cross: Sell Signal
                    balance = get_balance(ticker.split('-')[-1])                
                    # 매도 조건 추가 (예: 주식 잔고가 0보다 큰 경우에만 매도 주문 실행)
                    if balance > 0:
                        sell_amount = balance * 0.9995
                        upbit.sell_market_order(ticker, sell_amount)
                        print(f"STEP27: {ticker} => {current_price:,.0f} < {ema15:,.0f} < {ma15:,.0f} < {ma5:,.0f}") 
                        print(f"STEP27: {ticker} => Death Cross Sell Signal")    
                        print(f"STEP27: {ticker} => {krw_balance} > 20,000원")   
                        print(f"STEP27: {ticker} => AutoTrade 매도완료 {sell_amount} = {balance} * 0.9995")
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)


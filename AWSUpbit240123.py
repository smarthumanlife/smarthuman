
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

    #visualize_backtest_results(df_results, ticker)

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


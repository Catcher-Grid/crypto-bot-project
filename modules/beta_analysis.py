def calculate_beta(asset_returns, market_returns):
    if len(asset_returns) != len(market_returns):
        min_len = min(len(asset_returns), len(market_returns))
        asset_returns = asset_returns[-min_len:]
        market_returns = market_returns[-min_len:]
    covariance = ((asset_returns - asset_returns.mean()) * (market_returns - market_returns.mean())).mean()
    variance = market_returns.var()
    return covariance / variance if variance != 0 else 0

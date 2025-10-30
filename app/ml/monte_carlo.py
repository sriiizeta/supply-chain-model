# monte_carlo.py
import numpy as np
import pandas as pd

def simulate_stockouts(demand_forecast_mean, demand_forecast_std, lead_time_mean, lead_time_std, current_inventory, reorder_qty, reorder_point, trials=10000):
    """
    Simulate future stockouts given forecast distribution and supplier lead time distribution.
    demand_forecast_mean, demand_forecast_std: arrays for each future period
    returns dictionary with probabilities and expected shortfall
    """
    periods = len(demand_forecast_mean)
    stockout_counts = np.zeros(periods)
    total_shortage = np.zeros(periods)
    for t in range(trials):
        inv = current_inventory
        for i in range(periods):
            demand = np.random.normal(demand_forecast_mean[i], demand_forecast_std[i])
            demand = max(0, demand)
            inv -= demand
            if inv < 0:
                stockout_counts[i] += 1
                total_shortage[i] += (-inv)
                inv = 0
            # reorder logic: if below reorder_point, receive after lead time
            if inv <= reorder_point:
                lead_time = max(0.1, np.random.normal(lead_time_mean, lead_time_std))
                # we approximate lead-time by adding inventory after lead_time periods; for simplicity, we add immediately:
                inv += reorder_qty
        # end periods
    prob_stockout = stockout_counts / trials
    expected_shortage = total_shortage / trials
    return {
        "prob_stockout": prob_stockout.tolist(),
        "expected_shortage": expected_shortage.tolist()
    }

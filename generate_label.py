import math

@dataclass
class OrderBook:
    trigger_instrument: str
    timestamp: float
    exch_time: float
    bidpx: float
    bidqty: int
    askpx: float
    askqty: float
    vwap_px: float
    vwap_qty: int
    pnl: float
    target: float
    exec_param: ExecutionParams
    max_position: int = field(default=0)

class KernelPriceReturnTarget(object):

    def __init__(self, kernel, pivot) -> None:
        self.kernel = kernel
        self.k_len = len(self.kernel)
        self.pivot = pivot
        self.valid = False

    def process(self, ts):
        ts_len = len(ts)
        data = [0.0 for i in range(ts_len)]

        for i in range(ts_len):
            s = max(i - self.pivot, 0)  # close
            e = min(i + self.k_len - self.pivot, ts_len)  # open
            sum_1 = 0.0
            weight_1 = 0.0
            sum_2 = 0.0
            weight_2 = 0.0
            # print(“____________________”)
            for j in range(s, e):
                k = self.pivot - i + j
                if j <= i:
                    sum_1 += ts[j] * self.kernel[k]
                    weight_1 += self.kernel[k]
                    #print(“i = {}. sum_1 += ts[{}] * kernel[{}], weight_1 += kernerl[{}], sum_1={}, weight_1={}”.format(i, j, k, k, sum_1, weight_1))
                else:
                    sum_2 += ts[j] * self.kernel[k]
                    weight_2 += self.kernel[k]
                    #print(“i = {}. sum_2 += ts[{}] * kernel[{}], weight_2 += kernerl[{}], sum_2={}, weight_2={}”.format(i, j, k, k, sum_2, weight_2))
            if weight_2 != 0:
                avg_1 = sum_1 / weight_1
                avg_2 = sum_2 / weight_2
                data[i] = (avg_2 - avg_1) / avg_1

        return data

class FutWgtPxChangeTarget(object):

    def __init__(self, weight_zero, weight_total, weight_ratio) -> None:
        self.weight_zero = weight_zero
        self.weight_total = weight_total
        self.weight_ratio = weight_ratio
        self.valid = False

    def process(self, order_books: list[OrderBook]):
        changes = []
        n = len(order_books)
        for current_index in range(n):
            current_data = order_books[current_index]
            t0 = current_data.timestamp
            current_midpx = (current_data.bidpx + current_data.askpx)/2
            sum_wgtpx = 0.0
            sum_w = 0.0
            
            # Iterate over future data points
            for future_index in range(current_index + 1, n):
                future_data = order_books[future_index]
                t_i = future_data.timestamp
                delta_t = t_i - t0 - self.weight_zero
                if delta_t < 1 - 1e-6:
                    # Within weight_zero period; weight is zero
                    continue
                if delta_t >= self.weight_total + 1e-6:
                    # Beyond the weight_total period; stop processing
                    break
                n_i = int(math.floor(delta_t - 1e-6))
                if n_i >= 0 and n_i < self.weight_total:
                    future_wgtpx = (future_data.bidpx + future_data.askpx)/2
                    w_i = self.weight_ratio ** n_i
                    sum_wgtpx += w_i * future_wgtpx
                    sum_w += w_i
            if sum_w > 0:
                avg_wgtpx = sum_wgtpx / sum_w
                change = avg_wgtpx - current_midpx
                changes.append(change)
            else:
                changes.append(None)
        return changes


if __name__ == '__main__':
    t1 = KernelPriceReturnTarget([-1, 1], 0)
    v = [8.0, 9.0, 7.0, 5.0, 6.0, 8.0, 2.0, 3.0, 4.0, 2.0,
         1.0, 9.0, 3.0, 6.0, 5.0, 4.0, 3.0, 8.0, 7.0, 6.0]
    d = t1.process(v)

    t2 = KernelPriceReturnTarget([-1, 0, 1], 0)
    d = t2.process(v)

    t3 = KernelPriceReturnTarget([-1, 0, 1, 0.975, 0.975 ** 2, 0.975 ** 3], 0)
    d = t3.process(v)

    t4 = KernelPriceReturnTarget(
        [-0.975 ** 2, -0.975, -1, 0, 1, 0.975, 0.975 ** 2, 0.975 ** 3], 2)
    d = t4.process(v)
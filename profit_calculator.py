"""メルカリ転売利益計算モジュール"""

class ProfitCalculator:
    """Amazon仕入れ -> メルカリ売却の利益を計算"""

    MERCARI_FEE_RATE = 0.10  # メルカリ手数料 10%
    SHIPPING_COST = 500  # 送料（目安）

    @staticmethod
    def calculate(mercari_price: float, amazon_price: float, shipping_cost: float = None) -> dict:
        """
        利益を計算する

        Args:
            mercari_price: メルカリでの想定売却価格
            amazon_price: Amazonでの仕入れ価格
            shipping_cost: 送料（デフォルト: 500円）

        Returns:
            {
                'mercari_price': メルカリ売却価格,
                'amazon_price': Amazon仕入れ価格,
                'mercari_fee': メルカリ手数料,
                'shipping_cost': 送料,
                'profit': 利益,
                'profit_rate': 利益率 (%),
                'is_profitable': 利益が出るか
            }
        """
        if shipping_cost is None:
            shipping_cost = ProfitCalculator.SHIPPING_COST

        mercari_fee = mercari_price * ProfitCalculator.MERCARI_FEE_RATE
        profit = mercari_price - mercari_fee - amazon_price - shipping_cost
        profit_rate = (profit / amazon_price * 100) if amazon_price > 0 else 0

        return {
            'mercari_price': round(mercari_price, 2),
            'amazon_price': round(amazon_price, 2),
            'mercari_fee': round(mercari_fee, 2),
            'shipping_cost': round(shipping_cost, 2),
            'profit': round(profit, 2),
            'profit_rate': round(profit_rate, 2),
            'is_profitable': profit > 0
        }

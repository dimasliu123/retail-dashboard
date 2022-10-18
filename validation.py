from dataclasses import dataclass

@dataclass
class HomeDataValidation:
    total_sales : float
    top_country : str
    top_country_sales : float
    hot_product : str
    product_quantity : int
    product_sales : float
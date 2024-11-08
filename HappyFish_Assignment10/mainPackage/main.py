# main.py

import random
from dbUtilitiesPackage.dbUtilities import connect_to_database
from queryUtilitiesPackage.queryUtilities import fetch_query_results

if __name__ == "__main__":
    # Step 1: Connect to the database and fetch product data
    product_query = "SELECT ProductID, [UPC-A ], Description, ManufacturerID, BrandID FROM tProduct"
    product_data = fetch_query_results(product_query)
    
    # Check if product data was fetched
    if not product_data:
        print("No product data found or query returned no data.")
    else:
        # Step 2: Randomly select a product
        selected_product = random.choice(product_data)
        product_id = selected_product[0]
        description = selected_product[2] if selected_product[2] else "Unknown Product"  # Fallback if Description is empty
        manufacturer_id = selected_product[3]
        brand_id = selected_product[4]

        # Step 3 & 4: Fetch Manufacturer name
        manufacturer_query = f"SELECT Manufacturer FROM tManufacturer WHERE ManufacturerID = {manufacturer_id}"
        manufacturer_data = fetch_query_results(manufacturer_query)
        if manufacturer_data:
            manufacturer_name = manufacturer_data[0][0]
        else:
            print(f"No manufacturer found for ManufacturerID {manufacturer_id}.")
            manufacturer_name = "Unknown Manufacturer"

        # Step 5: Fetch Brand name
        brand_query = f"SELECT Brand FROM tBrand WHERE BrandID = {brand_id}"
        brand_data = fetch_query_results(brand_query)
        if brand_data:
            brand_name = brand_data[0][0]
        else:
            print(f"No brand found for BrandID {brand_id}.")
            brand_name = "Unknown Brand"

        # Step 6: Fetch the number of items sold for the selected product
        sales_query = f"""
        SELECT TOP (100) PERCENT SUM(dbo.tTransactionDetail.QtyOfProduct) AS NumberOfItemsSold
        FROM dbo.tTransactionDetail
        INNER JOIN dbo.tTransaction ON dbo.tTransactionDetail.TransactionID = dbo.tTransaction.TransactionID
        WHERE (dbo.tTransaction.TransactionTypeID = 1) AND (dbo.tTransactionDetail.ProductID = {product_id})
        """
        sales_data = fetch_query_results(sales_query)
        if sales_data:
            number_of_items_sold = sales_data[0][0]
        else:
            print(f"No sales data found for ProductID {product_id}.")
            number_of_items_sold = 0

        # Step 7: Print the result as a grammatically correct sentence
        result_sentence = (
            f"The product '{description}' manufactured by '{manufacturer_name}' "
            f"under the brand '{brand_name}' has sold {number_of_items_sold} items."
        )
        print(result_sentence)

#!/bin/bash

# Define your FastAPI server URL
API_URL="http://localhost:8000/products"

# Example cool product names, prices, and stock quantities
declare -a names=("GlowTech Smart Watch" "VibeMax Wireless Earbuds" "EcoWave Water Bottle" "SkyRunner Sneakers" "Nebula Gaming Mouse" "UltraBoost 4K Monitor" "AeroShield Laptop Backpack" "Vortex Fitness Tracker" "InstaGlow LED Lamp" "Quantum-X Gaming Chair" "PicoSmart Digital Camera" "HyperVolt Power Bank" "Zenith Pro Headphones" "PixelMaster Phone Case" "BoostX Smart Plug" "CosmoSound Bluetooth Speaker" "Eclipse Smart Bulb" "StealthTech Gaming Keyboard" "SolarFlare Power Charger" "EonTrack GPS Watch")

declare -a prices=(150.0 80.0 25.0 120.0 50.0 300.0 70.0 90.0 35.0 250.0 150.0 60.0 180.0 40.0 25.0 45.0 40.0 100.0 80.0 200.0)

# Stock quantities with some products having less than 3 in stock
declare -a stock_quantities=(100 2 200 1 300 400 500 2 700 800 900 1 1100 1200 1300 1400 1500 1600 2 1800)

# Loop to create 20 products
for i in ${!names[@]}; do
  PRODUCT_NAME=${names[$i]}
  PRODUCT_PRICE=${prices[$i]}
  PRODUCT_STOCK=${stock_quantities[$i]}

  # Create a JSON payload with the product data
  PRODUCT_JSON=$(cat <<EOF
{
  "name": "$PRODUCT_NAME",
  "price": $PRODUCT_PRICE,
  "stock_quantity": $PRODUCT_STOCK
}
EOF
)

  # Send a POST request to the FastAPI server to create the product
  curl -X 'POST' \
    "$API_URL" \
    -H 'Content-Type: application/json' \
    -d "$PRODUCT_JSON"

  echo "Product $PRODUCT_NAME created with $PRODUCT_STOCK items in stock."
done

echo "All products imported successfully."

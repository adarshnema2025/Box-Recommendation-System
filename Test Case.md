## Test Case 1: Exact Boundary Fit
Description: Verifies that a product whose dimensions, volume, and weight exactly equal a box's limits is still accepted (confirms <= comparisons, not strict <).

Request:

{
  "products": [
    {"length": 30, "width": 25, "height": 20, "weight": 8, "quantity": 1}
  ]
}

Expected Result: 200 OK, recommended_box.serial_no = "BOX-004"

## Test Case 2: Aggregated Totals Override Small Individual Items
Description: Verifies that even when each individual product is small enough to fit a small box dimensionally, the box is still rejected if the combined volume/weight of all products exceeds that box's capacity — confirming aggregation logic runs independently of the per-item dimension check.

Request:
{
  "products": [
    {"length": 8, "width": 8, "height": 8, "weight": 0.4, "quantity": 4},
    {"length": 6, "width": 6, "height": 6, "weight": 0.3, "quantity": 2}
  ]
}  

Expected Result: 200 OK, recommended_box.serial_no = "BOX-003", total_weight = 2.2, total_volume = 2480.0

## Test Case 3: Single Oversized Dimension Returns 404
Description: Verifies that a product exceeding every box's maximum length (even though its weight and other dimensions are trivially small) correctly returns a 404, confirming the per-axis dimension check independently blocks a match.

Request:

{
  "products": [
    {"length": 71, "width": 10, "height": 10, "weight": 1, "quantity": 1}
  ]
}

Expected Result: 404 Not Found, recommended_box: null

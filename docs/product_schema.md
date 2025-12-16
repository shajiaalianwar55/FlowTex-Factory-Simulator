# T-Shirt Product Schema (Factory Simulation Project)

## Identification Fields
- **product_id**: Unique ID for each T-shirt (e.g., "T000123").
- **product_line**: The production line where the product was made (e.g., "Line A", "Line B", "Line C").
- **batch_id**: ID for the batch or group of products (e.g., "B20250301_01").
- **line_sequence**: The sequence number of this product within its production line.

## Physical Attributes
- **size**: One of XS, S, M, L, XL.
- **color**: The color of the T-shirt.
- **weight_g**: Weight of the T-shirt in grams (e.g., 180.5).

## Production Metadata
- **production_timestamp**: The date/time when the product entered the factory system (ISO format).

## Quality Control / Inspection Fields
- **raw_defect_score**: A number between 0 and 1 showing defect severity (higher = worse).
- **inspected**: Boolean indicating whether inspection happened (True/False).
- **passed_inspection**: Boolean indicating whether product passed inspection.
- **rejection_reason**: If rejected, contains the reason (e.g., "stain", "hole", "misprint", etc.), else empty.
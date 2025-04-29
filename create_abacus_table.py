"""
This script outlines the steps to create the custom transaction table in Abacus.ai
for the Nick the Great agent.

Please follow these steps in the Abacus.ai interface:

1. Navigate to the "Set-up Data Pipelines" section.
2. Click "Create or Attach Dataset".
3. Select "Custom Table" as the data type.
4. Name the table "nick_great_transactions".
5. Define the schema using the fields outlined below.
6. Set appropriate indexing on frequently queried fields (transaction_id, timestamp, payment_type, amount, category, approval_status).

Table Schema:

Core Fields:
- transaction_id (String): Unique identifier for each transaction (Primary key)
- timestamp (DateTime): Date and time of the transaction
- payment_method_id (String): Identifier for the payment method used
- payment_type (Enum): Type of payment method (Virtual Card - Operational, Virtual Card - Marketing, Payment Processor, Cryptocurrency, Primary Bank)
- amount (Decimal): Transaction amount
- currency (String): Transaction currency code
- merchant (String): Name of the merchant or service provider
- category (String): Transaction category
- purpose_code (String): Code indicating the business purpose
- time_sensitivity (Boolean): Flag for time-sensitive transactions
- approval_status (Enum): Status (Auto-approved, Pending, Approved, Rejected, Escalated)
- approval_timestamp (DateTime): When approval decision was made
- approver_id (String): ID of human approver (if applicable)

Additional Fields for Compliance and Audit:
- decision_rationale (Text): Explanation of why transaction was approved/rejected
- autonomous_limit (Decimal): Applicable limit at time of transaction
- daily_total (Decimal): Running total for the day at time of transaction
- special_logging (Boolean): Flag for transactions processed under special conditions
- risk_score (Decimal): Calculated risk score for the transaction
- framework_version (String): Version of the framework applied
- notification_id (String): Reference to any notifications sent

Metadata Fields:
- created_at (DateTime): Record creation timestamp
- updated_at (DateTime): Last update timestamp
- source_system (String): System that initiated the transaction
- geographic_location (String): Location of transaction
- device_fingerprint (String): Device identifier if applicable
- session_id (String): Session identifier if applicable

Example Usage:
To create the table, navigate to the Abacus.ai interface and follow the steps outlined above.
"""

print("Please follow the instructions in this script to create the table in Abacus.ai")

# Custom Table Setup for Nick the Great in Abacus.ai

This document provides detailed information about the custom table setup required for the Nick the Great agent in Abacus.ai. The custom table is a critical component that enables the agent to make financial decisions based on the parameters defined in the preauthorized_accounts_framework.

## Purpose of the Custom Table

The custom transaction table serves as the central data repository for all financial transactions processed by the Nick the Great agent. It enables:

1. **Autonomous Decision-Making**: Provides the data structure needed for the agent to apply the decision thresholds defined in the frameworks
2. **Transaction Tracking**: Maintains a comprehensive record of all financial activities
3. **Compliance and Auditing**: Supports the audit requirements specified in the frameworks
4. **Performance Analysis**: Enables analysis of transaction patterns and optimization opportunities

## Table Structure

### Core Fields

| Field Name | Data Type | Description | Purpose |
|------------|-----------|-------------|---------|
| transaction_id | String | Unique identifier for each transaction | Primary key for transaction tracking |
| timestamp | DateTime | Date and time of the transaction | Temporal tracking and reporting |
| payment_method_id | String | Identifier for the payment method used | Links to payment method hierarchy |
| payment_type | Enum | Type of payment method (Virtual Card - Operational, Virtual Card - Marketing, Payment Processor, Cryptocurrency, Primary Bank) | Determines applicable transaction limits |
| amount | Decimal | Transaction amount | For comparison against autonomous limits |
| currency | String | Transaction currency code | For standardization and conversion |
| merchant | String | Name of the merchant or service provider | For category verification and reporting |
| category | String | Transaction category | For verification against pre-approved categories |
| purpose_code | String | Code indicating the business purpose | For association with strategies and initiatives |
| time_sensitivity | Boolean | Flag for time-sensitive transactions | Determines approval workflow |
| approval_status | Enum | Status (Auto-approved, Pending, Approved, Rejected, Escalated) | Tracks approval workflow state |
| approval_timestamp | DateTime | When approval decision was made | For audit and response time tracking |
| approver_id | String | ID of human approver (if applicable) | For audit and accountability |

### Additional Fields for Compliance and Audit

| Field Name | Data Type | Description | Purpose |
|------------|-----------|-------------|---------|
| decision_rationale | Text | Explanation of why transaction was approved/rejected | For audit and learning |
| autonomous_limit | Decimal | Applicable limit at time of transaction | For historical reference and audit |
| daily_total | Decimal | Running total for the day at time of transaction | For limit enforcement |
| special_logging | Boolean | Flag for transactions processed under special conditions | For audit and review |
| risk_score | Decimal | Calculated risk score for the transaction | For fraud prevention |
| framework_version | String | Version of the framework applied | For audit and framework evolution |
| notification_id | String | Reference to any notifications sent | For tracing notification workflow |

### Metadata Fields

| Field Name | Data Type | Description | Purpose |
|------------|-----------|-------------|---------|
| created_at | DateTime | Record creation timestamp | For system tracking |
| updated_at | DateTime | Last update timestamp | For change tracking |
| source_system | String | System that initiated the transaction | For integration tracking |
| geographic_location | String | Location of transaction | For geographic restrictions |
| device_fingerprint | String | Device identifier if applicable | For security monitoring |
| session_id | String | Session identifier if applicable | For security correlation |

## Relationships to Other Data

The transaction table relates to several other data structures in the system:

1. **Payment Method Registry**: Links via `payment_method_id` to track available payment methods and their limits
2. **Merchant Category Codes**: Links via `category` to verify against pre-approved merchant categories
3. **Approval Workflow**: Links via `approval_status` and `approver_id` to the notification and approval system
4. **Strategy Initiatives**: Links via `purpose_code` to associate transactions with specific business strategies
5. **Audit Logs**: All transactions feed into the audit logging system for compliance

## Implementation in Abacus.ai

### Table Creation Process

1. In the Abacus.ai interface, navigate to the "Set-up Data Pipelines" section
2. Click "Create or Attach Dataset"
3. Select "Custom Table" as the data type
4. Name the table "nick_great_transactions"
5. Define the schema using the fields outlined above
6. Set appropriate indexing on frequently queried fields (transaction_id, timestamp, payment_type, amount, category, approval_status)

### Data Sources

The transaction table can be populated from multiple sources:

1. **Direct API Integration**: Connect to payment processors, banking APIs, and financial platforms
2. **Manual Entry**: For transactions that require manual processing
3. **Batch Import**: For historical transaction data
4. **Simulated Transactions**: For testing and training purposes

### Usage by the Agent

The Nick the Great agent will interact with this table in several ways:

1. **Transaction Verification**: Before processing a transaction, the agent will:
   - Check if the amount is within the autonomous limit for the payment type
   - Verify the merchant category is pre-approved
   - Check daily totals against daily limits
   - Apply time-sensitivity rules if applicable

2. **Approval Workflow**: For transactions exceeding autonomous limits:
   - Create a pending transaction record
   - Initiate the approval request via the notification system
   - Update the record based on approval response or timeout rules

3. **Reporting and Analytics**: The agent will:
   - Generate daily transaction summaries
   - Analyze spending patterns by category
   - Monitor limit utilization
   - Identify optimization opportunities

4. **Audit and Compliance**: The agent will:
   - Maintain immutable transaction records
   - Associate transactions with business purposes
   - Generate compliance reports
   - Support audit requirements

## Example Transaction Records

### Example 1: Auto-approved Transaction

```json
{
  "transaction_id": "txn_20250425_001",
  "timestamp": "2025-04-25T09:15:23Z",
  "payment_method_id": "vc_op_001",
  "payment_type": "Virtual Card - Operational",
  "amount": 75.00,
  "currency": "USD",
  "merchant": "Adobe Systems",
  "category": "Software Subscription",
  "purpose_code": "CONTENT_PROD_TOOLS",
  "time_sensitivity": false,
  "approval_status": "Auto-approved",
  "approval_timestamp": "2025-04-25T09:15:23Z",
  "approver_id": "system",
  "decision_rationale": "Within autonomous limit of $100 for operational card and approved category",
  "autonomous_limit": 100.00,
  "daily_total": 75.00,
  "special_logging": false,
  "risk_score": 0.12,
  "framework_version": "1.2.0",
  "notification_id": null
}
```

### Example 2: Transaction Requiring Approval

```json
{
  "transaction_id": "txn_20250425_002",
  "timestamp": "2025-04-25T10:30:45Z",
  "payment_method_id": "vc_op_001",
  "payment_type": "Virtual Card - Operational",
  "amount": 150.00,
  "currency": "USD",
  "merchant": "Semrush",
  "category": "Marketing Tools",
  "purpose_code": "SEO_ANALYTICS",
  "time_sensitivity": true,
  "approval_status": "Pending",
  "approval_timestamp": null,
  "approver_id": null,
  "decision_rationale": "Exceeds autonomous limit of $100 for operational card",
  "autonomous_limit": 100.00,
  "daily_total": 225.00,
  "special_logging": false,
  "risk_score": 0.28,
  "framework_version": "1.2.0",
  "notification_id": "notif_20250425_002"
}
```

### Example 3: Auto-approved Time-sensitive Transaction with Special Logging

```json
{
  "transaction_id": "txn_20250425_003",
  "timestamp": "2025-04-25T14:45:12Z",
  "payment_method_id": "vc_op_001",
  "payment_type": "Virtual Card - Operational",
  "amount": 120.00,
  "currency": "USD",
  "merchant": "Mailchimp",
  "category": "Email Marketing",
  "purpose_code": "CUSTOMER_ENGAGEMENT",
  "time_sensitivity": true,
  "approval_status": "Auto-approved",
  "approval_timestamp": "2025-04-25T18:45:12Z",
  "approver_id": "system",
  "decision_rationale": "Time-sensitive transaction, no response within 4 hours, amount within 1.5x limit",
  "autonomous_limit": 100.00,
  "daily_total": 345.00,
  "special_logging": true,
  "risk_score": 0.35,
  "framework_version": "1.2.0",
  "notification_id": "notif_20250425_003"
}
```

## Integration with Feature Groups

The transaction data should be integrated with feature groups in Abacus.ai to enable the agent's decision-making capabilities:

1. **Financial Decision Features**:
   - Transaction amount relative to limits
   - Daily spending relative to daily limits
   - Category approval status
   - Historical transaction success rate

2. **Risk Management Features**:
   - Risk scores
   - Anomaly detection
   - Velocity checks
   - Geographic patterns

3. **Performance Optimization Features**:
   - Approval workflow efficiency
   - Response time metrics
   - Auto-approval rates
   - Exception handling metrics

## Conclusion

The custom transaction table is a foundational element of the Nick the Great agent's autonomous operation in Abacus.ai. By properly implementing this data structure with all the necessary fields and relationships, you enable the agent to make financial decisions according to the preauthorized_accounts_framework while maintaining appropriate security, compliance, and oversight.
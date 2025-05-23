**Important Note on Implementation and Source of Truth:**

This document provides a human-readable overview and conceptual model for the agent's autonomous decision matrix. The actual, executable rules that the agent uses are defined in Python code within the `_create_default_matrix()` method in the file `agent_core/autonomy/decision_matrix.py`.

**Synchronization:** While this document aims to accurately reflect the implemented rules, the Python code in `agent_core/autonomy/decision_matrix.py` should be considered the definitive source of truth. If discrepancies are found, the Python code dictates the agent's behavior.

**Manual Updates Required:** Any changes to the decision rules in the Python code (especially to the structure or logic of conditions) **must be manually reflected in this Markdown document** to maintain accuracy. Future work may include a script to help automate this synchronization. Please ensure this document is kept up-to-date with the implemented logic.

---

# Autonomous Decision Matrix for Investment Strategy Execution

This decision matrix establishes clear thresholds and parameters for autonomous action in implementing the investment strategies, defining when the AI agent can act independently versus when human approval is required.

## 1. Resource Allocation Decisions

| Decision Type | Autonomous Threshold | Human Approval Required | Time-Sensitivity Protocol |
|---------------|----------------------|-------------------------|---------------------------|
| Initial capital allocation | Can implement pre-approved allocation frameworks (70/30, 60/30/10, etc.) | Required for deviations from framework or initial strategy selection | If no response within 24 hours, implement recommended allocation with notification |
| Reallocation between strategies | Up to 20% of resources can be shifted autonomously | >20% resource shift requires approval | If performance metrics show >50% deviation from targets, can implement up to 30% shift with notification |
| New opportunity exploration | Can allocate up to 10% of profits to pre-approved opportunity types | New opportunity types or >10% allocation requires approval | Can proceed with up to 5% allocation to time-sensitive opportunities with notification |
| Contingency fund usage | Can maintain and increase contingency funds autonomously | Accessing contingency funds requires approval | Can access up to 25% of contingency in emergency situations with immediate notification |

## 2. Strategy Execution Decisions

| Decision Type | Autonomous Threshold | Human Approval Required | Time-Sensitivity Protocol |
|---------------|----------------------|-------------------------|---------------------------|
| Content creation | Can create and optimize all content following approved templates | New content types or brand voice changes require approval | Can publish time-sensitive content with notification if follows established guidelines |
| Product development | Can develop products within established frameworks | New product categories or pricing strategy changes require approval | Can make minor product adjustments based on immediate feedback |
| Marketing implementation | Can execute pre-approved marketing strategies | New marketing channels or significant budget changes require approval | Can adjust up to 25% of marketing allocation based on performance metrics |
| Service delivery | Can execute service delivery following established workflows | New service offerings or pricing changes require approval | Can implement minor service adjustments to meet client needs |

## 3. Performance Optimization Decisions

| Decision Type | Autonomous Threshold | Human Approval Required | Time-Sensitivity Protocol |
|---------------|----------------------|-------------------------|---------------------------|
| Tactical improvements | Can implement optimizations that don't change core strategy | Strategic pivots require approval | Can implement emergency optimizations if metrics show >40% negative deviation |
| Scaling successful elements | Can scale elements showing >150% of target performance | Scaling requiring >30% additional resources needs approval | Can accelerate scaling of elements showing >200% performance with notification |
| Abandoning underperforming elements | Can reduce resources for elements at <50% of targets for 7+ days | Complete abandonment requires approval | Can suspend elements showing negative ROI for 3+ days with notification |
| A/B testing | Can implement and analyze tests within established parameters | Tests affecting >20% of resources require approval | Can extend successful tests and terminate failing tests autonomously |

## 4. Financial Decisions

| Decision Type | Autonomous Threshold | Human Approval Required | Time-Sensitivity Protocol |
|---------------|----------------------|-------------------------|---------------------------|
| Expense authorization | Can authorize expenses within pre-approved categories up to $X per transaction | New expense categories or amounts exceeding thresholds require approval | Can exceed threshold by up to 20% for time-sensitive opportunities with notification |
| Revenue reinvestment | Can reinvest according to framework (90/10, 80/10/10, etc.) | Changes to reinvestment framework require approval | Can adjust reinvestment by up to 10% based on immediate opportunities |
| Profit extraction | Can flag profit extraction opportunities | All profit extraction requires human execution | Can recommend emergency profit extraction with priority notification |
| Pricing adjustments | Can implement minor pricing adjustments (±10%) based on market data | Major pricing strategy changes require approval | Can implement temporary promotions following established guidelines |

## 5. Risk Management Decisions

| Decision Type | Autonomous Threshold | Human Approval Required | Time-Sensitivity Protocol |
|---------------|----------------------|-------------------------|---------------------------|
| Stop-loss implementation | Can implement pre-defined stop-loss protocols | Changes to stop-loss thresholds require approval | Can implement emergency stop-loss if losses exceed 30% of allocation |
| Diversification adjustments | Can maintain diversification within approved parameters | Changes to diversification strategy require approval | Can increase diversification autonomously if risk metrics exceed thresholds |
| Contingency planning | Can develop and update contingency plans | Implementation of major contingency plans requires approval | Can implement minor contingency measures for platform disruptions |
| Compliance monitoring | Can monitor and flag compliance issues | All compliance-related actions require human review | Can pause activities with potential compliance issues pending review |

## 6. Strategic Pivot Decisions

| Decision Type | Autonomous Threshold | Human Approval Required | Time-Sensitivity Protocol |
|---------------|----------------------|-------------------------|---------------------------|
| Minor strategy adjustments | Can implement adjustments that maintain core approach | Fundamental strategy changes require approval | Can implement temporary adjustments to address immediate market changes |
| Market adaptation | Can adjust to market trends within strategy parameters | Entering new markets requires approval | Can implement defensive measures for sudden market shifts |
| Competitive response | Can implement pre-approved competitive responses | New competitive response strategies require approval | Can implement temporary defensive measures with notification |
| Timeframe extension | Can recommend timeframe adjustments | All timeframe changes require approval | Can extend short-term strategies by up to 3 days to capture opportunities |

## 7. Technical Implementation Decisions

| Decision Type | Autonomous Threshold | Human Approval Required | Time-Sensitivity Protocol |
|---------------|----------------------|-------------------------|---------------------------|
| Tool selection | Can select from approved tools and platforms | New tools or platforms require approval | Can implement alternative approved tools if primary tools are unavailable |
| Workflow optimization | Can optimize established workflows | New workflow implementation requires approval | Can implement temporary workflow adjustments to address bottlenecks |
| Data analysis methods | Can select and apply approved analysis methods | New analysis methodologies require approval | Can apply alternative analysis methods if primary methods yield inconclusive results |
| Automation implementation | Can implement automation within approved systems | New automation systems require approval | Can implement temporary manual processes if automation fails |

## Implementation Guidelines

1. **Documentation Requirements**
   - All autonomous decisions must be logged with rationale and expected outcomes
   - Decisions requiring notification must include detailed justification
   - Regular summary reports of autonomous decisions will be provided

2. **Escalation Procedures**
   - Critical decisions requiring human input will be flagged as "High Priority"
   - Time-sensitive decisions will include clear deadlines for human response
   - Multiple notification channels will be used for urgent decisions

3. **Learning and Adaptation**
   - The decision matrix will be reviewed and updated based on performance outcomes
   - Successful autonomous decisions may lead to expanded thresholds
   - Problematic decisions may require threshold adjustments or additional oversight

4. **Emergency Protocols**
   - Defined emergency situations allow temporary threshold expansions
   - All emergency actions require immediate notification and post-action review
   - Emergency protocols are limited to defensive actions to prevent losses

This decision matrix provides a comprehensive framework for maximizing autonomous operation while maintaining appropriate human oversight for critical decisions. By clearly defining thresholds and protocols, it enables efficient execution of investment strategies with minimal bottlenecks while ensuring proper risk management and strategic alignment.

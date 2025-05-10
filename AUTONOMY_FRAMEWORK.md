# Autonomy Framework

The Autonomy Framework for Nick the Great provides a sophisticated system for determining when the agent can act autonomously and when it needs human approval. It is designed to balance efficiency with appropriate oversight.

## Key Components

### 1. Decision Categories

The framework categorizes decisions into different types:

- **Experiment Management**: Creating, running, and analyzing experiments
- **Content Creation**: Generating content like articles, ebooks, etc.
- **Financial**: Actions involving money or financial resources
- **Platform Interaction**: Interactions with external platforms
- **System**: Internal system operations
- **Resource Allocation**: Allocating resources to different tasks
- **Strategy Adjustment**: Changes to strategic approach
- **New Opportunity**: Exploring new opportunities
- **Platform Expansion**: Expanding to new platforms

### 2. Risk Levels

Each action is assessed for its risk level:

- **Low**: Minimal risk, can usually be performed autonomously
- **Medium**: Moderate risk, may require notification
- **High**: Significant risk, typically requires approval
- **Critical**: Highest risk, may be prohibited

### 3. Approval Levels

Based on the decision category and risk level, actions are assigned an approval level:

- **Autonomous**: Agent can act without human approval
- **Notify**: Agent can act but must notify humans
- **Approval Required**: Agent must get human approval before acting
- **Prohibited**: Agent cannot perform this action

### 4. Decision Matrix

The Decision Matrix maps decision categories and risk levels to approval levels. For example:

| Category | Low Risk | Medium Risk | High Risk | Critical Risk |
|----------|----------|-------------|-----------|---------------|
| Experiment Management | Autonomous | Notify | Approval Required | Prohibited |
| Content Creation | Autonomous | Notify | Approval Required | Prohibited |
| Financial | Notify | Approval Required | Approval Required | Prohibited |
| Platform Interaction | Autonomous | Notify | Approval Required | Prohibited |
| System | Autonomous | Notify | Approval Required | Prohibited |
| Resource Allocation | Autonomous (<10% change) | Notify (10-25% change) | Approval Required (>25% change) | Prohibited |
| Strategy Adjustment | Autonomous (Tactical) | Notify (Secondary) | Approval Required (Primary) | Prohibited |
| New Opportunity | Autonomous (Research) | Notify (Small-scale testing) | Approval Required (Significant resources) | Prohibited |
| Platform Expansion | Autonomous (Additional content) | Notify (New features) | Approval Required (New platform) | Prohibited |

### 5. Notification System

The Notification System manages communications with humans:

- **Notification Types**: Info, Warning, Error, Success
- **Notification Priorities**: Low, Medium, High, Critical
- **Notification Channels**: Dashboard, Email, SMS, Mobile Push, Slack, Webhook
- **Notification Preferences**: User-specific preferences for channels, batching, and do-not-disturb periods
- **Notification Batching**: Grouping notifications to avoid overwhelming users

### 6. Approval Workflow

The Approval Workflow manages the process of requesting and processing human approvals:

- **Approval Requests**: Structured requests for human approval
- **Approval Delegation**: Allowing designated users to approve on behalf of others
- **Approval Templates**: Reusable templates for common approval scenarios
- **Auto-Approval/Rejection**: Automatic approval or rejection after a specified time
- **Approval Expiration**: Handling of expired approval requests

### 7. Risk Tolerance Framework

The Risk Tolerance Framework assesses the risk of actions and determines if they are within tolerance levels:

- **Risk Categories**: Financial, Reputation, Operational, Compliance, Security, Performance
- **Risk Levels**: Minimal, Low, Medium, High, Critical
- **Risk Tolerance Profiles**: Conservative, Balanced, Aggressive
- **Risk Assessment**: Evaluation of actions against risk tolerance profiles
- **Risk Mitigation**: Strategies for reducing risk to acceptable levels

### 8. Experimentation Framework

The Experimentation Framework allows the agent to run controlled experiments within predefined boundaries:

- **Experiment Types**: A/B Test, Multivariate Test, Feature Test, Content Test, Pricing Test, Audience Test, Platform Test, Product Test, Risk Tolerance, Decision Making
- **Experiment Templates**: Predefined templates with parameters, sample size ranges, duration ranges, and budget limits
- **Experiment Validation**: Validation of experiment parameters against templates
- **Experiment Approval**: Integration with the approval workflow for experiments requiring approval
- **Experiment Metrics**: Tracking and analysis of experiment results
- **Experiment Lifecycle**: Creation, running, pausing, resuming, completing, and cancelling experiments

## Usage

### Determining Autonomy

```python
# Check if the agent can execute an action
can_execute, reason = autonomy_framework.can_execute(
    category=DecisionCategory.CONTENT_CREATION,
    action="publish_article",
    context={
        "metrics": {
            "content_length": 1500,
            "sensitivity_score": 0.2
        }
    }
)

if can_execute:
    # Execute the action
    if reason == "Notification required":
        # Create a notification
        notification_system.create_notification(
            title="Article Published",
            message="The agent has published an article.",
            notification_type=NotificationType.INFO,
            priority=NotificationPriority.MEDIUM,
            user_id="admin"
        )
else:
    # Request approval
    approval_workflow.create_approval_request(
        title="Approval Required: Publish Article",
        description="The agent requires approval to publish an article.",
        category=DecisionCategory.CONTENT_CREATION,
        action="publish_article",
        context={
            "content_length": 1500,
            "sensitivity_score": 0.2
        },
        user_id="admin"
    )
```

### Running Experiments

#### Content A/B Test Experiment

```python
# Create a content A/B test experiment
experiment, warnings = experimentation_framework.create_experiment(
    name="A/B Test: Article Headlines",
    experiment_type=ExperimentType.A_B_TEST,
    description="Testing two different headlines for an article",
    parameters={
        "headline_a": "10 Ways to Improve Your Writing",
        "headline_b": "Improve Your Writing with These 10 Tips",
        "target_audience": "writers",
        "metric": "click_through_rate"
    },
    sample_size=2000,
    duration=5,
    budget=100.0,
    success_criteria={
        "min_improvement": 0.1,
        "confidence_level": 0.95
    },
    template_id="ab_content_template"
)

# Start the experiment
success, error = experimentation_framework.start_experiment(experiment.id)
if not success:
    print(f"Failed to start experiment: {error}")
```

#### Risk Tolerance Experiment

```python
# Create a risk tolerance experiment
experiment = autonomy_framework.create_experiment(
    name="Risk Tolerance Experiment",
    experiment_type=ExperimentType.RISK_TOLERANCE,
    description="Testing different risk tolerance levels",
    parameters={
        "initial_profile": "balanced",
        "test_profiles": ["conservative", "aggressive"],
        "test_actions": ["create_experiment", "spend_money", "publish_content"]
    },
    success_criteria={
        "completion_rate": 1.0,
        "error_rate": 0.0
    }
)

# Start the experiment
experiment.start()

# Update metrics during the experiment
experiment.update_metrics({
    "completion_rate": 1.0,
    "error_rate": 0.0,
    "conservative_approval_rate": 0.8,
    "balanced_approval_rate": 0.5,
    "aggressive_approval_rate": 0.2
})

# Complete the experiment with results
experiment.complete({
    "completion_rate": 1.0,
    "error_rate": 0.0,
    "best_profile": "balanced"
})
```

## Initialization

To initialize the frameworks:

```python
from initialize_frameworks import initialize_frameworks

# Initialize the frameworks
autonomy_framework, experimentation_framework = initialize_frameworks()
```

## Future Enhancements

1. **Learning from Decisions**: Implementing machine learning to improve decision-making based on past decisions
2. **Advanced Risk Assessment**: More sophisticated risk assessment based on multiple factors
3. **User Feedback Integration**: Incorporating user feedback into the decision matrix
4. **Multi-level Approval**: Supporting multi-level approval workflows for high-risk actions
5. **Adaptive Experimentation**: Automatically adjusting experiments based on early results

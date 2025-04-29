# Experiment Tracking Spreadsheet Template

This document provides the structure and formulas for creating a comprehensive tracking spreadsheet to monitor all parallel experiments within the Nick the Great system. This template should be implemented in Google Sheets to allow for easy access, collaboration, and automatic calculations.

## Spreadsheet Structure

### 1. Summary Dashboard Tab

**Purpose:** Provide at-a-glance performance metrics for all active experiments.

**Columns:**
- Experiment ID
- Experiment Name
- Status (Planning/Active/Paused/Completed/Terminated)
- Current Phase
- Days Active
- Total Revenue Generated ($)
- Total Human Time Invested (hours)
- Return on Time Invested (ROTI) - $/hour
- Week-over-Week Growth Rate (%)
- Audience/Customer Growth (%)
- Performance vs. Threshold (visualization)
- Resource Allocation (%)
- Next Review Date

**Features:**
- Color-coded status indicators (green for above threshold, yellow for adjustment zone, red for below threshold)
- Small sparkline charts showing week-over-week trends
- Conditional formatting to highlight experiments needing attention
- Auto-calculated metrics pulled from individual experiment tabs

### 2. Individual Experiment Tabs (One per experiment)

**Purpose:** Track detailed metrics for each specific experiment.

**Sections:**

#### a. Basic Information
- Experiment Name
- Experiment ID
- Start Date
- Status
- Current Phase
- Business Model Category
- Primary Platform

#### b. Revenue Tracking
**Columns:**
- Date
- Revenue Source
- Amount ($)
- Notes
- Running Total

#### c. Time Investment Tracking
**Columns:**
- Date
- Task Category (Setup, Content Creation, Client Communication, etc.)
- Minutes Spent
- Notes
- Running Total (hours)

#### d. Calculated Metrics
- Current ROTI (Revenue / Total Hours)
- 7-Day ROTI
- 30-Day ROTI
- Week-over-Week Revenue Growth (%)
- Week-over-Week Time Efficiency Improvement (%)

#### e. Lead Indicators
- Custom fields based on experiment type
- Target values
- Current values
- Trend (improving/declining)

#### f. Status Log
- Date
- Status Update
- Key Metrics at Update
- Notable Changes
- Next Steps

### 3. Resource Allocation Tab

**Purpose:** Track and optimize how time is distributed across experiments.

**Columns:**
- Experiment ID
- Experiment Name
- Current Allocation (%)
- Current Allocation (minutes per day)
- Recommended Allocation (%)
- Allocation Change History
- Performance Impact of Previous Changes
- ROTI by Allocation Level (visualization)

**Features:**
- Pie chart showing current allocation distribution
- Historical allocation tracking
- Performance correlation analysis
- Recommendations based on current performance

### 4. Weekly Review Tab

**Purpose:** Document each weekly review session and decisions made.

**Columns:**
- Review Date
- Experiments Reviewed
- Key Observations
- Resource Allocation Decisions
- Experiment Adjustments
- New Experiments Considered
- Performance Trends
- Action Items

### 5. Settings & Thresholds Tab

**Purpose:** Define and adjust the decision criteria for experiments.

**Settings:**
- Continuation Threshold: ROTI > $5/hour by week 3
- Scaling Threshold: ROTI > $15/hour for 2 consecutive weeks
- Adjustment Threshold: ROTI between $2-5/hour by week 3
- Termination Threshold: ROTI < $2/hour by week 3
- Maximum Allocation to Single Experiment: 40%
- Minimum Allocation to Testing: 10%
- Review Cycle Frequency

## Implementation Guidelines

### Setup Instructions

1. Create a new Google Sheet titled "Nick the Great - Experiment Tracking"
2. Create the tabs as outlined above
3. Set up all formulas for automatic calculations
4. Configure conditional formatting for visual indicators
5. Set up data validation for consistent data entry
6. Share the document with all stakeholders
7. Create desktop shortcut for quick daily access

### Key Formulas

#### ROTI Calculation:
```
=IF(SUM(TimeInvested)=0,"No data",SUM(Revenue)/SUM(TimeInvested))
```

#### Week-over-Week Growth:
```
=IF(OR(ISBLANK(LastWeekRevenue),LastWeekRevenue=0),"N/A",(ThisWeekRevenue-LastWeekRevenue)/LastWeekRevenue)
```

#### Days Active:
```
=IF(ISBLANK(StartDate),"Not started",TODAY()-StartDate)
```

#### Performance vs. Threshold Indicator:
```
=IF(DaysActive<21,"Too early",IF(ROTI>ScalingThreshold,"Scaling",IF(ROTI>ContinuationThreshold,"Continue",IF(ROTI>AdjustmentThreshold,"Adjust","Terminate"))))
```

### Data Entry Protocols

1. **Revenue Entry:**
   - Enter revenue on the date it was earned (not when paid out)
   - Include source details for proper attribution
   - Attach screenshots of earnings in the "Notes" section when possible

2. **Time Tracking:**
   - Log time immediately after completing tasks
   - Categorize time accurately for analysis
   - Include brief description of what was accomplished
   - Round to nearest 5 minutes for simplicity

3. **Status Updates:**
   - Update experiment status weekly at minimum
   - Include both quantitative metrics and qualitative observations
   - Document all adjustment decisions and their rationale

## Usage Workflow

### Daily Quick Review (5 minutes)
1. Open spreadsheet
2. Check for new orders/revenue
3. Log previous day's time investment
4. Note any urgent issues or opportunities
5. Prioritize daily tasks based on data

### Weekly Comprehensive Review (30 minutes)
1. Update all metrics for the week
2. Calculate weekly averages and growth rates
3. Compare performance against thresholds
4. Make resource allocation decisions
5. Document review in Weekly Review tab
6. Update experiment status logs
7. Plan for upcoming week

### Monthly Strategic Review (60 minutes)
1. Analyze month-over-month trends
2. Evaluate overall portfolio performance
3. Consider new experiment candidates
4. Make major scaling or termination decisions
5. Refine decision thresholds based on learning
6. Update activeContext.md and progress.md

## Example Setup (For First Experiment)

### Summary Dashboard Initial Entry:
- Experiment ID: EXP001
- Experiment Name: AI-Powered Freelance Writing Services
- Status: Planning
- Current Phase: Setup
- Days Active: 0
- Total Revenue: $0
- Total Time Invested: 2 hours (initial setup)
- ROTI: $0/hour
- Growth Rate: N/A
- Resource Allocation: 30%

### EXP001 Tab Initial Setup:
- Lead Indicators to track:
  * Profile Views
  * Inquiry Rate
  * Conversion Rate
  * Average Order Value
- Task Categories:
  * Account Setup
  * Service Description Creation
  * Portfolio Development
  * Client Communication
  * Content Creation
  * Editing & Quality Control
  * Marketing & Optimization

This tracking spreadsheet will serve as the central nervous system for our parallel experimentation approach, enabling data-driven decisions and efficient resource allocation. When implemented correctly, it will provide complete visibility into the performance of all experiments and guide strategic decision-making throughout Phase 0 and beyond.

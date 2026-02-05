# Daily Health Score Calculation - Detailed Guide

## Overview

The daily health score is a comprehensive metric (0-100) that evaluates your hotel booking system's performance over the last 24 hours. It provides an at-a-glance assessment of system health and helps identify areas needing immediate attention.

---

## 📊 Overall Score Structure

The health score is calculated from **three main components**, each contributing a specific number of points:

| Component | Maximum Points | Weight |
|-----------|---------------|--------|
| **Booking Health** | 40 points | 40% |
| **User Health** | 30 points | 30% |
| **Revenue Health** | 30 points | 30% |
| **TOTAL** | **100 points** | **100%** |

---

## 1️⃣ Booking Health (40 points maximum)

This component evaluates the quality and quantity of bookings received in the last 24 hours.

### Point Breakdown:

#### **New Bookings Exist (20 points)**
- **Condition:** At least 1 new booking was made today
- **Points:** 20 if true, 0 if false
- **Why it matters:** Shows active customer interest and system usage

#### **Confirmation Rate (15 points maximum)**
The percentage of bookings that are confirmed vs cancelled/pending:

- **≥80% confirmation rate:** +15 points (Excellent)
- **≥60% confirmation rate:** +10 points (Good)
- **≥40% confirmation rate:** +5 points (Fair)
- **<40% confirmation rate:** +0 points (Poor)

**Formula:** `(confirmed_bookings / total_bookings) × 100`

**Why it matters:** High confirmation rates indicate customer commitment and booking quality

#### **Low Cancellation Rate (5 points)**
- **Condition:** Cancellation rate is less than 10%
- **Points:** 5 if true, 0 if false
- **Formula:** `(cancelled_bookings / total_bookings) × 100`
- **Why it matters:** Low cancellations mean stable revenue and satisfied customers

### Example Calculation:

**Scenario:** 10 new bookings today, 8 confirmed, 2 cancelled

- New bookings exist: **20 points** ✓
- Confirmation rate: 80% → **15 points** ✓
- Cancellation rate: 20% (>10%) → **0 points** ✗

**Booking Health Total: 35/40 points**

---

## 2️⃣ User Health (30 points maximum)

This component evaluates user acquisition and engagement over the last 24 hours.

### Point Breakdown:

#### **New Users Today (15 points)**
- **Condition:** At least 1 new user registered today
- **Points:** 15 if true, 0 if false
- **Why it matters:** Shows marketing effectiveness and platform growth

#### **Active Users Exist (10 points)**
- **Condition:** At least 1 user made a booking today
- **Points:** 10 if true, 0 if false
- **Why it matters:** Indicates user engagement and platform value

#### **Positive User Growth (5 points)**
- **Condition:** User growth rate is greater than 0%
- **Points:** 5 if true, 0 if false
- **Formula:** `(new_users / total_users) × 100`
- **Why it matters:** Shows expanding user base and platform adoption

### Example Calculation:

**Scenario:** 3 new users today, 2 active users, total 150 users

- New users exist: **15 points** ✓
- Active users exist: **10 points** ✓
- User growth: (3/150)×100 = 2% → **5 points** ✓

**User Health Total: 30/30 points**

---

## 3️⃣ Revenue Health (30 points maximum)

This component evaluates financial performance over the last 24 hours.

### Point Breakdown:

#### **Revenue Generated (20 points)**
- **Condition:** Total revenue from confirmed bookings is greater than $0
- **Points:** 20 if true, 0 if false
- **Why it matters:** Core business metric - revenue is essential for operations

#### **High Average Booking Value (10 points maximum)**
The average revenue per confirmed booking:

- **>$200 average:** +10 points (Premium bookings)
- **>$100 average:** +5 points (Standard bookings)
- **≤$100 average:** +0 points (Budget bookings)

**Formula:** `total_revenue / confirmed_bookings`

**Why it matters:** Higher booking values indicate premium room sales and better profitability

### Example Calculation:

**Scenario:** $1,600 revenue today from 8 confirmed bookings

- Revenue generated: **20 points** ✓
- Avg booking value: $1,600/8 = $200 → **10 points** ✓

**Revenue Health Total: 30/30 points**

---

## 🎯 Complete Example Calculation

Let's calculate a full daily health score:

### Daily Metrics:
- **Bookings:** 10 new bookings (8 confirmed, 2 cancelled)
- **Users:** 3 new users, 2 active users, 150 total users
- **Revenue:** $1,600 from confirmed bookings

### Component Scores:

**1. Booking Health (40 points max):**
- New bookings exist: 20 points ✓
- Confirmation rate: 80% → 15 points ✓
- Cancellation rate: 20% → 0 points ✗
- **Subtotal: 35/40 points**

**2. User Health (30 points max):**
- New users exist: 15 points ✓
- Active users exist: 10 points ✓
- Positive growth: 2% → 5 points ✓
- **Subtotal: 30/30 points**

**3. Revenue Health (30 points max):**
- Revenue generated: 20 points ✓
- Avg booking value: $200 → 10 points ✓
- **Subtotal: 30/30 points**

### **Total Health Score: 95/100** 🎉

---

## 📈 Health Status Levels

The total score determines the overall health status:

| Score Range | Status | Color | Meaning |
|-------------|--------|-------|---------|
| **80-100** | Excellent | 🟢 Green | System performing optimally |
| **60-79** | Good | 🔵 Blue | System healthy with minor issues |
| **40-59** | Fair | 🟡 Yellow | System needs attention |
| **0-39** | Needs Attention | 🔴 Red | System requires immediate action |

### Status Interpretations:

**🟢 Excellent (80-100):**
- Strong booking activity
- High confirmation rates
- Growing user base
- Healthy revenue
- **Action:** Maintain current strategies

**🔵 Good (60-79):**
- Decent performance with room for improvement
- Some metrics below target
- **Action:** Optimize underperforming areas

**🟡 Fair (40-59):**
- Significant issues in one or more areas
- Below acceptable thresholds
- **Action:** Investigate and address problems

**🔴 Needs Attention (0-39):**
- Critical issues requiring immediate action
- Multiple failing metrics
- **Action:** Emergency response needed

---

## 🔍 Interpreting Your Score

### High Score (80-100) Scenarios:

**Perfect Day (100 points):**
- Multiple new bookings with 80%+ confirmation
- Low cancellations (<10%)
- New user registrations
- Active user engagement
- Strong revenue with high booking values

**Near-Perfect (85-99 points):**
- Missing one or two minor criteria
- Still excellent overall performance

### Medium Score (60-79) Scenarios:

**Good But Improvable (70-79 points):**
- Good booking activity but moderate confirmation rates (60-79%)
- Or high confirmations but low booking values
- Room for optimization

**Decent Performance (60-69 points):**
- Meeting basic targets but not excelling
- Some areas need attention

### Low Score (40-59) Scenarios:

**Fair Performance (50-59 points):**
- Bookings exist but poor confirmation rates
- Or no new users despite bookings
- Needs investigation

**Concerning (40-49 points):**
- Multiple weak areas
- Immediate attention required

### Critical Score (0-39) Scenarios:

**Poor Performance (20-39 points):**
- Very few bookings or high cancellations
- Minimal user activity
- Low revenue

**Emergency (0-19 points):**
- No bookings or all cancelled
- No new users
- No revenue
- System may be down or experiencing critical issues

---

## 💡 Using the Health Score

### Daily Monitoring:

**Morning Review (8 AM):**
1. Check today's health score
2. Compare to yesterday's score
3. Identify any sudden drops
4. Take immediate action if score <60

### Trend Analysis:

**Weekly Pattern:**
- Track daily scores over 7 days
- Identify day-of-week patterns
- Adjust staffing/marketing accordingly

**Monthly Average:**
- Calculate average daily score
- Set improvement targets
- Measure progress over time

### Action Triggers:

| Score | Action Required |
|-------|----------------|
| <40 | **Emergency:** Investigate immediately |
| 40-59 | **High Priority:** Address within 24 hours |
| 60-79 | **Medium Priority:** Optimize within 1 week |
| 80-100 | **Low Priority:** Maintain and monitor |

---

## 🎯 Improving Your Health Score

### To Improve Booking Health:

1. **Increase confirmations:**
   - Simplify booking process
   - Send confirmation reminders
   - Offer booking incentives

2. **Reduce cancellations:**
   - Flexible cancellation policies
   - Clear communication
   - Address customer concerns quickly

### To Improve User Health:

1. **Attract new users:**
   - Marketing campaigns
   - Social media presence
   - Referral programs

2. **Increase engagement:**
   - Email newsletters
   - Special offers
   - Loyalty programs

### To Improve Revenue Health:

1. **Increase booking values:**
   - Promote premium rooms
   - Upsell amenities
   - Package deals

2. **Optimize pricing:**
   - Dynamic pricing strategies
   - Seasonal adjustments
   - Competitive analysis

---

## 📊 Code Implementation

The health score is calculated in `backend/performance_metrics.py`:

```python
def calculate_health_score(self, report_data):
    """
    Calculate overall system health score (0-100)
    """
    booking_metrics = report_data["booking_metrics"]
    user_metrics = report_data["user_metrics"]
    revenue_metrics = report_data["revenue_metrics"]
    
    # Booking Health (40 points max)
    booking_score = 0
    if booking_metrics["new_bookings"] > 0:
        booking_score += 20  # Has new bookings
    
    confirmation_rate = booking_metrics["confirmation_rate"]
    if confirmation_rate >= 80:
        booking_score += 15
    elif confirmation_rate >= 60:
        booking_score += 10
    elif confirmation_rate >= 40:
        booking_score += 5
    
    if booking_metrics["cancellation_rate"] < 10:
        booking_score += 5  # Low cancellation rate
    
    # User Health (30 points max)
    user_score = 0
    if user_metrics["new_users"] > 0:
        user_score += 15  # Has new users
    
    if user_metrics["active_users"] > 0:
        user_score += 10  # Has active users
    
    if user_metrics["user_growth_rate"] > 0:
        user_score += 5  # Positive growth
    
    # Revenue Health (30 points max)
    revenue_score = 0
    if revenue_metrics["total_revenue"] > 0:
        revenue_score += 20  # Has revenue
    
    avg_value = revenue_metrics["avg_booking_value"]
    if avg_value > 200:
        revenue_score += 10
    elif avg_value > 100:
        revenue_score += 5
    
    # Total Score
    total_score = booking_score + user_score + revenue_score
    
    # Determine status
    if total_score >= 80:
        status = "Excellent"
        color = "excellent"
    elif total_score >= 60:
        status = "Good"
        color = "good"
    elif total_score >= 40:
        status = "Fair"
        color = "fair"
    else:
        status = "Needs Attention"
        color = "poor"
    
    return {
        "total_score": total_score,
        "status": status,
        "color": color,
        "booking_score": booking_score,
        "user_score": user_score,
        "revenue_score": revenue_score
    }
```

---

## 📋 Quick Reference Card

### Scoring Checklist:

**Booking Health (40 pts):**
- [ ] New bookings today? (+20)
- [ ] Confirmation rate ≥80%? (+15)
- [ ] Confirmation rate ≥60%? (+10)
- [ ] Confirmation rate ≥40%? (+5)
- [ ] Cancellation rate <10%? (+5)

**User Health (30 pts):**
- [ ] New users today? (+15)
- [ ] Active users today? (+10)
- [ ] Positive user growth? (+5)

**Revenue Health (30 pts):**
- [ ] Revenue generated? (+20)
- [ ] Avg booking value >$200? (+10)
- [ ] Avg booking value >$100? (+5)

**Status:**
- 80-100: Excellent 🟢
- 60-79: Good 🔵
- 40-59: Fair 🟡
- 0-39: Needs Attention 🔴

---

## 🎓 Best Practices

### Daily Review Process:

1. **8:00 AM - Check Report**
   - Open daily HTML report
   - Note health score and status
   - Review component breakdown

2. **8:15 AM - Analyze Trends**
   - Compare to yesterday
   - Look for patterns
   - Identify anomalies

3. **8:30 AM - Take Action**
   - Address critical issues (<40)
   - Plan improvements (40-79)
   - Maintain strategies (80-100)

4. **End of Day - Document**
   - Record actions taken
   - Note results
   - Plan for tomorrow

### Weekly Review:

- Calculate average daily score
- Identify best and worst days
- Analyze day-of-week patterns
- Adjust strategies accordingly

### Monthly Review:

- Track monthly average score
- Compare to previous months
- Set improvement goals
- Celebrate achievements

---

## 📞 Support and Troubleshooting

### Common Issues:

**Score is always 0:**
- Check database connection
- Verify bookings exist
- Ensure date range is correct

**Score seems inaccurate:**
- Review raw metrics in JSON report
- Verify calculation logic
- Check for data quality issues

**Score fluctuates wildly:**
- Normal for new systems
- Stabilizes with more data
- Focus on weekly averages

### Getting Help:

1. Review this guide thoroughly
2. Check `AUTOMATED_REPORTING.md` for system details
3. Examine JSON reports for raw data
4. Verify database connectivity
5. Test with manual report generation

---

## 📚 Related Documentation

- **AUTOMATED_REPORTING.md** - Complete reporting system documentation
- **performance_metrics.py** - Metrics collection implementation
- **daily_report_automation.py** - Daily report generation script
- **report_generator.py** - Report formatting and HTML generation

---

## 📝 Summary

The daily health score is a **powerful, actionable metric** that:

✅ Provides instant assessment of daily performance  
✅ Combines multiple KPIs into one number  
✅ Uses weighted components for balanced evaluation  
✅ Offers clear status levels for quick interpretation  
✅ Enables trend tracking and pattern identification  
✅ Triggers appropriate actions based on score  
✅ Helps prioritize improvement efforts  

**By monitoring your daily health score, you can quickly identify issues, celebrate successes, and maintain optimal system performance!**

---

*Last Updated: February 5, 2026*  
*Version: 1.0*  
*Part of: Luxury Haven Hotel Automated Reporting System*

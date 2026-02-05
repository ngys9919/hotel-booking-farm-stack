# Automated Weekly Performance Reporting System

## Overview

The Luxury Haven Hotel Booking System now includes a comprehensive automated performance reporting system that generates detailed weekly reports with key performance indicators (KPIs), visualizations, and health scores.

---

## 📊 Features

### Metrics Collected

**User Metrics:**
- Total users
- New users (weekly)
- Active users (users who made bookings)
- Admin vs regular users breakdown
- User growth rate

**Booking Metrics:**
- Total bookings
- New bookings (weekly)
- Confirmed, cancelled, and pending bookings
- Confirmation and cancellation rates
- Average guests per booking
- Average nights per booking

**Revenue Metrics:**
- Total revenue (confirmed bookings)
- Average booking value
- Potential revenue (including cancelled)
- Lost revenue (from cancellations)
- Revenue by room type
- Top performing rooms

**Room Metrics:**
- Total available rooms
- Average room price
- Min and max room prices
- Room categories and pricing

**Health Score:**
- Overall system health (0-100)
- Booking health score (0-40 points)
- User health score (0-30 points)
- Revenue health score (0-30 points)
- Status: Excellent, Good, Fair, or Needs Attention

---

## 🗂️ System Components

### 1. Performance Metrics Collection (`performance_metrics.py`)

The core module that collects and analyzes all performance data from the database.

**Key Classes:**
- `PerformanceMetrics`: Main class for collecting metrics
  - `collect_user_metrics()`: Gathers user-related KPIs
  - `collect_booking_metrics()`: Gathers booking-related KPIs
  - `collect_revenue_metrics()`: Gathers revenue-related KPIs
  - `collect_room_metrics()`: Gathers room-related KPIs
  - `generate_weekly_report()`: Generates complete report data
  - `calculate_health_score()`: Calculates system health score
  - `save_report()`: Saves report to JSON file

**Usage:**
```python
from performance_metrics import PerformanceMetrics
from database import users_collection, bookings_collection, rooms_collection

metrics = PerformanceMetrics(users_collection, bookings_collection, rooms_collection)
report_data = metrics.generate_weekly_report()
json_path = metrics.save_report(report_data)
```

### 2. Report Generator (`report_generator.py`)

Generates beautifully formatted HTML reports and email summaries.

**Key Classes:**
- `ReportGenerator`: Main class for generating reports
  - `generate_html_report()`: Creates HTML report with visualizations
  - `generate_summary_email()`: Creates email-friendly summary

**Features:**
- Professional HTML design with gradient backgrounds
- Responsive layout for all devices
- Color-coded health scores
- Interactive metric cards
- Data tables for top performers
- Print-friendly styling

**Usage:**
```python
from report_generator import ReportGenerator

generator = ReportGenerator()
html_path = generator.generate_html_report(report_data)
email_content = generator.generate_summary_email(report_data)
```

### 3. Weekly Report Automation (`weekly_report_automation.py`)

Main automation script that orchestrates the entire reporting process.

**Process Flow:**
1. Collect performance metrics from database
2. Save JSON report with raw data
3. Generate HTML report with visualizations
4. Generate email summary
5. Display summary in console
6. Report completion status

**Usage:**
```bash
# Run manually
python3.11 /home/ubuntu/hotel-booking-app/backend/weekly_report_automation.py

# Or make executable and run
chmod +x /home/ubuntu/hotel-booking-app/backend/weekly_report_automation.py
./weekly_report_automation.py
```

---

## ⏰ Automated Schedule

The system is configured to run automatically every **Monday at 9:00 AM**.

**Schedule Details:**
- **Frequency:** Weekly (every Monday)
- **Time:** 9:00 AM (server timezone)
- **Cron Expression:** `0 0 9 * * 1`
- **Task Name:** Luxury Haven Hotel Weekly Performance Report

**What Happens Automatically:**
1. Script runs at scheduled time
2. Collects data from past 7 days
3. Generates all report files
4. Saves to reports directory
5. Can be configured to send email notifications

---

## 📁 Generated Files

All reports are saved to: `/home/ubuntu/hotel-booking-app/reports/`

**File Types:**

1. **JSON Report** (`performance_report_YYYYMMDD_HHMMSS.json`)
   - Raw data in JSON format
   - Complete metrics and calculations
   - Suitable for programmatic access
   - Size: ~1-2 KB

2. **HTML Report** (`weekly_report_YYYYMMDD_HHMMSS.html`)
   - Beautiful visual report
   - Interactive metric cards
   - Data tables and charts
   - Print-friendly layout
   - Size: ~10-15 KB

3. **Email Summary** (`email_summary_YYYYMMDD_HHMMSS.txt`)
   - Text-based summary
   - Key highlights only
   - Email-friendly format
   - Size: ~1 KB

**File Naming Convention:**
- Timestamp format: `YYYYMMDD_HHMMSS`
- Example: `weekly_report_20260205_112359.html`

---

## 🎨 HTML Report Features

The generated HTML report includes:

### Visual Design
- **Header:** Gradient blue background with hotel logo and report period
- **Health Score Card:** Color-coded score display (green/blue/yellow/red)
- **Metric Cards:** Grid layout with hover effects
- **Data Tables:** Professional tables for top performers
- **Footer:** Timestamp and copyright information

### Sections
1. **System Health Score:** Overall health (0-100) with status
2. **User Metrics:** Total, new, active users with growth rate
3. **Booking Metrics:** Bookings, confirmations, cancellations
4. **Revenue Metrics:** Total revenue, avg value, top rooms
5. **Room Metrics:** Room inventory and pricing
6. **Health Score Breakdown:** Component scores

### Responsive Design
- Desktop: 3-column grid layout
- Tablet: 2-column grid layout
- Mobile: Single column layout
- Print: Optimized for printing

---

## 📧 Email Summary Format

The email summary provides a concise text-based overview:

```
🏨 Luxury Haven Hotel - Weekly Performance Report
============================================================

Report Period: January 29, 2026 - February 05, 2026

SYSTEM HEALTH SCORE: 85/100 - Excellent

KEY HIGHLIGHTS:
============================================================

👥 USER METRICS:
   • Total Users: 150
   • New Users: 25 (+20%)
   • Active Users: 45

📅 BOOKING METRICS:
   • Total Bookings: 200
   • New Bookings: 35
   • Confirmed: 30 (85.7%)
   • Cancelled: 5 (14.3%)

💰 REVENUE METRICS:
   • Total Revenue: $15,250.00
   • Avg Booking Value: $508.33
   • Potential Revenue: $17,500.00
   • Lost Revenue: $2,250.00

🏆 TOP PERFORMING ROOMS:
   1. Presidential Penthouse: $5,999.92
   2. Family Garden Suite: $4,199.88
   3. Deluxe Ocean View Suite: $2,999.90

============================================================
```

---

## 🔧 Configuration

### Database Connection

The system uses the database collections from `database.py`:
- `users_collection`
- `bookings_collection`
- `rooms_collection`

**For MongoDB Atlas:**
Update `.env` file with your connection string:
```
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=hotel_booking_db
```

**For Mock Database:**
The system automatically uses in-memory mock data if MongoDB is not configured.

### Report Period

Default: Last 7 days (weekly)

To change the period, modify in `performance_metrics.py`:
```python
def get_date_range(self, days: int = 7):  # Change 7 to desired days
    ...
```

### Schedule Modification

To change the schedule:
1. Update the cron expression in the schedule configuration
2. Common schedules:
   - Daily at 9 AM: `0 0 9 * * *`
   - Weekly on Monday at 9 AM: `0 0 9 * * 1`
   - Monthly on 1st at 9 AM: `0 0 9 1 * *`

---

## 📊 Health Score Calculation

The health score (0-100) is calculated based on three components:

### Booking Health (40 points)
- New bookings exist: +20 points
- Confirmation rate ≥80%: +15 points
- Confirmation rate ≥60%: +10 points
- Confirmation rate ≥40%: +5 points
- Cancellation rate <10%: +5 points

### User Health (30 points)
- New users exist: +15 points
- Active users exist: +10 points
- Positive user growth: +5 points

### Revenue Health (30 points)
- Revenue generated: +20 points
- Avg booking value >$200: +10 points
- Avg booking value >$100: +5 points

### Status Levels
- **Excellent:** 80-100 points (Green)
- **Good:** 60-79 points (Blue)
- **Fair:** 40-59 points (Yellow)
- **Needs Attention:** 0-39 points (Red)

---

## 🚀 Usage Examples

### Manual Report Generation

```bash
# Navigate to backend directory
cd /home/ubuntu/hotel-booking-app/backend

# Run the automation script
python3.11 weekly_report_automation.py

# Check generated reports
ls -lh /home/ubuntu/hotel-booking-app/reports/
```

### View HTML Report

```bash
# Open in browser (if running locally)
open /home/ubuntu/hotel-booking-app/reports/weekly_report_*.html

# Or serve via HTTP server
cd /home/ubuntu/hotel-booking-app/reports
python3 -m http.server 8080
# Then visit: http://localhost:8080/weekly_report_*.html
```

### Programmatic Access

```python
import json

# Load JSON report
with open('/home/ubuntu/hotel-booking-app/reports/performance_report_*.json', 'r') as f:
    report = json.load(f)

# Access metrics
print(f"Health Score: {report['health_score']['total_score']}")
print(f"Total Revenue: ${report['revenue_metrics']['total_revenue']}")
print(f"New Bookings: {report['booking_metrics']['new_bookings']}")
```

---

## 🔍 Troubleshooting

### Issue: No data in reports

**Cause:** Empty database or mock database being used

**Solution:**
1. Ensure MongoDB is properly configured in `.env`
2. Check database connection
3. Verify collections have data
4. Run a test booking to populate data

### Issue: Script fails to run

**Cause:** Missing dependencies or permissions

**Solution:**
```bash
# Install dependencies
cd /home/ubuntu/hotel-booking-app/backend
sudo pip3 install -r requirements.txt

# Make script executable
chmod +x weekly_report_automation.py

# Check Python version
python3.11 --version
```

### Issue: Reports not generating

**Cause:** Directory permissions or disk space

**Solution:**
```bash
# Create reports directory
mkdir -p /home/ubuntu/hotel-booking-app/reports

# Set permissions
chmod 755 /home/ubuntu/hotel-booking-app/reports

# Check disk space
df -h
```

### Issue: Schedule not running

**Cause:** Cron service not active or incorrect schedule

**Solution:**
1. Verify the schedule was created successfully
2. Check the cron expression is correct
3. Test manual execution first
4. Check system logs for errors

---

## 📈 Future Enhancements

Potential improvements for the reporting system:

1. **Email Integration**
   - Automatic email delivery to stakeholders
   - SMTP configuration
   - HTML email templates

2. **Advanced Visualizations**
   - Charts and graphs (Chart.js integration)
   - Trend analysis over multiple weeks
   - Comparative metrics

3. **Custom Reports**
   - User-defined metrics
   - Custom date ranges
   - Filtered reports by room type

4. **Real-time Dashboard**
   - Live metrics display
   - WebSocket updates
   - Interactive charts

5. **Export Options**
   - PDF generation
   - Excel spreadsheets
   - CSV data export

6. **Alerting System**
   - Threshold-based alerts
   - Slack/Discord notifications
   - SMS alerts for critical issues

7. **Historical Analysis**
   - Month-over-month comparisons
   - Year-over-year trends
   - Seasonal patterns

---

## 📝 Best Practices

1. **Review Reports Regularly**
   - Check health score weekly
   - Identify trends and patterns
   - Take action on low scores

2. **Monitor Key Metrics**
   - Confirmation rate (target: >80%)
   - Cancellation rate (target: <10%)
   - User growth rate (target: positive)
   - Revenue per booking (target: >$200)

3. **Data Quality**
   - Ensure accurate booking data
   - Verify user information
   - Validate price calculations

4. **Report Retention**
   - Archive old reports monthly
   - Keep last 12 weeks for analysis
   - Backup important reports

5. **Performance Optimization**
   - Run during off-peak hours
   - Optimize database queries
   - Clean up old report files

---

## 🎯 Success Metrics

Track these KPIs to measure system performance:

**User Growth:**
- Target: 10-20% weekly growth
- Monitor: New user registrations
- Action: Marketing campaigns if growth slows

**Booking Confirmation:**
- Target: >80% confirmation rate
- Monitor: Cancellation reasons
- Action: Improve booking process if rate drops

**Revenue Growth:**
- Target: Consistent week-over-week growth
- Monitor: Average booking value
- Action: Promote higher-value rooms

**System Health:**
- Target: >80 health score (Excellent)
- Monitor: Component scores
- Action: Address weak areas immediately

---

## 📞 Support

For issues or questions about the automated reporting system:

1. Check this documentation first
2. Review the troubleshooting section
3. Check system logs for errors
4. Test manual execution
5. Verify database connectivity

---

## 📄 Summary

The automated weekly performance reporting system provides:

✅ **Comprehensive Metrics** - Users, bookings, revenue, rooms  
✅ **Beautiful Reports** - HTML with visualizations  
✅ **Health Monitoring** - 0-100 score with status  
✅ **Automatic Execution** - Weekly on Mondays at 9 AM  
✅ **Multiple Formats** - JSON, HTML, and email  
✅ **Easy Access** - Saved to reports directory  
✅ **Actionable Insights** - Identify trends and issues  

**The system is ready to use and will generate reports automatically every week!**

---

*Last Updated: February 5, 2026*  
*Version: 1.0*

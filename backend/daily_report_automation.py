#!/usr/bin/env python3
"""
Daily Report Automation Script for Luxury Haven Hotel
Automatically generates daily performance reports with 24-hour metrics
"""

import sys
import os
from datetime import datetime

# Add backend directory to path
sys.path.insert(0, '/home/ubuntu/hotel-booking-app/backend')

from performance_metrics import PerformanceMetrics
from report_generator import ReportGenerator
from database import rooms_collection, bookings_collection, users_collection


def generate_daily_report():
    """
    Main function to generate daily performance report
    """
    print("=" * 70)
    print("🏨 Luxury Haven Hotel - Daily Report Generation")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Step 1: Collect metrics for last 24 hours
        print("Step 1: Collecting daily performance metrics (last 24 hours)...")
        metrics_collector = PerformanceMetrics(
            users_collection=users_collection,
            bookings_collection=bookings_collection,
            rooms_collection=rooms_collection
        )
        
        # Override the date range to get last 24 hours (1 day)
        start_date, end_date = metrics_collector.get_date_range(days=1)
        
        # Collect metrics
        report_data = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "period_start": start_date.isoformat(),
                "period_end": end_date.isoformat(),
                "period_days": 1,
                "report_type": "daily"
            },
            "user_metrics": metrics_collector.collect_user_metrics(start_date, end_date),
            "booking_metrics": metrics_collector.collect_booking_metrics(start_date, end_date),
            "revenue_metrics": metrics_collector.collect_revenue_metrics(start_date, end_date),
            "room_metrics": metrics_collector.collect_room_metrics()
        }
        
        # Calculate health score
        report_data["health_score"] = metrics_collector.calculate_health_score(report_data)
        
        print("✓ Daily metrics collected successfully")
        print()
        
        # Step 2: Save JSON report
        print("Step 2: Saving daily JSON report...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"daily_report_{timestamp}.json"
        json_path = metrics_collector.save_report(report_data, json_filename)
        print(f"✓ JSON report saved: {json_path}")
        print()
        
        # Step 3: Generate HTML report (with daily-specific styling)
        print("Step 3: Generating daily HTML report...")
        report_gen = ReportGenerator()
        html_path = generate_daily_html_report(report_gen, report_data)
        print(f"✓ HTML report generated: {html_path}")
        print()
        
        # Step 4: Generate email summary
        print("Step 4: Generating daily email summary...")
        email_content = generate_daily_email_summary(report_data)
        
        # Save email content
        email_path = f"/home/ubuntu/hotel-booking-app/reports/daily_email_summary_{timestamp}.txt"
        with open(email_path, 'w') as f:
            f.write(email_content)
        print(f"✓ Email summary saved: {email_path}")
        print()
        
        # Step 5: Display summary
        print("=" * 70)
        print("📊 DAILY REPORT SUMMARY")
        print("=" * 70)
        print(email_content)
        print()
        
        # Step 6: Report completion
        print("=" * 70)
        print("✅ DAILY REPORT GENERATION COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("Generated files:")
        print(f"  • JSON Report: {json_path}")
        print(f"  • HTML Report: {html_path}")
        print(f"  • Email Summary: {email_path}")
        print()
        print(f"Health Score: {report_data['health_score']['total_score']}/100 - {report_data['health_score']['status']}")
        print()
        
        return {
            "success": True,
            "json_report": json_path,
            "html_report": html_path,
            "email_summary": email_path,
            "health_score": report_data['health_score']['total_score']
        }
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }


def generate_daily_html_report(report_gen, report_data):
    """Generate daily-specific HTML report"""
    metadata = report_data["report_metadata"]
    user_metrics = report_data["user_metrics"]
    booking_metrics = report_data["booking_metrics"]
    revenue_metrics = report_data["revenue_metrics"]
    room_metrics = report_data["room_metrics"]
    health_score = report_data["health_score"]
    
    # Format dates
    period_start = datetime.fromisoformat(metadata["period_start"]).strftime("%B %d, %Y at %I:%M %p")
    period_end = datetime.fromisoformat(metadata["period_end"]).strftime("%B %d, %Y at %I:%M %p")
    generated_at = datetime.fromisoformat(metadata["generated_at"]).strftime("%B %d, %Y at %I:%M %p")
    report_date = datetime.fromisoformat(metadata["period_end"]).strftime("%B %d, %Y")
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luxury Haven Hotel - Daily Performance Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 36px;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            font-size: 18px;
            opacity: 0.9;
            margin-bottom: 10px;
        }}
        
        .header .daily-badge {{
            background: rgba(255,255,255,0.2);
            display: inline-block;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 15px;
        }}
        
        .header .period {{
            font-size: 16px;
            opacity: 0.8;
            background: rgba(255,255,255,0.1);
            display: inline-block;
            padding: 10px 20px;
            border-radius: 20px;
        }}
        
        .health-score {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .health-score.good {{
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        }}
        
        .health-score.fair {{
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        }}
        
        .health-score.poor {{
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        }}
        
        .health-score h2 {{
            font-size: 24px;
            margin-bottom: 15px;
        }}
        
        .health-score .score {{
            font-size: 72px;
            font-weight: 700;
            margin: 10px 0;
        }}
        
        .health-score .status {{
            font-size: 20px;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            font-size: 28px;
            color: #f59e0b;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #fbbf24;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }}
        
        .metric-card .label {{
            font-size: 14px;
            color: #92400e;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
            font-weight: 600;
        }}
        
        .metric-card .value {{
            font-size: 36px;
            font-weight: 700;
            color: #d97706;
            margin-bottom: 5px;
        }}
        
        .metric-card .change {{
            font-size: 14px;
            color: #10b981;
            font-weight: 600;
        }}
        
        .metric-card .change.negative {{
            color: #ef4444;
        }}
        
        .daily-highlight {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            border-left: 5px solid #f59e0b;
        }}
        
        .daily-highlight h3 {{
            color: #d97706;
            margin-bottom: 10px;
        }}
        
        .table-container {{
            overflow-x: auto;
            margin: 20px 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        th {{
            background: #f59e0b;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 15px;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        tr:last-child td {{
            border-bottom: none;
        }}
        
        tr:hover {{
            background: #fef3c7;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .badge.success {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .badge.warning {{
            background: #fef3c7;
            color: #92400e;
        }}
        
        .badge.danger {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .footer {{
            background: #fef3c7;
            padding: 30px;
            text-align: center;
            color: #92400e;
            font-size: 14px;
        }}
        
        .footer .timestamp {{
            margin-top: 10px;
            font-size: 12px;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🏨 Luxury Haven Hotel</h1>
            <div class="subtitle">Daily Performance Report</div>
            <div class="daily-badge">📅 24-HOUR SNAPSHOT</div>
            <div class="period">
                {report_date}
            </div>
        </div>
        
        <!-- Health Score -->
        <div class="health-score {health_score['color']}">
            <h2>Daily Health Score</h2>
            <div class="score">{health_score['total_score']}/100</div>
            <div class="status">{health_score['status']}</div>
        </div>
        
        <!-- Content -->
        <div class="content">
            <!-- Daily Highlight -->
            <div class="daily-highlight">
                <h3>📊 Today's Highlights</h3>
                <p><strong>New Bookings:</strong> {booking_metrics['new_bookings']} | 
                   <strong>New Users:</strong> {user_metrics['new_users']} | 
                   <strong>Revenue:</strong> ${revenue_metrics['total_revenue']:,.2f}</p>
            </div>
            
            <!-- User Metrics -->
            <div class="section">
                <h2>👥 User Activity (Last 24 Hours)</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="label">Total Users</div>
                        <div class="value">{user_metrics['total_users']}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">New Users Today</div>
                        <div class="value">{user_metrics['new_users']}</div>
                        <div class="change">+{user_metrics['user_growth_rate']}% growth</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Active Users</div>
                        <div class="value">{user_metrics['active_users']}</div>
                    </div>
                </div>
            </div>
            
            <!-- Booking Metrics -->
            <div class="section">
                <h2>📅 Booking Activity (Last 24 Hours)</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="label">New Bookings</div>
                        <div class="value">{booking_metrics['new_bookings']}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Confirmed</div>
                        <div class="value">{booking_metrics['confirmed_bookings']}</div>
                        <div class="change">{booking_metrics['confirmation_rate']}% rate</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Cancelled</div>
                        <div class="value">{booking_metrics['cancelled_bookings']}</div>
                        <div class="change negative">{booking_metrics['cancellation_rate']}% rate</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Avg Nights</div>
                        <div class="value">{booking_metrics['avg_nights_per_booking']}</div>
                    </div>
                </div>
            </div>
            
            <!-- Revenue Metrics -->
            <div class="section">
                <h2>💰 Revenue (Last 24 Hours)</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="label">Today's Revenue</div>
                        <div class="value">${revenue_metrics['total_revenue']:,.2f}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Avg Booking Value</div>
                        <div class="value">${revenue_metrics['avg_booking_value']:,.2f}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Potential Revenue</div>
                        <div class="value">${revenue_metrics['potential_revenue']:,.2f}</div>
                    </div>
                </div>
                
                <!-- Top Performing Rooms Today -->
                <h3 style="margin-top: 30px; margin-bottom: 15px; color: #f59e0b;">Top Rooms Today</h3>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Room</th>
                                <th>Revenue</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
"""
    
    # Add top performing rooms
    for idx, room_data in enumerate(revenue_metrics['top_performing_rooms'], 1):
        badge_class = "success" if idx == 1 else "warning" if idx == 2 else "danger"
        html_content += f"""
                            <tr>
                                <td><strong>#{idx}</strong></td>
                                <td>{room_data['room']}</td>
                                <td>${room_data['revenue']:,.2f}</td>
                                <td><span class="badge {badge_class}">Top {idx}</span></td>
                            </tr>
"""
    
    html_content += """
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <div>© 2026 Luxury Haven Hotel - Automated Daily Report</div>
            <div class="timestamp">Generated on """ + generated_at + """</div>
        </div>
    </div>
</body>
</html>
"""
    
    # Save HTML file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"daily_report_{timestamp}.html"
    filepath = os.path.join("/home/ubuntu/hotel-booking-app/reports", filename)
    
    with open(filepath, 'w') as f:
        f.write(html_content)
    
    return filepath


def generate_daily_email_summary(report_data):
    """Generate daily email summary"""
    metadata = report_data["report_metadata"]
    user_metrics = report_data["user_metrics"]
    booking_metrics = report_data["booking_metrics"]
    revenue_metrics = report_data["revenue_metrics"]
    health_score = report_data["health_score"]
    
    report_date = datetime.fromisoformat(metadata["period_end"]).strftime("%B %d, %Y")
    
    email_content = f"""
🏨 Luxury Haven Hotel - Daily Performance Report
{'=' * 60}

Report Date: {report_date} (Last 24 Hours)

DAILY HEALTH SCORE: {health_score['total_score']}/100 - {health_score['status']}

TODAY'S HIGHLIGHTS:
{'=' * 60}

👥 USER ACTIVITY:
   • Total Users: {user_metrics['total_users']}
   • New Users Today: {user_metrics['new_users']} (+{user_metrics['user_growth_rate']}%)
   • Active Users: {user_metrics['active_users']}

📅 BOOKING ACTIVITY:
   • New Bookings: {booking_metrics['new_bookings']}
   • Confirmed: {booking_metrics['confirmed_bookings']} ({booking_metrics['confirmation_rate']}%)
   • Cancelled: {booking_metrics['cancelled_bookings']} ({booking_metrics['cancellation_rate']}%)
   • Avg Nights: {booking_metrics['avg_nights_per_booking']}

💰 REVENUE:
   • Today's Revenue: ${revenue_metrics['total_revenue']:,.2f}
   • Avg Booking Value: ${revenue_metrics['avg_booking_value']:,.2f}
   • Potential Revenue: ${revenue_metrics['potential_revenue']:,.2f}

🏆 TOP ROOMS TODAY:
"""
    
    for idx, room_data in enumerate(revenue_metrics['top_performing_rooms'], 1):
        email_content += f"   {idx}. {room_data['room']}: ${room_data['revenue']:,.2f}\n"
    
    email_content += f"""
{'=' * 60}

For detailed report with visualizations, check the HTML report.

This is an automated daily report generated by Luxury Haven Hotel Performance System.
"""
    
    return email_content


if __name__ == "__main__":
    result = generate_daily_report()
    
    # Exit with appropriate code
    sys.exit(0 if result["success"] else 1)

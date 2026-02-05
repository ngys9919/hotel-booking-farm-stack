"""
Weekly Performance Report Generator for Luxury Haven Hotel
Generates beautiful HTML and PDF reports with visualizations
"""

from datetime import datetime
from typing import Dict, Any
import json
import os


class ReportGenerator:
    """Generates formatted performance reports with visualizations"""
    
    def __init__(self):
        """Initialize report generator"""
        self.report_dir = "/home/ubuntu/hotel-booking-app/reports"
        os.makedirs(self.report_dir, exist_ok=True)
    
    def generate_html_report(self, report_data: Dict[str, Any]) -> str:
        """
        Generate HTML report with visualizations
        
        Args:
            report_data: Report data dictionary from PerformanceMetrics
        
        Returns:
            Path to generated HTML file
        """
        metadata = report_data["report_metadata"]
        user_metrics = report_data["user_metrics"]
        booking_metrics = report_data["booking_metrics"]
        revenue_metrics = report_data["revenue_metrics"]
        room_metrics = report_data["room_metrics"]
        health_score = report_data["health_score"]
        
        # Format dates
        period_start = datetime.fromisoformat(metadata["period_start"]).strftime("%B %d, %Y")
        period_end = datetime.fromisoformat(metadata["period_end"]).strftime("%B %d, %Y")
        generated_at = datetime.fromisoformat(metadata["generated_at"]).strftime("%B %d, %Y at %I:%M %p")
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luxury Haven Hotel - Weekly Performance Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
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
            margin-bottom: 20px;
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
            color: #1e3a8a;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #3b82f6;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
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
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }}
        
        .metric-card .value {{
            font-size: 36px;
            font-weight: 700;
            color: #1e3a8a;
            margin-bottom: 5px;
        }}
        
        .metric-card .change {{
            font-size: 14px;
            color: #10b981;
        }}
        
        .metric-card .change.negative {{
            color: #ef4444;
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
            background: #1e3a8a;
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
            background: #f9fafb;
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
            background: #f3f4f6;
            padding: 30px;
            text-align: center;
            color: #6b7280;
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
            <div class="subtitle">Weekly Performance Report</div>
            <div class="period">
                {period_start} - {period_end}
            </div>
        </div>
        
        <!-- Health Score -->
        <div class="health-score {health_score['color']}">
            <h2>System Health Score</h2>
            <div class="score">{health_score['total_score']}/100</div>
            <div class="status">{health_score['status']}</div>
        </div>
        
        <!-- Content -->
        <div class="content">
            <!-- User Metrics -->
            <div class="section">
                <h2>👥 User Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="label">Total Users</div>
                        <div class="value">{user_metrics['total_users']}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">New Users</div>
                        <div class="value">{user_metrics['new_users']}</div>
                        <div class="change">+{user_metrics['user_growth_rate']}% growth</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Active Users</div>
                        <div class="value">{user_metrics['active_users']}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Admin Users</div>
                        <div class="value">{user_metrics['admin_users']}</div>
                    </div>
                </div>
            </div>
            
            <!-- Booking Metrics -->
            <div class="section">
                <h2>📅 Booking Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="label">Total Bookings</div>
                        <div class="value">{booking_metrics['total_bookings']}</div>
                    </div>
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
                        <div class="label">Avg Guests</div>
                        <div class="value">{booking_metrics['avg_guests_per_booking']}</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Avg Nights</div>
                        <div class="value">{booking_metrics['avg_nights_per_booking']}</div>
                    </div>
                </div>
            </div>
            
            <!-- Revenue Metrics -->
            <div class="section">
                <h2>💰 Revenue Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="label">Total Revenue</div>
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
                    <div class="metric-card">
                        <div class="label">Lost Revenue</div>
                        <div class="value">${revenue_metrics['lost_revenue']:,.2f}</div>
                    </div>
                </div>
                
                <!-- Top Performing Rooms -->
                <h3 style="margin-top: 30px; margin-bottom: 15px; color: #1e3a8a;">Top Performing Rooms</h3>
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
            
            <!-- Room Metrics -->
            <div class="section">
                <h2>🏠 Room Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="label">Total Rooms</div>
                        <div class="value">""" + str(room_metrics['total_rooms']) + """</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Avg Room Price</div>
                        <div class="value">$""" + f"{room_metrics['avg_room_price']:,.2f}" + """</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Min Price</div>
                        <div class="value">$""" + f"{room_metrics['min_room_price']:,.2f}" + """</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Max Price</div>
                        <div class="value">$""" + f"{room_metrics['max_room_price']:,.2f}" + """</div>
                    </div>
                </div>
            </div>
            
            <!-- Health Score Breakdown -->
            <div class="section">
                <h2>📊 Health Score Breakdown</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="label">Booking Health</div>
                        <div class="value">""" + str(health_score['booking_score']) + """/40</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">User Health</div>
                        <div class="value">""" + str(health_score['user_score']) + """/30</div>
                    </div>
                    <div class="metric-card">
                        <div class="label">Revenue Health</div>
                        <div class="value">""" + str(health_score['revenue_score']) + """/30</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <div>© 2026 Luxury Haven Hotel - Automated Performance Report</div>
            <div class="timestamp">Generated on """ + generated_at + """</div>
        </div>
    </div>
</body>
</html>
"""
        
        # Save HTML file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"weekly_report_{timestamp}.html"
        filepath = os.path.join(self.report_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return filepath
    
    def generate_summary_email(self, report_data: Dict[str, Any]) -> str:
        """
        Generate email-friendly summary
        
        Args:
            report_data: Report data dictionary
        
        Returns:
            Email text content
        """
        metadata = report_data["report_metadata"]
        user_metrics = report_data["user_metrics"]
        booking_metrics = report_data["booking_metrics"]
        revenue_metrics = report_data["revenue_metrics"]
        health_score = report_data["health_score"]
        
        period_start = datetime.fromisoformat(metadata["period_start"]).strftime("%B %d, %Y")
        period_end = datetime.fromisoformat(metadata["period_end"]).strftime("%B %d, %Y")
        
        email_content = f"""
🏨 Luxury Haven Hotel - Weekly Performance Report
{'=' * 60}

Report Period: {period_start} - {period_end}

SYSTEM HEALTH SCORE: {health_score['total_score']}/100 - {health_score['status']}

KEY HIGHLIGHTS:
{'=' * 60}

👥 USER METRICS:
   • Total Users: {user_metrics['total_users']}
   • New Users: {user_metrics['new_users']} (+{user_metrics['user_growth_rate']}%)
   • Active Users: {user_metrics['active_users']}

📅 BOOKING METRICS:
   • Total Bookings: {booking_metrics['total_bookings']}
   • New Bookings: {booking_metrics['new_bookings']}
   • Confirmed: {booking_metrics['confirmed_bookings']} ({booking_metrics['confirmation_rate']}%)
   • Cancelled: {booking_metrics['cancelled_bookings']} ({booking_metrics['cancellation_rate']}%)

💰 REVENUE METRICS:
   • Total Revenue: ${revenue_metrics['total_revenue']:,.2f}
   • Avg Booking Value: ${revenue_metrics['avg_booking_value']:,.2f}
   • Potential Revenue: ${revenue_metrics['potential_revenue']:,.2f}
   • Lost Revenue: ${revenue_metrics['lost_revenue']:,.2f}

🏆 TOP PERFORMING ROOMS:
"""
        
        for idx, room_data in enumerate(revenue_metrics['top_performing_rooms'], 1):
            email_content += f"   {idx}. {room_data['room']}: ${room_data['revenue']:,.2f}\n"
        
        email_content += f"""
{'=' * 60}

For detailed report with visualizations, please check the HTML report.

This is an automated report generated by Luxury Haven Hotel Performance System.
"""
        
        return email_content


# Example usage
if __name__ == "__main__":
    print("Report Generator Module")
    print("=" * 50)
    print("This module generates formatted HTML and email reports")
    print("Use with PerformanceMetrics to create weekly reports")

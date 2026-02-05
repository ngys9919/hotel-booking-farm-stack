#!/usr/bin/env python3
"""
Weekly Report Automation Script for Luxury Haven Hotel
Automatically generates and distributes weekly performance reports
"""

import sys
import os
from datetime import datetime

# Add backend directory to path
sys.path.insert(0, '/home/ubuntu/hotel-booking-app/backend')

from performance_metrics import PerformanceMetrics
from report_generator import ReportGenerator
from database import rooms_collection, bookings_collection, users_collection


def generate_weekly_report():
    """
    Main function to generate weekly performance report
    """
    print("=" * 70)
    print("🏨 Luxury Haven Hotel - Weekly Report Generation")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Step 1: Collect metrics
        print("Step 1: Collecting performance metrics...")
        metrics_collector = PerformanceMetrics(
            users_collection=users_collection,
            bookings_collection=bookings_collection,
            rooms_collection=rooms_collection
        )
        
        report_data = metrics_collector.generate_weekly_report()
        print("✓ Metrics collected successfully")
        print()
        
        # Step 2: Save JSON report
        print("Step 2: Saving JSON report...")
        json_path = metrics_collector.save_report(report_data)
        print(f"✓ JSON report saved: {json_path}")
        print()
        
        # Step 3: Generate HTML report
        print("Step 3: Generating HTML report...")
        report_gen = ReportGenerator()
        html_path = report_gen.generate_html_report(report_data)
        print(f"✓ HTML report generated: {html_path}")
        print()
        
        # Step 4: Generate email summary
        print("Step 4: Generating email summary...")
        email_content = report_gen.generate_summary_email(report_data)
        
        # Save email content
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        email_path = f"/home/ubuntu/hotel-booking-app/reports/email_summary_{timestamp}.txt"
        with open(email_path, 'w') as f:
            f.write(email_content)
        print(f"✓ Email summary saved: {email_path}")
        print()
        
        # Step 5: Display summary
        print("=" * 70)
        print("📊 REPORT SUMMARY")
        print("=" * 70)
        print(email_content)
        print()
        
        # Step 6: Report completion
        print("=" * 70)
        print("✅ WEEKLY REPORT GENERATION COMPLETED SUCCESSFULLY")
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


if __name__ == "__main__":
    result = generate_weekly_report()
    
    # Exit with appropriate code
    sys.exit(0 if result["success"] else 1)

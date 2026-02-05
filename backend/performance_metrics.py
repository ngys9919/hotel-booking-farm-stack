"""
Performance Metrics Collection for Luxury Haven Hotel Booking System
Collects and analyzes key performance indicators (KPIs) for weekly reports
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
import json
from collections import defaultdict


class PerformanceMetrics:
    """Collects and analyzes performance metrics for the hotel booking system"""
    
    def __init__(self, users_collection, bookings_collection, rooms_collection):
        """
        Initialize with database collections
        
        Args:
            users_collection: MongoDB users collection
            bookings_collection: MongoDB bookings collection
            rooms_collection: MongoDB rooms collection
        """
        self.users = users_collection
        self.bookings = bookings_collection
        self.rooms = rooms_collection
    
    def get_date_range(self, days: int = 7) -> tuple:
        """
        Get date range for the last N days
        
        Args:
            days: Number of days to look back (default: 7 for weekly)
        
        Returns:
            Tuple of (start_date, end_date)
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        return start_date, end_date
    
    def collect_user_metrics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Collect user-related metrics
        
        Returns:
            Dictionary with user metrics
        """
        try:
            # Total users
            total_users = len(list(self.users.find({})))
            
            # New users in period
            new_users = len(list(self.users.find({
                "created_at": {
                    "$gte": start_date.isoformat(),
                    "$lte": end_date.isoformat()
                }
            })))
            
            # Active users (users who made bookings in period)
            bookings_in_period = list(self.bookings.find({
                "created_at": {
                    "$gte": start_date.isoformat(),
                    "$lte": end_date.isoformat()
                }
            }))
            active_users = len(set(b.get("user_email", "") for b in bookings_in_period if b.get("user_email")))
            
            # User roles breakdown
            admin_users = len(list(self.users.find({"role": "admin"})))
            regular_users = total_users - admin_users
            
            return {
                "total_users": total_users,
                "new_users": new_users,
                "active_users": active_users,
                "admin_users": admin_users,
                "regular_users": regular_users,
                "user_growth_rate": round((new_users / max(total_users - new_users, 1)) * 100, 2) if total_users > 0 else 0
            }
        except Exception as e:
            print(f"Error collecting user metrics: {e}")
            return {
                "total_users": 0,
                "new_users": 0,
                "active_users": 0,
                "admin_users": 0,
                "regular_users": 0,
                "user_growth_rate": 0
            }
    
    def collect_booking_metrics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Collect booking-related metrics
        
        Returns:
            Dictionary with booking metrics
        """
        try:
            # All bookings
            all_bookings = list(self.bookings.find({}))
            total_bookings = len(all_bookings)
            
            # Bookings in period
            bookings_in_period = list(self.bookings.find({
                "created_at": {
                    "$gte": start_date.isoformat(),
                    "$lte": end_date.isoformat()
                }
            }))
            new_bookings = len(bookings_in_period)
            
            # Status breakdown
            confirmed_bookings = len([b for b in bookings_in_period if b.get("status") == "confirmed"])
            cancelled_bookings = len([b for b in bookings_in_period if b.get("status") == "cancelled"])
            pending_bookings = len([b for b in bookings_in_period if b.get("status") == "pending"])
            
            # Confirmation rate
            confirmation_rate = round((confirmed_bookings / max(new_bookings, 1)) * 100, 2) if new_bookings > 0 else 0
            
            # Average guests per booking
            total_guests = sum(b.get("guests", 1) for b in bookings_in_period)
            avg_guests = round(total_guests / max(new_bookings, 1), 2) if new_bookings > 0 else 0
            
            # Average nights per booking
            total_nights = 0
            for booking in bookings_in_period:
                try:
                    check_in = datetime.fromisoformat(booking.get("check_in_date", ""))
                    check_out = datetime.fromisoformat(booking.get("check_out_date", ""))
                    nights = (check_out - check_in).days
                    total_nights += nights
                except:
                    pass
            avg_nights = round(total_nights / max(new_bookings, 1), 2) if new_bookings > 0 else 0
            
            return {
                "total_bookings": total_bookings,
                "new_bookings": new_bookings,
                "confirmed_bookings": confirmed_bookings,
                "cancelled_bookings": cancelled_bookings,
                "pending_bookings": pending_bookings,
                "confirmation_rate": confirmation_rate,
                "cancellation_rate": round((cancelled_bookings / max(new_bookings, 1)) * 100, 2) if new_bookings > 0 else 0,
                "avg_guests_per_booking": avg_guests,
                "avg_nights_per_booking": avg_nights
            }
        except Exception as e:
            print(f"Error collecting booking metrics: {e}")
            return {
                "total_bookings": 0,
                "new_bookings": 0,
                "confirmed_bookings": 0,
                "cancelled_bookings": 0,
                "pending_bookings": 0,
                "confirmation_rate": 0,
                "cancellation_rate": 0,
                "avg_guests_per_booking": 0,
                "avg_nights_per_booking": 0
            }
    
    def collect_revenue_metrics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Collect revenue-related metrics
        
        Returns:
            Dictionary with revenue metrics
        """
        try:
            # Bookings in period
            bookings_in_period = list(self.bookings.find({
                "created_at": {
                    "$gte": start_date.isoformat(),
                    "$lte": end_date.isoformat()
                }
            }))
            
            # Total revenue (confirmed bookings only)
            confirmed_bookings = [b for b in bookings_in_period if b.get("status") == "confirmed"]
            total_revenue = sum(float(b.get("total_price", 0)) for b in confirmed_bookings)
            
            # Average booking value
            avg_booking_value = round(total_revenue / max(len(confirmed_bookings), 1), 2) if confirmed_bookings else 0
            
            # Revenue by room type
            revenue_by_room = defaultdict(float)
            bookings_by_room = defaultdict(int)
            for booking in confirmed_bookings:
                room_name = booking.get("room_name", "Unknown")
                revenue_by_room[room_name] += float(booking.get("total_price", 0))
                bookings_by_room[room_name] += 1
            
            # Top performing rooms
            top_rooms = sorted(revenue_by_room.items(), key=lambda x: x[1], reverse=True)[:3]
            
            # Potential revenue (all bookings including cancelled)
            potential_revenue = sum(float(b.get("total_price", 0)) for b in bookings_in_period)
            lost_revenue = potential_revenue - total_revenue
            
            return {
                "total_revenue": round(total_revenue, 2),
                "avg_booking_value": avg_booking_value,
                "potential_revenue": round(potential_revenue, 2),
                "lost_revenue": round(lost_revenue, 2),
                "revenue_by_room": dict(revenue_by_room),
                "bookings_by_room": dict(bookings_by_room),
                "top_performing_rooms": [{"room": room, "revenue": round(rev, 2)} for room, rev in top_rooms]
            }
        except Exception as e:
            print(f"Error collecting revenue metrics: {e}")
            return {
                "total_revenue": 0,
                "avg_booking_value": 0,
                "potential_revenue": 0,
                "lost_revenue": 0,
                "revenue_by_room": {},
                "bookings_by_room": {},
                "top_performing_rooms": []
            }
    
    def collect_room_metrics(self) -> Dict[str, Any]:
        """
        Collect room-related metrics
        
        Returns:
            Dictionary with room metrics
        """
        try:
            # Total rooms
            all_rooms = list(self.rooms.find({}))
            total_rooms = len(all_rooms)
            
            # Room price statistics
            prices = [float(r.get("price_per_night", 0)) for r in all_rooms]
            avg_price = round(sum(prices) / max(len(prices), 1), 2) if prices else 0
            min_price = round(min(prices), 2) if prices else 0
            max_price = round(max(prices), 2) if prices else 0
            
            # Room categories
            room_categories = {}
            for room in all_rooms:
                name = room.get("name", "Unknown")
                price = float(room.get("price_per_night", 0))
                room_categories[name] = price
            
            return {
                "total_rooms": total_rooms,
                "avg_room_price": avg_price,
                "min_room_price": min_price,
                "max_room_price": max_price,
                "room_categories": room_categories
            }
        except Exception as e:
            print(f"Error collecting room metrics: {e}")
            return {
                "total_rooms": 0,
                "avg_room_price": 0,
                "min_room_price": 0,
                "max_room_price": 0,
                "room_categories": {}
            }
    
    def generate_weekly_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive weekly performance report
        
        Returns:
            Dictionary with all metrics
        """
        start_date, end_date = self.get_date_range(7)
        
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "period_start": start_date.isoformat(),
                "period_end": end_date.isoformat(),
                "period_days": 7,
                "report_type": "weekly"
            },
            "user_metrics": self.collect_user_metrics(start_date, end_date),
            "booking_metrics": self.collect_booking_metrics(start_date, end_date),
            "revenue_metrics": self.collect_revenue_metrics(start_date, end_date),
            "room_metrics": self.collect_room_metrics()
        }
        
        # Calculate overall health score (0-100)
        health_score = self.calculate_health_score(report)
        report["health_score"] = health_score
        
        return report
    
    def calculate_health_score(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall system health score based on metrics
        
        Returns:
            Dictionary with health score and breakdown
        """
        try:
            booking_metrics = report["booking_metrics"]
            user_metrics = report["user_metrics"]
            revenue_metrics = report["revenue_metrics"]
            
            # Booking health (40 points)
            booking_score = 0
            if booking_metrics["new_bookings"] > 0:
                booking_score += 20
            if booking_metrics["confirmation_rate"] >= 80:
                booking_score += 15
            elif booking_metrics["confirmation_rate"] >= 60:
                booking_score += 10
            elif booking_metrics["confirmation_rate"] >= 40:
                booking_score += 5
            if booking_metrics["cancellation_rate"] < 10:
                booking_score += 5
            
            # User health (30 points)
            user_score = 0
            if user_metrics["new_users"] > 0:
                user_score += 15
            if user_metrics["active_users"] > 0:
                user_score += 10
            if user_metrics["user_growth_rate"] > 0:
                user_score += 5
            
            # Revenue health (30 points)
            revenue_score = 0
            if revenue_metrics["total_revenue"] > 0:
                revenue_score += 20
            if revenue_metrics["avg_booking_value"] > 200:
                revenue_score += 10
            elif revenue_metrics["avg_booking_value"] > 100:
                revenue_score += 5
            
            total_score = booking_score + user_score + revenue_score
            
            # Determine health status
            if total_score >= 80:
                status = "Excellent"
                color = "green"
            elif total_score >= 60:
                status = "Good"
                color = "blue"
            elif total_score >= 40:
                status = "Fair"
                color = "yellow"
            else:
                status = "Needs Attention"
                color = "red"
            
            return {
                "total_score": total_score,
                "booking_score": booking_score,
                "user_score": user_score,
                "revenue_score": revenue_score,
                "status": status,
                "color": color,
                "max_score": 100
            }
        except Exception as e:
            print(f"Error calculating health score: {e}")
            return {
                "total_score": 0,
                "booking_score": 0,
                "user_score": 0,
                "revenue_score": 0,
                "status": "Unknown",
                "color": "gray",
                "max_score": 100
            }
    
    def save_report(self, report: Dict[str, Any], filename: str = None) -> str:
        """
        Save report to JSON file
        
        Args:
            report: Report dictionary
            filename: Optional filename (default: auto-generated)
        
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_report_{timestamp}.json"
        
        filepath = f"/home/ubuntu/hotel-booking-app/reports/{filename}"
        
        # Create reports directory if it doesn't exist
        import os
        os.makedirs("/home/ubuntu/hotel-booking-app/reports", exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filepath


# Example usage
if __name__ == "__main__":
    # This would be used with real database collections
    print("Performance Metrics Collection Module")
    print("=" * 50)
    print("This module collects and analyzes KPIs for the hotel booking system")
    print("Use with database collections to generate weekly reports")

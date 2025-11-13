#!/usr/bin/env python3
"""
Jetlag Sleep Calculator
Calculates optimal sleep times based on departure time and destination timezone
to minimize jetlag effects.
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import sys

def get_timezone_abbreviation(timezone_name):
    """Get common timezone abbreviations for user-friendly display"""
    timezone_map = {
        'America/New_York': 'EST/EDT',
        'America/Chicago': 'CST/CDT',
        'America/Denver': 'MST/MDT',
        'America/Los_Angeles': 'PST/PDT',
        'Europe/London': 'GMT/BST',
        'Europe/Paris': 'CET/CEST',
        'Asia/Tokyo': 'JST',
        'Asia/Shanghai': 'CST',
        'Australia/Sydney': 'AEDT/AEST',
        'Pacific/Auckland': 'NZDT/NZST',
    }
    return timezone_map.get(timezone_name, timezone_name.split('/')[-1])

def calculate_time_difference(origin_tz, dest_tz):
    """Calculate time difference between two timezones"""
    now = datetime.now(ZoneInfo(origin_tz))
    dest_now = now.astimezone(ZoneInfo(dest_tz))
    time_diff = dest_now - now
    return time_diff.total_seconds() / 3600  # Return hours difference

def get_sleep_recommendations(origin_tz, dest_tz, departure_time, flight_duration_hours=0):
    """
    Calculate sleep recommendations based on timezone change and departure time.
    
    Args:
        origin_tz: Origin timezone (e.g., 'America/New_York')
        dest_tz: Destination timezone (e.g., 'Europe/London')
        departure_time: Departure datetime in origin timezone
        flight_duration_hours: Flight duration in hours
    
    Returns:
        Dictionary with sleep recommendations
    """
    # Calculate time difference
    time_diff_hours = calculate_time_difference(origin_tz, dest_tz)
    
    # Calculate arrival time
    arrival_time_origin = departure_time + timedelta(hours=flight_duration_hours)
    arrival_time_dest = arrival_time_origin.astimezone(ZoneInfo(dest_tz))
    
    # Determine direction of travel
    is_eastward = time_diff_hours > 0
    
    recommendations = {
        'time_difference_hours': time_diff_hours,
        'arrival_time_dest': arrival_time_dest,
        'is_eastward': is_eastward,
        'pre_flight_sleep': [],
        'post_flight_sleep': [],
        'tips': []
    }
    
    # Pre-flight recommendations (2-3 days before)
    days_before = [3, 2, 1]
    for days in days_before:
        if days == 1:
            # Day before: adjust to destination schedule
            if is_eastward:
                # Going east: go to bed earlier
                target_bedtime = departure_time.replace(hour=21, minute=0) - timedelta(days=1)
                target_wake = target_bedtime + timedelta(hours=8)
            else:
                # Going west: stay up later
                target_bedtime = departure_time.replace(hour=23, minute=0) - timedelta(days=1)
                target_wake = target_bedtime + timedelta(hours=8)
        else:
            # 2-3 days before: gradual adjustment
            adjustment_hours = (time_diff_hours / 3) * (4 - days)
            if is_eastward:
                target_bedtime = departure_time.replace(hour=22, minute=0) - timedelta(days=days) - timedelta(hours=adjustment_hours)
            else:
                target_bedtime = departure_time.replace(hour=22, minute=0) - timedelta(days=days) + timedelta(hours=abs(adjustment_hours))
            target_wake = target_bedtime + timedelta(hours=8)
        
        recommendations['pre_flight_sleep'].append({
            'days_before': days,
            'bedtime': target_bedtime.strftime('%Y-%m-%d %H:%M'),
            'wake_time': target_wake.strftime('%Y-%m-%d %H:%M')
        })
    
    # Post-flight recommendations
    # First night: try to sleep at local bedtime
    first_night_bedtime = arrival_time_dest.replace(hour=22, minute=0)
    if first_night_bedtime < arrival_time_dest:
        first_night_bedtime += timedelta(days=1)
    
    recommendations['post_flight_sleep'].append({
        'night': 1,
        'bedtime': first_night_bedtime.strftime('%Y-%m-%d %H:%M'),
        'wake_time': (first_night_bedtime + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M'),
        'note': 'Try to stay awake until local bedtime'
    })
    
    # General tips
    if abs(time_diff_hours) >= 6:
        recommendations['tips'].append("Large time difference detected. Consider melatonin supplements.")
    if is_eastward:
        recommendations['tips'].append("Eastward travel: Expose yourself to morning light at destination.")
        recommendations['tips'].append("Avoid caffeine after 2 PM local time at destination.")
    else:
        recommendations['tips'].append("Westward travel: Expose yourself to evening light at destination.")
        recommendations['tips'].append("You may find it easier to adjust going west.")
    
    recommendations['tips'].append("Stay hydrated during flight.")
    recommendations['tips'].append("Avoid alcohol during flight.")
    recommendations['tips'].append("Try to sleep on the plane if it's nighttime at destination.")
    
    return recommendations

def print_recommendations(recommendations, origin_tz, dest_tz):
    """Pretty print sleep recommendations"""
    print("\n" + "="*60)
    print("JETLAG SLEEP RECOMMENDATIONS")
    print("="*60)
    print(f"\nTime Difference: {recommendations['time_difference_hours']:.1f} hours")
    print(f"Direction: {'Eastward' if recommendations['is_eastward'] else 'Westward'}")
    print(f"Arrival Time (Destination): {recommendations['arrival_time_dest'].strftime('%Y-%m-%d %H:%M %Z')}")
    
    print("\n" + "-"*60)
    print("PRE-FLIGHT SLEEP SCHEDULE (Adjust gradually)")
    print("-"*60)
    for sleep in recommendations['pre_flight_sleep']:
        print(f"\n{sleep['days_before']} day(s) before departure:")
        print(f"  Bedtime:  {sleep['bedtime']}")
        print(f"  Wake up:  {sleep['wake_time']}")
    
    print("\n" + "-"*60)
    print("POST-FLIGHT SLEEP SCHEDULE")
    print("-"*60)
    for sleep in recommendations['post_flight_sleep']:
        print(f"\nNight {sleep['night']} at destination:")
        print(f"  Bedtime:  {sleep['bedtime']} ({get_timezone_abbreviation(dest_tz)})")
        print(f"  Wake up:  {sleep['wake_time']} ({get_timezone_abbreviation(dest_tz)})")
        if 'note' in sleep:
            print(f"  Note:     {sleep['note']}")
    
    print("\n" + "-"*60)
    print("TIPS TO MINIMIZE JETLAG")
    print("-"*60)
    for i, tip in enumerate(recommendations['tips'], 1):
        print(f"{i}. {tip}")
    
    print("\n" + "="*60 + "\n")

def main():
    """Main interactive function"""
    print("\n" + "="*60)
    print("JETLAG SLEEP CALCULATOR")
    print("="*60)
    
    # Common timezones for easy selection
    common_timezones = {
        '1': ('America/New_York', 'New York (EST/EDT)'),
        '2': ('America/Chicago', 'Chicago (CST/CDT)'),
        '3': ('America/Denver', 'Denver (MST/MDT)'),
        '4': ('America/Los_Angeles', 'Los Angeles (PST/PDT)'),
        '5': ('Europe/London', 'London (GMT/BST)'),
        '6': ('Europe/Paris', 'Paris (CET/CEST)'),
        '7': ('Asia/Tokyo', 'Tokyo (JST)'),
        '8': ('Asia/Shanghai', 'Shanghai (CST)'),
        '9': ('Australia/Sydney', 'Sydney (AEDT/AEST)'),
        '10': ('Pacific/Auckland', 'Auckland (NZDT/NZST)'),
    }
    
    print("\nSelect your ORIGIN timezone:")
    for key, (tz, name) in common_timezones.items():
        print(f"  {key}. {name}")
    print("  Or enter a timezone name (e.g., 'America/New_York')")
    
    origin_choice = input("\nYour choice: ").strip()
    if origin_choice in common_timezones:
        origin_tz = common_timezones[origin_choice][0]
    else:
        origin_tz = origin_choice if origin_choice else 'America/New_York'
    
    print("\nSelect your DESTINATION timezone:")
    for key, (tz, name) in common_timezones.items():
        print(f"  {key}. {name}")
    print("  Or enter a timezone name (e.g., 'Europe/London')")
    
    dest_choice = input("\nYour choice: ").strip()
    if dest_choice in common_timezones:
        dest_tz = common_timezones[dest_choice][0]
    else:
        dest_tz = dest_choice if dest_choice else 'Europe/London'
    
    # Get departure time
    print("\nEnter your DEPARTURE TIME:")
    print("Format: YYYY-MM-DD HH:MM (e.g., 2024-12-15 14:30)")
    print("Or press Enter to use current time + 1 day")
    
    departure_str = input("Departure time: ").strip()
    if departure_str:
        try:
            departure_time = datetime.strptime(departure_str, '%Y-%m-%d %H:%M')
            departure_time = departure_time.replace(tzinfo=ZoneInfo(origin_tz))
        except ValueError:
            print("Invalid format. Using current time + 1 day.")
            departure_time = datetime.now(ZoneInfo(origin_tz)) + timedelta(days=1)
    else:
        departure_time = datetime.now(ZoneInfo(origin_tz)) + timedelta(days=1)
    
    # Get flight duration
    flight_duration = input("\nFlight duration in hours (press Enter for 0): ").strip()
    try:
        flight_duration_hours = float(flight_duration) if flight_duration else 0
    except ValueError:
        flight_duration_hours = 0
    
    # Calculate recommendations
    try:
        recommendations = get_sleep_recommendations(
            origin_tz, dest_tz, departure_time, flight_duration_hours
        )
        print_recommendations(recommendations, origin_tz, dest_tz)
    except Exception as e:
        print(f"\nError: {e}")
        print("Please check your timezone names and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()


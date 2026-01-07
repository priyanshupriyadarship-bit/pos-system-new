"""
Calendar Agent - Manages scheduling and time blocks
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta

class CalendarAgent:
    """
    Manages calendar scheduling and time blocking.
    Coordinates avatar time blocks and task scheduling.
    """
    
    def __init__(self, llm_engine):
        self.llm_engine = llm_engine
        self.events: Dict[str, Dict] = {}
        self.time_blocks: Dict[str, Dict] = {}
    
    def execute(self, user_input: str, context: Dict[str, Any]) -> Dict:
        """Handle calendar operations."""
        
        intent = self.llm_engine.analyze_intent(user_input)
        
        if "check" in intent.get('intent', '') or "what" in user_input.lower():
            return self.get_next_schedule(context)
        elif "block" in intent.get('intent', '') or "schedule" in user_input.lower():
            return self.create_time_block(user_input, context)
        else:
            return self.get_next_schedule(context)
    
    def get_next_schedule(self, context: Dict) -> Dict:
        """Get user's next scheduled events."""
        
        # Create sample events for demo
        now = datetime.now()
        sample_events = [
            {
                'id': '1',
                'title': 'Team Standup',
                'start': now + timedelta(hours=1),
                'duration_minutes': 30,
                'avatar': 'Businessman'
            },
            {
                'id': '2',
                'title': 'Focus Time - Coding',
                'start': now + timedelta(hours=2),
                'duration_minutes': 120,
                'avatar': 'Businessman'
            },
            {
                'id': '3',
                'title': 'Gym Workout',
                'start': now + timedelta(hours=5),
                'duration_minutes': 60,
                'avatar': 'Warrior'
            },
            {
                'id': '4',
                'title': 'Family Dinner',
                'start': now + timedelta(hours=9),
                'duration_minutes': 90,
                'avatar': 'Nurturer'
            },
            {
                'id': '5',
                'title': 'Creative Writing',
                'start': now + timedelta(hours=11),
                'duration_minutes': 60,
                'avatar': 'Creator'
            }
        ]
        
        # Format events for display
        formatted_events = []
        for event in sample_events:
            formatted_events.append({
                'title': event['title'],
                'time': event['start'].strftime('%H:%M'),
                'duration': event['duration_minutes'],
                'avatar': event['avatar']
            })
        
        schedule_text = "\n".join([
            f"🕐 {e['time']} - {e['title']} ({e['duration']} min) [{e['avatar']}]"
            for e in formatted_events
        ])
        
        return {
            'success': True,
            'events': formatted_events,
            'count': len(formatted_events),
            'schedule': schedule_text,
            'message': f"📅 Your schedule for today:\n{schedule_text}"
        }
    
    def create_time_block(self, user_input: str, context: Dict) -> Dict:
        """
        Create a time block for an avatar.
        
        Example: Create "Warrior" block from 6am-9am for fitness tasks.
        """
        
        now = datetime.now()
        
        # Parse time block request
        avatar_names = ['Warrior', 'Businessman', 'Creator', 'Nurturer']
        avatar = next((a for a in avatar_names if a.lower() in user_input.lower()), 'Businessman')
        
        # Create default morning block (6am-9am)
        start_time = now.replace(hour=6, minute=0, second=0, microsecond=0)
        if start_time < now:
            start_time = start_time + timedelta(days=1)
        
        duration_hours = 3
        end_time = start_time + timedelta(hours=duration_hours)
        
        block_id = f"{avatar}_{start_time.strftime('%Y%m%d')}"
        
        time_block = {
            'id': block_id,
            'avatar': avatar,
            'start': start_time,
            'end': end_time,
            'duration_hours': duration_hours,
            'created_at': datetime.now().isoformat()
        }
        
        self.time_blocks[block_id] = time_block
        
        return {
            'success': True,
            'block_id': block_id,
            'message': f" Created {avatar} block from {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}",
            'time_block': time_block
        }
    
    def get_avatar_blocks(self, context: Dict) -> Dict:
        """Get all avatar time blocks for today."""
        
        blocks_by_avatar = {}
        for block in self.time_blocks.values():
            avatar = block['avatar']
            if avatar not in blocks_by_avatar:
                blocks_by_avatar[avatar] = []
            blocks_by_avatar[avatar].append(block)
        
        return {
            'success': True,
            'blocks': blocks_by_avatar,
            'count': len(self.time_blocks),
            'message': f" Avatar time blocks: {len(self.time_blocks)} total"
        }
    
    def reschedule_event(self, event_id: str, new_time: datetime) -> Dict:
        """Reschedule an event to a new time."""
        
        if event_id not in self.events:
            return {
                'success': False,
                'message': f"  Event {event_id} not found"
            }
        
        event = self.events[event_id]
        old_time = event.get('start')
        event['start'] = new_time
        
        return {
            'success': True,
            'message': f"  Rescheduled '{event['title']}' from {old_time} to {new_time}",
            'event': event
        }
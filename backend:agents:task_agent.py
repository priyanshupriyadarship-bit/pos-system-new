"""
Task Agent - Handles all task-related operations
"""
from typing import Dict, List, Any
from datetime import datetime
import uuid
import json

class TaskAgent:
    """
    Handles all task operations:
    - Creating tasks
    - Prioritizing tasks
    - Scheduling tasks
    - Completing tasks
    - Managing task lifecycle
    """
    
    def __init__(self, llm_engine):
        self.llm_engine = llm_engine
        self.tasks: Dict[str, Dict] = {}
    
    def execute(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method for task operations.
        
        Args:
            user_input: User's request (e.g., "Add task: Write report by Friday")
            context: User's current state and goals
        
        Returns:
            Result of task operation
        """
        
        intent = self.llm_engine.analyze_intent(user_input)
        
        if "create" in intent.get('intent', '') or "add" in user_input.lower():
            return self.create_task(user_input, context)
        elif "complete" in intent.get('intent', '') or "done" in user_input.lower():
            return self.mark_complete(user_input, context)
        elif "list" in user_input.lower() or "show" in user_input.lower():
            return self.list_tasks(context)
        else:
            return self.create_task(user_input, context)
    
    def create_task(self, user_input: str, context: Dict) -> Dict:
        """Create a new task from user input."""
        
        # Extract task details using LLM
        prompt = f"""
Extract task details from this input:
"{user_input}"

Return JSON (only JSON, no other text):
{{
    "title": "task title",
    "due_date": "YYYY-MM-DD or null",
    "estimated_minutes": 30,
    "avatar": "Warrior|Businessman|Creator|Nurturer|null"
}}
"""
        
        response = self.llm_engine.think(prompt, context)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1:
                task_data = json.loads(response[json_start:json_end])
            else:
                task_data = {"title": user_input}
        except:
            task_data = {"title": user_input}
        
        # Determine priority
        priority = self.llm_engine.determine_priority(
            task_data.get('title', user_input),
            context
        )
        
        # Assign avatar if not specified
        if not task_data.get('avatar'):
            task_data['avatar'] = self._suggest_avatar(task_data.get('title', user_input))
        
        # Create task object
        task_id = str(uuid.uuid4())[:8]
        task = {
            'id': task_id,
            'title': task_data.get('title', user_input),
            'priority': priority,
            'avatar': task_data.get('avatar', 'Businessman'),
            'due_date': task_data.get('due_date'),
            'estimated_minutes': task_data.get('estimated_minutes', 30),
            'status': 'inbox',
            'created_at': datetime.now().isoformat(),
            'completed_at': None
        }
        
        # Save to memory
        self.tasks[task_id] = task
        
        return {
            'success': True,
            'task_id': task_id,
            'message': f"✅ Task created: {task['title']} ({priority})",
            'task': task
        }
    
    def mark_complete(self, user_input: str, context: Dict) -> Dict:
        """Mark a task as complete and award XP."""
        
        if not self.tasks:
            return {'success': False, 'message': 'No tasks found'}
        
        # Get the most recent task (simple approach)
        latest_task = list(self.tasks.values())[-1]
        
        latest_task['status'] = 'completed'
        latest_task['completed_at'] = datetime.now().isoformat()
        
        return {
            'success': True,
            'message': f" Task completed: {latest_task['title']}",
            'task': latest_task
        }
    
    def list_tasks(self, context: Dict) -> Dict:
        """List all pending tasks."""
        
        pending_tasks = [t for t in self.tasks.values() if t['status'] != 'completed']
        
        return {
            'success': True,
            'count': len(pending_tasks),
            'tasks': pending_tasks,
            'message': f" You have {len(pending_tasks)} pending tasks"
        }
    
    def _suggest_avatar(self, task_title: str) -> str:
        """Suggest which avatar this task belongs to."""
        
        prompt = f"""
Which life role should this task belong to?
Task: {task_title}

Options: Warrior, Businessman, Creator, Nurturer

Respond with ONLY the avatar name.
"""
        
        response = self.llm_engine.think(prompt, {})
        
        valid_avatars = ['Warrior', 'Businessman', 'Creator', 'Nurturer']
        
        for avatar in valid_avatars:
            if avatar.lower() in response.lower():
                return avatar
        
        return 'Businessman'  # default
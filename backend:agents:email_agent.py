"""
Email Agent - Processes emails and converts them to tasks
"""
from typing import Dict, Any, List
import json

class EmailAgent:
    """
    Processes incoming emails and converts them to tasks.
    Automatically categorizes and responds to routine emails.
    """
    
    def __init__(self, llm_engine):
        self.llm_engine = llm_engine
        self.processed_emails: List[Dict] = []
    
    def execute(self, user_input: str, context: Dict[str, Any]) -> Dict:
        """
        Process email-related requests.
        
        Args:
            user_input: User's email request
            context: User context
        
        Returns:
            Result of email processing
        """
        
        # Simulate processing emails (in real implementation, would use Gmail API)
        return self.process_sample_emails(context)
    
    def process_sample_emails(self, context: Dict) -> Dict:
        """Process sample emails for demo."""
        
        sample_emails = [
            {
                'from': 'boss@company.com',
                'subject': 'Project update needed',
                'body': 'Can you send me the Q4 report by Friday?'
            },
            {
                'from': 'friend@email.com',
                'subject': 'Coffee this week?',
                'body': 'Hey! Want to grab coffee on Wednesday?'
            }
        ]
        
        results = []
        
        for email in sample_emails:
            analysis = self._analyze_email(email, context)
            
            if analysis.get('is_actionable'):
                task = {
                    'title': analysis['task_title'],
                    'source': 'email',
                    'priority': analysis.get('priority', 'P3'),
                    'from': email['from']
                }
                results.append({
                    'type': 'task',
                    'data': task,
                    'message': f"  Task from email: {task['title']}"
                })
            
            if analysis.get('needs_response'):
                draft = self._draft_response(email, analysis, context)
                results.append({
                    'type': 'email_draft',
                    'data': draft,
                    'message': f" Draft response ready"
                })
        
        return {
            'success': True,
            'processed': len(sample_emails),
            'actions': results,
            'message': f"  Processed {len(sample_emails)} emails"
        }
    
    def _analyze_email(self, email: Dict, context: Dict) -> Dict:
        """Analyze email to determine if actionable."""
        
        email_body = email.get('body', '')
        subject = email.get('subject', '')
        
        prompt = f"""
Is this email actionable? Does it require a task or response?

Subject: {subject}
Body: {email_body}

Return JSON (only JSON):
{{
    "is_actionable": true/false,
    "task_title": "if actionable, what's the task?",
    "needs_response": true/false,
    "tone_for_response": "professional|warm|urgent",
    "priority": "P1|P2|P3|P4"
}}
"""
        
        response = self.llm_engine.think(prompt, context)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1:
                return json.loads(response[json_start:json_end])
        except:
            pass
        
        return {
            'is_actionable': False,
            'needs_response': False
        }
    
    def _draft_response(self, email: Dict, analysis: Dict, context: Dict) -> Dict:
        """Draft an email response."""
        
        email_body = email.get('body', '')
        subject = email.get('subject', '')
        tone = analysis.get('tone_for_response', 'professional')
        
        prompt = f"""
Draft a brief email response to this email:

Subject: {subject}
Body: {email_body}

Tone: {tone}

Keep response under 2 sentences. Be helpful and professional.
"""
        
        draft_text = self.llm_engine.think(prompt, context)
        
        return {
            'type': 'email_draft',
            'to': email.get('from'),
            'subject': f"Re: {subject}",
            'body': draft_text,
            'requires_review': True,
            'tone': tone
        }
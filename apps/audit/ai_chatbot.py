import os
import json
from django.conf import settings
from typing import List, Dict

class AIChatbot:
    """AI chatbot for answering questions about audit logs."""
    
    def __init__(self):
        self.openai_key = settings.OPENAI_API_KEY
        self.gemini_key = settings.GEMINI_API_KEY
    
    def format_logs_for_ai(self, logs):
        """Format audit logs for AI consumption."""
        formatted = []
        for log in logs:
            formatted.append({
                'timestamp': log.created_at.isoformat(),
                'user': log.user.email,
                'action': log.action,
                'resource_type': log.resource_type,
                'details': log.details
            })
        return formatted
    
    def generate_prompt(self, logs, question):
        """Generate prompt for AI model."""
        logs_json = json.dumps(logs, indent=2, default=str)
        
        prompt = f"""
        You are an AI assistant for an organization manager application.
        Here are today's audit logs for the organization:
        
        {logs_json}
        
        Please answer the following question based ONLY on these logs:
        {question}
        
        Provide a concise, accurate answer. If the question cannot be answered from the logs,
        say so politely.
        """
        
        return prompt
    
    def ask_openai(self, prompt):
        """Query OpenAI API."""
        import openai
        openai.api_key = self.openai_key
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for organizational analytics."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error querying OpenAI: {str(e)}"
    
    def ask_gemini(self, prompt):
        """Query Google Gemini API."""
        import google.generativeai as genai
        genai.configure(api_key=self.gemini_key)
        
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error querying Gemini: {str(e)}"
    
    def ask(self, logs, question, stream=False):
        """Ask AI a question about logs."""
        formatted_logs = self.format_logs_for_ai(logs)
        prompt = self.generate_prompt(formatted_logs, question)
        
        # Use Gemini if available, else OpenAI
        if self.gemini_key:
            answer = self.ask_gemini(prompt)
        elif self.openai_key:
            answer = self.ask_openai(prompt)
        else:
            answer = "No AI service configured. Please set OPENAI_API_KEY or GEMINI_API_KEY."
        
        return answer
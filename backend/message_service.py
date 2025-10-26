from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MessageGenerationService:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
    
    async def generate_message(self, emotion: str, language: str) -> str:
        """
        Generate an empathetic motivational message based on emotion and language.
        
        Args:
            emotion: The user's current emotion
            language: The language for the message
            
        Returns:
            Generated motivational message
        """
        try:
            # Create a unique session ID for each request
            session_id = f"moodmate_{emotion}_{language}_{datetime.utcnow().timestamp()}"
            
            # System message that defines MoodMate's personality
            system_message = (
                "You are MoodMate, an empathetic AI that instantly creates short motivational messages. "
                "Your goal is to make the user feel understood, calm, and inspired - like a supportive friend. "
                f"Always respond in the selected language: {language}. "
                f"The user's current emotion is: {emotion}. "
                "Write a unique 1-2 sentence message that matches their emotion and uplifts them emotionally. "
                "Keep the tone natural, warm, and hopeful. Avoid robotic or overly generic phrases. "
                "Add a small emoji if appropriate, but never more than two. "
                "Return ONLY the message text, nothing else."
            )
            
            # Initialize the chat
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message=system_message
            ).with_model("openai", "gpt-4o-mini")
            
            # Create user message
            user_message = UserMessage(
                text=f"Generate a motivational message for someone feeling {emotion}."
            )
            
            # Send message and get response
            response = await chat.send_message(user_message)
            
            logger.info(f"Generated message for emotion={emotion}, language={language}")
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating message: {str(e)}")
            # Fallback message if AI fails
            fallback_messages = {
                'English': 'You are doing great. Keep going! 💙',
                'Turkish': 'Harika gidiyorsun. Devam et! 💙',
                'Spanish': '¡Lo estás haciendo genial. Sigue adelante! 💙',
                'German': 'Du machst das großartig. Mach weiter! 💙',
                'French': 'Tu fais du bon travail. Continue! 💙',
                'Italian': 'Stai andando alla grande. Continua così! 💙',
                'Russian': 'У тебя отлично получается. Продолжай! 💙',
                'Arabic': 'أنت تقوم بعمل رائع. استمر! 💙',
                'Japanese': '素晴らしいです。頑張って! 💙'
            }
            return fallback_messages.get(language, fallback_messages['English'])
# services/summarizer_service.py
from uuid import uuid4
from datetime import datetime, timezone
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .system_prompts import get_prompt_template
from utils.logger import setup_logger

logger = setup_logger(__name__)

class SummarizerService:
    def __init__(self, db):
        self.db = db
        logger.info("Initializing SummarizerService")
    
    async def summarize_text(self, text, summary_type, api_key, username):
        logger.info("Initializing SummarizerService")
        llm = ChatGroq(
            api_key=api_key,
            model="llama-3.3-70b-versatile",  
            temperature=0
        )
        
        # Get prompt template
        prompt_template = get_prompt_template(summary_type)
        logger.debug(f"Using template for type: {summary_type}")

        # Create prompt and chain using new RunnableSequence approach
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | llm | StrOutputParser()
        
        # Generate summary
        logger.info("Generating summary")
        summary = await chain.ainvoke({"text": text})
        
        # Store in database
        summary_id = str(uuid4())
        logger.info(f"Storing summary with ID: {summary_id}")

        await self.db.summaries.insert_one({
            "summary_id": summary_id,
            "username": username,
            "summary_type": summary_type,
            "original_text": text,
            "summary": summary,
            "created_at": datetime.now(timezone.utc)  
        })
        
        return summary, summary_id
    
    async def get_user_summaries(self, username):
        summaries = []
        cursor = self.db.summaries.find({"username": username}).sort("created_at", -1)
        async for summary in cursor:
            summaries.append({
                "id": summary["summary_id"],
                "type": summary["summary_type"],
                # "title": summary.get("title", "Untitled Summary"),
                "created_at": summary["created_at"].strftime("%Y-%m-%d %H:%M")
            })
        return summaries
    
    async def get_summary_by_id(self, summary_id, username):
        return await self.db.summaries.find_one({
            "summary_id": summary_id,
            "username": username
        })
    
    async def save_summary(self, summary_id: str, username: str) -> bool:
        try:
            # First check if summary exists
            summary = await self.db.summaries.find_one({
                "summary_id": summary_id,
                "username": username
            })
            
            if not summary:
                return False
                
            # Update the saved status
            result = await self.db.summaries.update_one(
                {"summary_id": summary_id, "username": username},
                {"$set": {"saved": True}}
            )
            return result.modified_count > 0
            
        except Exception as e:
            print(f"Error saving summary: {str(e)}")
            return False
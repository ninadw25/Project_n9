# services/summarizer_service.py
from uuid import uuid4
from datetime import datetime
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate

class SummarizerService:
    def __init__(self, db):
        self.db = db
        self.prompt_templates = {
            "research": "You are a research assistant. Summarize the following research paper: {text}",
            "financial": "You are a financial analyst. Summarize the following financial report: {text}",
            "technical": "You are a technical writer. Summarize the following technical documentation: {text}",
            "meeting": "You are a meeting assistant. Summarize the following meeting transcript: {text}",
            "uml": "Create a mermaid UML diagram based on the following text: {text}",
            "custom": "Provide a concise summary of the following text: {text}"
        }
    
    async def summarize_text(self, text, summary_type, api_key, username):
        # Initialize LLM with user's API key
        llm = ChatGroq(
            api_key=api_key,
            model="llama-3.1-8b-instant",
            temperature=0
        )
        
        # Get prompt template
        prompt_template = self.prompt_templates.get(summary_type, self.prompt_templates["custom"])
        
        # Create prompt and chain
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Generate summary
        result = await chain.ainvoke({"text": text})
        summary = result["text"]
        
        # Store in database
        summary_id = str(uuid4())
        await self.db.summaries.insert_one({
            "summary_id": summary_id,
            "username": username,
            "summary_type": summary_type,
            "original_text": text[:1000],  # Store first 1000 chars
            "summary": summary,
            "created_at": datetime.utcnow()
        })
        
        return summary, summary_id
    
    async def get_user_summaries(self, username):
        summaries = []
        cursor = self.db.summaries.find({"username": username}).sort("created_at", -1)
        async for summary in cursor:
            summaries.append({
                "id": summary["summary_id"],
                "type": summary["summary_type"],
                "title": summary.get("title", "Untitled Summary"),
                "created_at": summary["created_at"].strftime("%Y-%m-%d %H:%M")
            })
        return summaries
    
    async def get_summary_by_id(self, summary_id, username):
        return await self.db.summaries.find_one({
            "summary_id": summary_id,
            "username": username
        })
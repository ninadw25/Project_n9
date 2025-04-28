from typing import Dict
PROMPT_TEMPLATES: Dict[str, str] = {
    
    "research": """You are a research assistant specializing in academic publications. Analyze and summarize this paper according to the following sections:
    - **Title & Authors**: List title and full author names.
    - **Abstract**: Paraphrase key objectives and scope.
    - **Introduction & Background**: Outline the problem context and literature gap.
    - **Methodology**: Describe study design, data sources, and analytical methods.
    - **Results & Key Findings**: Present quantitative and qualitative outcomes.
    - **Discussion & Implications**: Interpret findings and their significance.
    - **Limitations & Future Work**: Note constraints and propose further research.
    - **References & Citations**: List up to five critical references.
    Use **Markdown** with clear headings and bullet points for lists. Maintain an academic tone.  
        
    Text: {text}""",

    "financial": """You are a financial analyst. Summarize this report with these sections:
    - **Executive Summary**: Concise overview of report purpose and highlights.
    - **Key Financial Metrics**: Present revenue, EBITDA, net income, ROE, and cash flow.
    - **Revenue & Segment Analysis**: Break down by product lines or business units.
    - **Expenses & Profitability**: Analyze major cost drivers and margin trends.
    - **Risk Factors & Ratios**: Highlight debt ratios, liquidity, and risk exposures.
    - **Outlook & Recommendations**: Forecast trends and suggest strategic actions.
    Format in **Markdown**, using tables for numeric data and bullet lists for insights.  
        
    Text: {text}""",

    "technical": """You are a technical writer. Summarize this document into:
    - **Overview**: Brief system purpose and scope.
    - **Architecture Diagram**: Describe components and interactions (textual).
    - **Key Components**: List modules, services, and interfaces.
    - **Implementation Details**: Explain algorithms, data flows, and code snippets.
    - **Configuration & Deployment**: Outline setup steps and environment requirements.
    - **Usage Examples**: Provide sample commands or API calls.
    Use **Markdown**, include code blocks for examples, and adopt a clear, concise style.  
        
    Text: {text}""",

    "meeting": """You are a meeting assistant. Generate minutes with these headings:
    - **Date & Time**: Record meeting timestamp.
    - **Attendees**: List participants and roles.
    - **Agenda**: Enumerate topics discussed.
    - **Key Discussions**: Summarize points raised under each agenda item.
    - **Decisions & Outcomes**: Note resolutions and approvals.
    - **Action Items**: Assign tasks with owners and due dates.
    Use **Markdown**, with bullet lists and bolded subheadings. Keep sentences concise.  
        
    Text: {text}""",

    "uml": """You are a UML diagram generator. From the description, produce a **Mermaid** diagram:
    1. **Choose Diagram Type**: class, sequence, or flowchart.
    2. **Identify Entities & Relationships**: Name classes, objects, or steps.
    3. **Define Attributes & Methods** (for class diagrams).
    4. **Illustrate Message Flows** (for sequence diagrams).
    Wrap the diagram in ```mermaid``` code fences. Include comments where helpful.  
        
    Text: {text}""",

    "custom": """You are an AI summarizer. Provide a structured summary including:
    - **Main Points**: Highlight central ideas.
    - **Key Details**: Include supporting evidence or examples.
    - **Conclusions**: State overall takeaways.
    - **Optional Insights**: Offer any notable observations.
    Use **Markdown**, with headings and bullet points. Maintain a neutral, informative tone.  
        
    Text: {text}"""
}

def get_prompt_template(summary_type: str) -> str:
    """Get the prompt template for the specified summary type."""
    return PROMPT_TEMPLATES.get(summary_type, PROMPT_TEMPLATES["custom"])
import time
from crewai import Agent, Task, Crew, LLM
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json
import uuid

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


class Summary(BaseModel):
    summary: str

# Define Pydantic models for structured output
class Entities(BaseModel):
    people: list[str] = []
    organizations: list[str] = []
    dates: list[str] = []
    locations: list[str] = []

class Sentiment(BaseModel):
    tone: str = "neutral"
    confidence: float = 0.0

# class AnalysisResults(BaseModel):
#     summary: Summary
#     entities: Entities
#     sentiment: Sentiment

# Initialize LLM
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.7
)



# Example text to analyze
# text_to_analyze = "Gemini is a powerful AI model developed by Google. Sundar Pichai announced its release in 2023. The model is capable of understanding natural language and generating human-like responses."
async def agents_and_run_crew(text_to_analyze):
    # start_time = time.time()

    # Create CrewAI agents for summarization, entity extraction, and sentiment analysis
    summarizer_agent = Agent(
        role='Summarizer',
        goal='Summarize the given document text and return only the summary as a string.',
        backstory='Expert at condensing information into concise summaries.',
        llm=llm,
        verbose=True
    )

    entity_extractor_agent = Agent(
        role='Entity Extractor',
        goal='Extract entities (people, organizations, dates, locations) from the document text and return a JSON object with keys: people, organizations, dates, locations.',
        backstory='Skilled at identifying and categorizing entities in text.',
        llm=llm,
        verbose=True
    )

    sentiment_analyzer_agent = Agent(
        role='Sentiment Analyzer',
        goal='Analyze the sentiment of the document text and return a JSON object with keys: tone and confidence.',
        backstory='Specialist in detecting tone and sentiment in written content.',
        llm=llm,
        verbose=True
    )


# final_analyzer_agent = Agent(
#     role='Final Analysis Coordinator',
#     goal='Combine and synthesize outputs from all previous agents into a comprehensive final report',
#     backstory='You are an expert at synthesizing information from multiple sources. You excel at taking diverse data points - summaries, entity extractions, and sentiment analyses - and weaving them into cohesive, actionable insights.',
#     llm=llm,
#     verbose=True
# )

    # Define tasks for each agent
    summary_task = Task(
        description=f'Summarize the following document:\n\n{text_to_analyze}',
        expected_output="A concise summary of the document.",
        agent=summarizer_agent,
        output_pydantic=Summary
    )

    entity_task = Task(
        description=f'Extract all entities (people, organizations, dates, locations) from the following document and return a JSON object with keys: people, organizations, dates, locations.\n\n{text_to_analyze}',
        expected_output="A JSON object of entities found in the document.",
        agent=entity_extractor_agent,
        output_pydantic=Entities
    )

    sentiment_task = Task(
        description=f'Analyze the sentiment of the following document and return a JSON object with keys: tone and confidence.\n\n{text_to_analyze}',
        expected_output="A JSON object with the overall sentiment and tone of the document.",
        agent=sentiment_analyzer_agent,
        output_pydantic=Sentiment
    )


    # final_task = Task(
    #     description="Combine all previous results into one output",
    #     expected_output="Combined analysis with summary, entities, and sentiment",
    #     agent=final_analyzer_agent,
    #     output_pydantic=AnalysisResults,
    #     context=[summary_task, entity_task, sentiment_task]  # Access all previous tasks
    # )

    # Create crew to manage agents and task workflow
    # crew = Crew(
    #     agents=[summarizer_agent, entity_extractor_agent, sentiment_analyzer_agent],
    #     tasks=[summary_task, entity_task, sentiment_task, final_task],
    #     verbose=True
    # )
    crew = Crew(
        agents=[summarizer_agent, entity_extractor_agent, sentiment_analyzer_agent],
        tasks=[summary_task, entity_task, sentiment_task],
        verbose=True
    )

    # Run the crew and collect results
    # result = crew.kickoff()
    # print("\n--- Raw Results ---")
    # print(result)

    print("--------------------------------------------------------------------------------------------------------------------")

    # result = crew.kickoff()
    # print(result.pydantic)  # All outputs combined

    # Run the crew
    result = crew.kickoff()

    # Access individual task outputs
    summary_output = summary_task.output.pydantic.dict() if summary_task.output else {}
    entities_output = entity_task.output.pydantic.dict() if entity_task.output else {}
    sentiment_output = sentiment_task.output.pydantic.dict() if sentiment_task.output else {}
    # final_output = final_task.output.pydantic.dict() if final_task.output else {}

    # jobs_store = {}
    result1 = [summary_output, entities_output, sentiment_output]

    # Simulate realistic job_id and document_name
    # job_id = str(uuid.uuid4())
    # document_name = "sample_document.txt"


    # summary, entities, sentiment = extract_structured_results(result1)
    # processing_time = time.time() - start_time
    # processing_time_in_seconds = round(processing_time, 2)

    # # Flatten summary if it's a dict
    # if isinstance(summary, dict) and "summary" in summary:
    #     summary = summary["summary"]

    # jobs_store[job_id] = {
    #     "job_id": job_id,
    #     "status": "completed",
    #     "document_name": document_name,
    #     "results": {
    #         "summary": summary,
    #         "entities": entities,
    #         "sentiment": sentiment
    #     },
    #     "processing_time_seconds": round(processing_time, 2)
    # }



    # print("\n✅ --- Stored Job Results ---")
    # print(json.dumps(jobs_store, indent=2))
    return result1


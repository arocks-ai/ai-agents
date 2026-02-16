from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field


class EmailContent(BaseModel):
    subject: str = Field(..., description="The subject of the email. This message should be concise and very descriptive.")
    body: str = Field(..., description="The body of the email. This message should be well-formatted with proper greeting, one or more paragraphs, and end with email signature.")



root_agent = LlmAgent(
    name = "email_agent",
    model = "gemini-2.5-flash",
    instruction="""
        You are an Email Generation Assistant.
        Your task is to generate a professional email based on the user's request.

        GUIDELINES:
        - First greet with a greeting and ask how you can assist the user with their email needs.
        - Create an appropriate subject line (concise and relevant)
        - Write a well-structured email body with:
            * Professional greeting
            * Clear and concise main content
            * Appropriate closing
            * Your name as signature
        - Suggest relevant attachments if applicable (empty list if none needed)
        - Email tone should match the purpose (formal for business, friendly for colleagues)
        - Keep emails concise but complete

        IMPORTANT: Your response MUST be valid JSON matching this structure:
        {
            "subject": "Subject line here",
            "body": "Email body here with proper paragraphs and formatting",
        }

        DO NOT include any explanations or additional text outside the JSON response.
    """,
    description="Generates professional emails with structured subject and body",
    output_schema=EmailContent,
    output_key="email",
    # tools = [google_search]  # Tools can't be used along with output schema - if you want to use tools, you need to remove the output schema and make sure your agent outputs text in the correct format for tool parsing.
)



Maya Persona Evaluation System
==============================

This system evaluates AI-generated responses from various LLMs based on:
- Persona alignment
- Prompt consistency
- Engagement
- Overall quality
- Policy adherence (optional)
- Performance drift detection

The results can be uploaded to a Lovable dashboard for visualization and monitoring.

-------------------------------
Project Structure
-------------------------------

Files:
- evaluate_models.py              : Main evaluation script
- maya_systemprompts.txt          : System prompt for all models
- maya_persona_defination.md      : Persona characteristics and behavior
- user_test_cases.json            : User prompts to evaluate
- evaluation_results.json : Output result file (upload this to Lovable)
- evaluation_summary.md   : Markdown summary of model performance
- .env                            : API keys and config variables
- requirements.txt                : Required Python packages
- README.txt                      : This file

-------------------------------
Setup Instructions
-------------------------------

1. Clone the repository and move into the directory:
   git clone https://github.com/yourusername/maya-evaluator
   cd maya-evaluator

2. Create a .env file in the root folder with the following keys:
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_claude_api_key 
   MISTRAL_API_KEY=your_mistral_api_key

3. Install dependencies:
pip install -r requirements.txt

-------------------------------
How to Use
-------------------------------

To run the evaluation:
python evaluate_models.py

This will:
- Load prompts from user_test_cases.json
- Query multiple LLM APIs for responses
- Score each response using LLM-based evaluation
- Save:
- A JSON file: evaluation_results.json
- A Markdown summary: evaluation_summary.md

You can upload the result.json file to Lovable to monitor and compare results across models.

-------------------------------
Viewing Results (via Lovable)
-------------------------------

1. Open https://ai-eval-viz.lovable.app
2. Upload the file:
   results.json

Lovable will automatically visualize scores, comparison charts, and performance trends.

-------------------------------
Evaluation Metrics
-------------------------------

Each model is evaluated across:
- Persona alignment
- Prompt consistency
- Engagement level
- Overall quality
- (Optional) Policy violation flags
- Drift detection based on prior runs

All scores are generated using NLP models for consistency.

-------------------------------
Planned Features
-------------------------------

- Real-time evaluation pipeline
- Slack/email alerts for significant performance drops or violations
- Persona evolution tracking
- Live production monitoring


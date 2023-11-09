# Semantic Prompting Lunch Menu Analyzer
The Semantic Prompting Lunch Menu Analyzer is a serious name for my messing around with OpenAI APIs with the goal of experimenting with function calling. 

TL;DR: The program queries the lunch menu at a given restaurant near the Faculty of Informatics in Brno. 

## Features
- **Restaurant selection**: The program generates a function call for getting a restaurants menu by extracting the name from the prompt.
- **Day of week extraction**: The program extracts the day of week from the prompt. 
- **Menu analysis**: Based on the prompt, menu, and day of week the program prompts the model to generate the response.

## Getting Started
To get started with the Semantic Prompting Lunch Menu Analyzer, you'll need to set up a few things first.

### Prerequisites
- An OpenAI API key
- Python 3.6 or higher
- Pip for installing dependencies

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ondrejsotolar/filunch-api.git
   ```
2. Navigate to the project directory:
   ```bash
   cd filunch-api
   ```

## Usage
To use the analyzer, run the main script and follow the prompts:
   ```bash
   python -i lunch.py
   >>> getlunch("Is there a dish with rice at Divá Bára tomorrow?")
   ```

## Configuration
   ```plaintext
   OPENAI_API_KEY='your-api-key-here'
   ```

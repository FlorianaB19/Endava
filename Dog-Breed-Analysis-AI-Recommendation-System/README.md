# 🐕 Dog Breed Analysis & AI Recommendation System

A comprehensive interactive web application built with **Streamlit** for exploring, analyzing, and recommending dog breeds based on their characteristics, traits, and geographic distribution.

The project combines **data analysis, machine learning, recommendation algorithms, and Generative AI**.

In addition to traditional breed analysis and visualization, the application includes an **AI-powered Dog Breed Recommendation Assistant** that allows users to describe their personality, lifestyle, and preferences using natural language.

The assistant uses the **OpenAI API** to understand the user's preferences, while the actual dog breed recommendations are calculated using the project's local dog breed dataset.

> **OpenAI understands and explains. The dataset decides.**

---

## 🌟 Features

### 🔍 Search for Dog

* Interactive breed selector
* Detailed breed information
* Visual trait indicators
* Breed descriptions
* Height and weight information
* Life expectancy
* Breed-specific word clouds

Dog characteristics are organized into several categories:

* **Family Life**

  * Affection with family
  * Compatibility with children
  * Compatibility with other dogs

* **Physical Characteristics**

  * Shedding level
  * Grooming frequency
  * Drooling level

* **Social Characteristics**

  * Openness to strangers
  * Playfulness
  * Protective nature
  * Adaptability

* **Personality**

  * Trainability
  * Energy level
  * Barking level
  * Mental stimulation needs

---

## 📊 Descriptive Analysis

The application provides multiple statistical and visual analyses of the dog breed dataset.

Features include:

* Word cloud visualization
* Correlation matrix
* Trait frequency distributions
* Statistical insights
* Trait relationship analysis

Breed characteristics are generally represented using a **1–5 rating scale**.

---

## 🗺️ Geographic Analysis

The application uses **GeoPandas** to explore the geographic origin of dog breeds.

Features include:

* Interactive world map
* Country-based breed filtering
* Geographic breed distribution
* Country highlighting
* Breed origin exploration

---

## 🔬 Machine Learning Analysis

The project includes several machine learning and statistical techniques.

### Hierarchical Clustering

Dog breeds are grouped according to similarities between their characteristics.

### K-Means Clustering

K-Means clustering is used to explore groups of breeds based on physical characteristics.

### Elbow Method

Used to investigate an appropriate number of clusters.

### Silhouette Analysis

Used to evaluate clustering quality.

### Regression Analysis

The project includes:

* Simple linear regression
* Multiple linear regression

Examples include investigating relationships between:

* Height
* Weight
* Life expectancy

---

# 🤖 AI Dog Breed Recommendation Assistant

The application includes an interactive conversational assistant that recommends dog breeds based on the user's personality, lifestyle, and preferences.

Instead of completing a traditional questionnaire, users can describe themselves naturally.

Example:

> I live in a small apartment and I am not very active. I would prefer a small dog with a low energy level. Barking is very important to me because I prefer a quiet home.

The assistant gradually converts this conversation into a structured preference profile.

Example:

```text
Preferred size: Small
Energy level: 2/5
Barking level: 1/5
Trainability: 4/5
```

The resulting profile is matched against dog breeds contained in the project's dataset.

---

## 🧠 AI Recommendation Architecture

The recommendation system separates natural-language understanding from breed selection.

```text
User
  │
  ▼
Streamlit Chat Interface
  │
  ▼
OpenAI API
Natural Language Preference Extraction
  │
  ▼
Structured User Profile
  │
  ▼
Conversational Memory
  │
  ▼
Weighted Recommendation Engine
  │
  ▼
Local Dog Breed Dataset
  │
  ▼
Top 3 Matching Breeds
  │
  ▼
Grounded OpenAI Explanation
  │
  ▼
Breed Cards + Comparison + Match Explanation
```

This separation is intentional.

The language model does **not independently decide which dog breed should be recommended**.

Instead:

1. OpenAI interprets the user's natural-language input.
2. The application converts the input into structured preferences.
3. A deterministic recommendation algorithm compares those preferences with the local dataset.
4. The best matching breeds are selected.
5. OpenAI explains the selected results using the retrieved breed information.

---

## 💬 Conversational Preference Extraction

Users do not need to provide all information in a single message.

For example:

```text
User:
I live in a small apartment and I would prefer a small dog.

Assistant:
How active are you on a typical day?

User:
I am not very active.

Assistant:
How important is it for you to have a quiet dog?

User:
Barking is a deal breaker for me.
```

The application maintains a preference profile throughout the current Streamlit session.

Information from previous messages is preserved and combined with new information.

---

## ❓ Intelligent Clarifying Questions

The assistant does not immediately generate a recommendation when insufficient information is available.

For example:

```text
User:
I am a quiet person.
```

Instead of forcing a recommendation, the assistant may ask:

```text
Do you prefer a small, medium, or large dog?
```

or:

```text
How active are you on a typical day?
```

This allows the recommendation profile to be constructed progressively.

---

## 👤 User Preference Profile

The application displays the interpreted user preferences directly in the Streamlit interface.

Example:

```text
Preferred size: Small

Energy: 2/5
Barking: 1/5
Trainability: 4/5
Adaptability: 4/5
```

This makes the AI interpretation visible to the user rather than treating it as a hidden process.

---

## ⚖️ Preference Importance

Not every preference should influence the recommendation equally.

The system therefore supports preference importance weights:

```text
1 = Nice to have
2 = Important
3 = Very important
```

For example:

```text
"I would prefer a quiet dog."
```

may represent a normal preference.

However:

```text
"Barking is a deal breaker for me.
I absolutely need a very quiet dog."
```

indicates that barking should have significantly more influence on the final recommendation.

The OpenAI preference extraction component identifies this importance from the user's language.

---

## 🧮 Weighted Recommendation Algorithm

Dog breeds are ranked using a **weighted content-based recommendation algorithm**.

For each relevant trait, the system compares:

```text
User desired value
        ↓
Breed dataset value
        ↓
Trait similarity
```

Trait similarity is calculated on the project's 1–5 scale.

A perfect match receives:

```text
100%
```

A one-point difference receives:

```text
75%
```

A two-point difference receives:

```text
50%
```

A three-point difference receives:

```text
25%
```

The final score incorporates preference importance:

```text
                       Σ(Trait Similarity × Importance Weight)
Weighted Match Score = ───────────────────────────────────────
                               Σ(Importance Weights)
```

This means that a characteristic described as a **deal breaker** can influence the recommendation more strongly than a characteristic described as merely desirable.

---

## 📏 Dog Size Matching

Dog size is estimated using the breed's average weight:

```text
Average Weight =
(min_weight + max_weight) / 2
```

The recommendation system then assigns a simplified size category:

```text
Small  → up to 10 kg
Medium → above 10 kg and up to 25 kg
Large  → above 25 kg
```

The user's preferred dog size is included in the weighted recommendation score.

---

## 🏆 Top Breed Recommendations

The system returns the **Top 3 matching breeds**.

Each recommendation includes information such as:

* Overall match score
* Size
* Average weight
* Energy level
* Barking level
* Trainability
* Adaptability

The Streamlit interface presents these results using visual breed cards.

---

## 📊 Explainable Recommendations

The recommendation system is designed to be transparent.

Instead of displaying only:

```text
Italian Greyhound — 87.5% match
```

the application can explain how that score was obtained.

Example:

```text
Energy Level

Your preference: 2/5
Breed value: 3/5
Trait match: 75%

Preference importance:
Important (weight 2)
```

Another example:

```text
Barking Level

Your preference: 1/5
Breed value: 1/5
Trait match: 100%

Preference importance:
Very important (weight 3)
```

This makes it possible to understand why a breed received a particular recommendation score.

---

## ⚖️ Breed Comparison

Recommended breeds can also be compared directly.

The comparison is generated from the local dataset rather than by the language model.

Example:

| Trait         | Breed A | Breed B |
| ------------- | ------: | ------: |
| Match Score   |     92% |     87% |
| Energy Level  |     2/5 |     3/5 |
| Barking Level |     1/5 |     2/5 |
| Trainability  |     4/5 |     5/5 |
| Adaptability  |     5/5 |     4/5 |

Users can select multiple recommended breeds for a focused comparison.

---

# 🛡️ Hallucination Prevention

A major design goal of the AI assistant is to prevent the language model from inventing dog breeds or unsupported breed characteristics.

The application therefore separates **language understanding** from **recommendation logic**.

OpenAI is responsible for:

* Understanding natural-language user input
* Extracting structured preferences
* Detecting preference importance
* Producing natural-language explanations

The local application is responsible for:

* Selecting dog breeds
* Calculating similarity
* Calculating weighted scores
* Ranking breeds
* Retrieving breed characteristics
* Building comparison tables

The response-generation step receives only the candidate breeds selected by the recommendation engine and their associated dataset information.

The model is instructed to:

* Recommend only supplied candidate breeds
* Use only supplied breed information
* Never invent breed characteristics
* Avoid introducing unsupported external breed knowledge
* Explicitly acknowledge when information is unavailable

Therefore, the primary source of truth for breed recommendations is the **local project dataset**, not the language model's general knowledge.

---

# 📁 Project Structure

```text
dog-breed-analysis-streamlit-main/
│
├── chatbot/
│   ├── __init__.py
│   ├── comparison.py
│   ├── openai_client.py
│   ├── preference_extractor.py
│   ├── prompts.py
│   ├── recommendation_engine.py
│   └── response_generator.py
│
├── pages/
│   └── Dog_Recommendation_Chat.py
│
├── date_in/
│   ├── akc-data-latest.csv
│   ├── breed_rank.csv
│   ├── breed_traits.csv
│   ├── custom.geo.json
│   ├── Dog Breads Around The World.csv
│   └── dog.png
│
├── date_out/
│   ├── date.csv
│   └── date.py
│
├── .env
├── .env.example
├── .gitignore
├── Home.py
├── links_datasets.txt
├── README.md
└── requirements.txt
```

---

# 🚀 Installation

## Prerequisites

* Python 3.12 recommended
* pip
* OpenAI API key

Clone the repository:

```bash
git clone <repository-url>
cd dog-breed-analysis-streamlit-main
```

Create a virtual environment:

### Windows

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

---

# 🔑 OpenAI Configuration

Create a `.env` file in the project root.

```text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

The `.env` file contains sensitive credentials and **must never be committed to GitHub**.

The repository should instead contain:

```text
.env.example
```

with:

```text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

The project's `.gitignore` should contain:

```gitignore
.env
.venv/
venv/
__pycache__/
*.pyc
.idea/
.vscode/
```

---

# ▶️ Running the Application

Start Streamlit:

```powershell
python -m streamlit run Home.py
```

Then open the local URL displayed by Streamlit.

If port `8501` is already being used by another application:

```powershell
python -m streamlit run Home.py --server.port 8502
```

---

# 📦 Main Technologies

### Application

* Python
* Streamlit

### Data Processing

* Pandas
* NumPy

### Data Visualization

* Matplotlib
* Seaborn
* Plotly
* WordCloud

### Machine Learning

* Scikit-learn
* SciPy
* Statsmodels

### Geographic Analysis

* GeoPandas
* GeoPy

### Generative AI

* OpenAI API
* Structured preference extraction
* Grounded response generation

### Recommendation System

* Content-based recommendation
* Weighted similarity scoring
* Conversational preference profiling

---

# 🧪 Suggested Test Scenarios

The recommendation assistant can be tested using different scenarios.

### Insufficient Information

```text
I am a quiet person.
```

Expected behavior: the assistant should ask for additional information instead of immediately generating a recommendation.

### Conversational Memory

```text
I live in a small apartment.
```

Then:

```text
I am not very active.
```

Then:

```text
Barking is a deal breaker for me.
```

The final user profile should combine information from all messages.

### Irrelevant Information

```text
I love anime, video games and pizza.
My favorite color is blue.
I live in a small apartment and I am not very active.
```

Irrelevant information should not be converted into dog breed traits.

### Preference Change

```text
I want a large dog.
```

Then:

```text
Actually, I changed my mind. I would prefer a small dog.
```

The most recent explicit preference should replace the previous value.

---

# ⚠️ Limitations

The recommendation system has several important limitations:

* Recommendations depend on the completeness and accuracy of the underlying datasets.
* Natural-language statements can sometimes be ambiguous.
* OpenAI may interpret ambiguous preferences differently than the user intended.
* The visual user profile is provided so users can inspect how their preferences were interpreted.
* Match percentages represent similarity according to the project's recommendation algorithm and should **not** be interpreted as statistical probabilities.
* Size categories are simplified and based on average breed weight.
* Individual dogs can differ significantly from breed-level averages.
* Recommendations are intended for exploratory and educational purposes.
* The application does not replace professional veterinary, behavioral, or responsible dog ownership advice.

---

# 🔮 Future Improvements

Possible future improvements include:

* Retrieval-Augmented Generation (RAG) over breed descriptions
* ChromaDB for semantic breed-description retrieval
* User feedback and recommendation refinement
* Integration of clustering results with chatbot recommendations
* Persistent user profiles
* More advanced preference weighting
* Automated testing
* Deployment to a cloud platform

---

# 📚 Data Sources

The application combines multiple dog breed datasets, including:

1. Top Dog Breeds Around the World
2. Dog Breeds Dataset
3. Alternative Dog Breeds Dataset
4. American Kennel Club breed information

See `links_datasets.txt` for the original dataset references.

---


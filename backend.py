from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

dataset_context = {}

CSV_FILENAME = "cleaned_steam_games.csv" 

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Looking for local file: {CSV_FILENAME}...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, CSV_FILENAME)

    if os.path.exists(csv_path):
        try:
            # Load Data
            print("Loading CSV...")
            df = pd.read_csv(csv_path)
            
            # Clean column names
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            
            # Prepare Data for ML
            print("Preparing Machine Learning Model...")
            df['genres'] = df['genres'].fillna('')
            df['about_the_game'] = df['about_the_game'].fillna('')
            
            # Create text soup
            df['combined_features'] = df['genres'] + " " + df['about_the_game'].astype(str).str.slice(0, 500)

            # Create Matrix
            tfidf = TfidfVectorizer(stop_words='english', max_features=2000)
            feature_matrix = tfidf.fit_transform(df['combined_features'])
            
            # Save to Context
            dataset_context["df"] = df
            dataset_context["feature_matrix"] = feature_matrix
            
            print(f"Success! API is ready with {len(df)} games.")
        except Exception as e:
            print(f" Error loading data: {e}")
            dataset_context["df"] = pd.DataFrame()
    else:
        print(f" File not found at: {csv_path}")
        dataset_context["df"] = pd.DataFrame()
        
    yield
    dataset_context.clear()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#ENDPOINTS

app = FastAPI(lifespan=lifespan)

@app.api_route("/", methods=["GET", "HEAD"])
def home():
    # Render sends HEAD / to check if the service is healthy
    return {"message": "Recommendation API is Running."}


@app.get("/games")
def get_games(limit: int = 10, search: str = None):
    df = dataset_context.get("df")
    if df is None or df.empty: return []

    if search:
        filtered_df = df[df['name'].astype(str).str.contains(search, case=False, na=False)]
    else:
        filtered_df = df

    subset = filtered_df.head(limit).where(pd.notnull(filtered_df), None)
    return subset[['name']].to_dict(orient="records")

@app.get("/recommend")
def get_recommendation(game_name: str):
    df = dataset_context.get("df")
    feature_matrix = dataset_context.get("feature_matrix")
    
    if df is None or df.empty:
        raise HTTPException(status_code=500, detail="Model not loaded")

    #PARTIAL MATCHING

    # Try Exact Match First
    matches = df[df['name'].astype(str).str.lower() == game_name.lower()]
    
    # If no exact match, try Partial Match ("contains")
    if matches.empty:
        # regex=False ensures special characters like '+' or '(' don't crash it
        matches = df[df['name'].astype(str).str.lower().str.contains(game_name.lower(), regex=False)]
        
    if matches.empty:
        raise HTTPException(status_code=404, detail="Game not found")
        
    # Take the first match found (e.g. "Resident Evil 4" if input was "Resident Evil")
    idx = matches.index[0]
    matched_name = df.iloc[idx]['name'] # Get the actual full name found

    # ML LOGIC
    target_vec = feature_matrix.getrow(idx)
    sim_scores = linear_kernel(target_vec, feature_matrix).flatten()
    
    similar_idx = sim_scores.argsort()[-6:-1][::-1]
    results = df.iloc[similar_idx]
    
    results = results.where(pd.notnull(results), None)
    
    # We also return the 'matched_name' so the frontend knows which game was actually used
    response_data = results[['name', 'genres', 'about_the_game', 'price']].to_dict(orient="records")
    
    return {
        "source_game": matched_name,
        "recommendations": response_data
    }
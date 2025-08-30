# Backend (FastAPI)

## Setup
1. Install Python 3.8+
2. `pip install -r requirements.txt`
3. `uvicorn app.main:app --reload`

## API Endpoints
- `POST /predict` - Single transaction prediction
- `POST /upload` - Batch prediction via CSV

## Model
- Trained model saved in `app/model/`
- See `notebooks/eda_modeling.ipynb` for training steps

## Folder Structure
- `app/main.py` - API endpoints
- `app/model/` - Model loading & prediction
- `app/utils/` - Preprocessing helpers

## Example Request
See project README for API contracts.

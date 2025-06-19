import os
import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import xgboost as xgb
from sentence_transformers import SentenceTransformer

model_path = os.path.join(os.path.dirname(__file__), "..", "model", "minilm_model1")
model1 = SentenceTransformer(model_path)


# Load collaborative filtering model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "model.joblib")
data = joblib.load(MODEL_PATH)
cf_model = data["model"]
dataset = data["dataset"]
user_features = data["user_features"]
item_features = data["item_features"]
user_mapping = dataset.mapping()[0]
item_mapping = dataset.mapping()[2]

def contentMatching(freelancer_df, skills_vec, type_vec, desc_vec):
    freelancer_df['favproj_vec'] = model1.encode(freelancer_df['favouriteProject'].tolist(), convert_to_tensor=True).cpu().numpy().tolist()
    freelancer_df['skills_vec'] = model1.encode([" ".join(sk) for sk in freelancer_df['skills']], convert_to_tensor=True).cpu().numpy().tolist()
    freelancer_df['proposal_vec'] = model1.encode(freelancer_df['proposal'], convert_to_tensor=True).cpu().numpy().tolist()

    freelancer_df['similarity_score'] = (
        cosine_similarity(freelancer_df['favproj_vec'].tolist(), skills_vec.reshape(1, -1)).flatten() +
        cosine_similarity(freelancer_df['skills_vec'].tolist(), skills_vec.reshape(1, -1)).flatten() +
        cosine_similarity(freelancer_df['proposal_vec'].tolist(), skills_vec.reshape(1, -1)).flatten() +
        cosine_similarity(freelancer_df['proposal_vec'].tolist(), type_vec.reshape(1, -1)).flatten() +
        cosine_similarity(freelancer_df['skills_vec'].tolist(), type_vec.reshape(1, -1)).flatten() +
        cosine_similarity(freelancer_df['favproj_vec'].tolist(), type_vec.reshape(1, -1)).flatten() +
        cosine_similarity(freelancer_df['favproj_vec'].tolist(), desc_vec.reshape(1, -1)).flatten() +
        cosine_similarity(freelancer_df['skills_vec'].tolist(), desc_vec.reshape(1, -1)).flatten() +
        cosine_similarity(freelancer_df['proposal_vec'].tolist(), desc_vec.reshape(1, -1)).flatten()
    )
    freelancer_df['content_score'] = freelancer_df['similarity_score']
    return freelancer_df

def recommend_freelancers(project, freelancers):
    freelancer_df = pd.DataFrame([f.dict() for f in freelancers])

    desc_vec = model1.encode(project.description, convert_to_tensor=True)
    skills_vec = model1.encode(" ".join(project.skills), convert_to_tensor=True)
    type_vec = model1.encode(" ".join(project.projecttype), convert_to_tensor=True)

    freelancer_df = contentMatching(freelancer_df, skills_vec, type_vec, desc_vec)

    # CF score
    freelancer_df['cf_score'] = 0.0
    if project.clientId in item_mapping:
        client_internal_id = item_mapping[project.clientId]
        valid_indices = []
        cf_scores = []
        for idx, fl_id in enumerate(freelancer_df['flancerId']):
            if fl_id in user_mapping:
                internal_id = user_mapping[fl_id]
                score = cf_model.predict([internal_id], [client_internal_id],
                                         user_features=user_features,
                                         item_features=item_features)[0]
                cf_scores.append(score)
                valid_indices.append(idx)
        freelancer_df.loc[valid_indices, 'cf_score'] = cf_scores

    # Normalize + final score
    scaler = MinMaxScaler()
    freelancer_df[['content_score_norm']] = scaler.fit_transform(freelancer_df[['content_score']])
    freelancer_df[['cf_score_norm']] = scaler.fit_transform(freelancer_df[['cf_score']])
    freelancer_df['final_score'] = 0.7 * freelancer_df['content_score_norm'] + 0.3 * freelancer_df['cf_score_norm']

    # Success model
    success = pd.DataFrame({
        'flancerId': freelancer_df['flancerId'],
        'final_score': freelancer_df['final_score'],
        'bid': freelancer_df['bid'],
        'exp_timeline': freelancer_df['exp_timeline'],
        'rating': freelancer_df['rating'],
        'budget': project.budget,
        'timeline': project.timeline
    })
    success['target'] = (success['rating'] >= 4).astype(int)
    success['bid_diff'] = success['bid'] - success['budget']
    success['bid_ratio'] = success['bid'] / success['budget']
    success['timeline_diff'] = success['exp_timeline'] - success['timeline']
    success['timeline_ratio'] = success['exp_timeline'] / success['timeline']

    X = success[['final_score', 'bid_diff', 'bid_ratio', 'timeline_diff', 'timeline_ratio']]
    y = success['target']

    if y.nunique() < 2:
        # If y only contains one class (e.g., all 1s), assign constant prediction
        success['pred_proba'] = 1.0 if y.iloc[0] == 1 else 0.0
    else:
        model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        model.fit(X, y)
        success['pred_proba'] = model.predict_proba(X)[:, 1]

    return success.sort_values(by='pred_proba', ascending=False).head(10)[['flancerId', 'pred_proba']]

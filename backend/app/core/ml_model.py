import joblib

class MLModel:
    def __init__(self):
        self.df = None
        self.scaler = None
        self.knn = None
        self.X_scaled_all = None

    def load(self):
        self.df = joblib.load("app/files/df_recetas.joblib")
        self.scaler = joblib.load("app/files/scaler.joblib")
        self.knn = joblib.load("app/files/knn.joblib")

        FEATURES = ['calories', 'fat_content', 'carbohydrate_content', 'protein_content']
        self.X_scaled_all = self.scaler.transform(self.df[FEATURES])

ml_model = MLModel()
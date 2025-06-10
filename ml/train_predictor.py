# File: ml/train_predictor.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import glob
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("train_predictor")

def load_all_signals(folder="signals"):
    paths = glob.glob(os.path.join(folder, "*.json"))
    frames = []
    for path in paths:
        try:
            df = pd.read_json(path, lines=True)
            if 'signal' in df.columns:
                df['source'] = os.path.basename(path)
                frames.append(df)
        except Exception as e:
            logger.warning(f"Failed to load {path}: {e}")
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

def main():
    df = load_all_signals()
    if df.empty:
        logger.warning("No data found to train on.")
        return

    df = df.dropna(subset=['signal'])
    df['signal'] = df['signal'].astype('category').cat.codes

    X = df[['price', 'roc']] if 'roc' in df.columns else df[['price', 'ma']]
    y = df['signal']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    main()

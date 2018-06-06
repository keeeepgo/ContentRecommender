from gensim import corpora, models
import gensim.utils.SaveLoad as saveload
import pandas as pd

if __name__ == "__main__":
    rec_df = pd.DataFrame(columns=['id', 'score'])

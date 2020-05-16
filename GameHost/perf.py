from multiprocessing import Pool
import pandas as pd
import numpy as np
from functools import partial


def parallelize_dataframe(df, func, n_cores=4, param=None):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = None
    if param is None:
        df = pd.concat(pool.map(func, df_split))
    else:
        df = pd.concat(pool.map(partial(func, card_id=param), df_split))
    pool.close()
    pool.join()
    return df

# def parallelize_dataframe_extra_arg(tup, func, n_cores=4):
#
#     df, second_arg = tup
#     df_split = np.array_split(df, n_cores)
#     pool = Pool(n_cores)
#     df = pd.concat(pool.map(func, df_split))
#     pool.close()
#     pool.join()
#     return df
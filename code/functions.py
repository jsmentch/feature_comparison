def load_features_ns():
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt
    %matplotlib inline
    import seaborn as sns
    sns.set("paper", "white")
    from pyns import Neuroscout
    api = Neuroscout()
    run_id=api.runs.get(dataset_id=27, subject='sid000005',number=1)[0]['id']
    run_duration=api.runs.get(dataset_id=27, subject='sid000005',number=1)[0]['duration']
    budapest_predictors=api.predictors.get(run_id=run_id)
    budapest_predictor_ids = []
    budapest_predictor_names = []
    budapest_predictor_modality = []

    for i in budapest_predictors:
        if not i['source'] == 'fmriprep' and not i['mean'] == None:
            budapest_predictor_ids.append(i['id'])
            budapest_predictor_names.append(i['name'])
            try:
                budapest_predictor_modality.append(i['extracted_feature']['modality'])
            except:
                budapest_predictor_modality.append(None)

    df_predictors=pd.DataFrame(data= np.array([budapest_predictor_ids,budapest_predictor_modality,budapest_predictor_names]).T , columns=['id','modality','names'])
    df_predictors = df_predictors.sort_values(by=['id','names','modality'])
    budapest_predictor_ids= df_predictors['id'].to_numpy()
    budapest_predictor_names= df_predictors['names'].to_numpy()
    budapest_predictor_modality= df_predictors['modality'].to_numpy()


    import math
    all_feats = []
    for pred_id in budapest_predictor_ids:
        an_event=api.predictor_events.get(predictor_id=pred_id,run_id=run_id,stimulus_timing=True)
        data = np.zeros((int(run_duration)))
        for i in an_event:
            start = round(i['onset'])
            stop = start + math.ceil(i['duration'])
            value = i['value']
            #onset=round(onset)
            try:
                data[start:stop]=value
            except:
                #print()
                print(f'skipped {value}')

        all_feats.append(data)
    #all_feats is length = # predictors each predictor is size = run duration

    all_feats = np.asarray(all_feats)

    import dcor
    result = df.apply(lambda col1: df.apply(lambda col2: dcor.distance_correlation(col1, col2)))
    return(budapest_predictor_ids,
           budapest_predictor_names,
           budapest_predictor_modality,
           all_feats,
           df_predictors)
"""Small fixed-regularization logistic predictor implemented with NumPy only."""
import numpy as np

L2=10.0
METHODS=('global_rate','model_prompt','taxonomy','interface','structure')


def sigmoid(x):
    return 1/(1+np.exp(-np.clip(x,-35,35)))


def encoder(rows,numeric,taxonomy=False):
    raw=np.array([[r['features'][k] for k in numeric] for r in rows],dtype=float)
    means=raw.mean(axis=0) if numeric else np.array([])
    scales=raw.std(axis=0) if numeric else np.array([])
    scales=np.where(scales<1e-8,1,scales)
    return dict(numeric=list(numeric),means=means.tolist(),scales=scales.tolist(),
                contexts=sorted({r['model']+'|'+r['phase'] for r in rows}),
                categories=sorted({r['mechanism'] for r in rows}) if taxonomy else [])


def transform(rows,enc):
    # IDs for games/targets/families/seeds never enter this design matrix.
    values=[]
    for r in rows:
        numeric=[(r['features'][k]-m)/s for k,m,s in zip(enc['numeric'],enc['means'],enc['scales'])]
        context=r['model']+'|'+r['phase']
        values.append([1.]+numeric+[float(context==c) for c in enc['contexts']]+
                      [float(r['mechanism']==c) for c in enc['categories']])
    return np.asarray(values,dtype=float)


def fit(rows,method,game_features,witness_features):
    assert method in METHODS and rows
    y=np.asarray([r['y'] for r in rows],dtype=float)
    if method=='global_rate' or len(set(y))<2:
        return dict(method=method,constant=float((y.sum()+1)/(len(y)+2)))
    numeric=(list(game_features) if method=='interface' else
             list(game_features)+list(witness_features) if method=='structure' else [])
    enc=encoder(rows,numeric,method=='taxonomy');x=transform(rows,enc)
    beta=np.zeros(x.shape[1]);beta[0]=np.log((y.sum()+1)/(len(y)-y.sum()+1))
    penalty=np.ones(len(beta))*L2;penalty[0]=0
    def objective(b):
        z=x@b
        return float(np.sum(np.logaddexp(0,z)-y*z)+.5*np.sum(penalty*b*b))
    for iteration in range(80):
        prob=sigmoid(x@beta);w=np.maximum(prob*(1-prob),1e-8)
        gradient=x.T@(prob-y)+penalty*beta
        hessian=x.T@(w[:,None]*x)+np.diag(penalty+1e-8)
        step=np.linalg.solve(hessian,gradient);before=objective(beta);scale=1.
        while scale>1e-8 and objective(beta-scale*step)>before:scale*=.5
        beta-=scale*step
        if np.max(np.abs(scale*step))<1e-7:break
    return dict(method=method,encoder=enc,beta=beta.tolist(),l2=L2,iterations=iteration+1,
                max_abs_gradient=float(np.max(np.abs(x.T@(sigmoid(x@beta)-y)+penalty*beta))))


def predict(artifact,rows):
    if 'constant' in artifact:return np.full(len(rows),artifact['constant'])
    return sigmoid(transform(rows,artifact['encoder'])@np.array(artifact['beta']))


def make_folds(rows,scheme):
    field='game' if scheme=='edition' else 'family' if scheme=='family' else 'mechanism'
    for group in sorted({r[field] for r in rows}):
        test=[i for i,r in enumerate(rows) if r[field]==group]
        forbidden_families={rows[i]['family'] for i in test} if scheme=='mechanism_purged_family' else set()
        train=[i for i,r in enumerate(rows) if r[field]!=group and r['family'] not in forbidden_families]
        assert train and test
        assert not {rows[i]['target'] for i in test} & {rows[i]['target'] for i in train}
        if scheme in ('family','mechanism_purged_family'):
            assert not {rows[i]['family'] for i in test} & {rows[i]['family'] for i in train}
        yield group,train,test


def losses(y,prob):
    y=np.asarray(y);prob=np.clip(prob,1e-6,1-1e-6)
    return (prob-y)**2,-y*np.log(prob)-(1-y)*np.log(1-prob)

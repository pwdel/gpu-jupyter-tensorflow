# TODO LIST

* MLOPS: Install sklearn via conda in image
* MLOPS: Install matplotlib via conda in image
* MLOPS: Install QuantLib-Python
* MLOPS: Install arch
* MLOPS: Install numpy
* MLOPS: Install datasets bitsandbytes einops wandb
* MLOPS: Install trl transformers accelerate git+https://github.com/huggingface/peft.git
* MLOPS: Fix /opt/conda/envs/tf_gpu_env/lib/python3.9/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html
* MLOPS: Do we need to store JupyterLab logs?

* APP: User search utility by user_id
* APP: Username search utility by username
* APP: User profit analysis

* DS: Create PCA/Kmeans analysis preserving market_id information.
* DS: Tweak and Improve PCA/Kmeans Analysis, better PCA explination of variance
* DS: Run functions on much larger database
* DS: Output CLUSTER and MARKET_TITLE to a huge dict list which we can use to train an LLM
* DS: Hook up falcon7GB to notebook, run it
* DS: Train falcon7GB on notebook, with a very small dataset, maybe 10 or so entries.
* DS: After evaluating the above short trained LLM, go for a larger training set.
* DS: Test using fine-tuned LLM with prompt to try to qualify/predict an incoming market by CLUSTER
* DS: Explore dealing with sparce data, e.g. convert feature from dense to sparce maybe to improve/tweak if needed

* DS: Market volatility tool
* DS: Market volatility by cluster

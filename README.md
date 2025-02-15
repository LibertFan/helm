<!--intro-start-->
# Holistic Evaluation of Language Models

[comment]: <> (When using the img tag, which allows us to specify size, src has to be a URL.)
<img src="https://github.com/stanford-crfm/helm/raw/main/src/helm/benchmark/static/images/helm-logo.png" alt=""  width="800"/>

Welcome! The **`crfm-helm`** Python package contains code used in the **Holistic Evaluation of Language Models** project ([paper](https://arxiv.org/abs/2211.09110), [website](https://crfm.stanford.edu/helm/latest/)) by [Stanford CRFM](https://crfm.stanford.edu/). This package includes the following features:

- Collection of datasets in a standard format (e.g., NaturalQuestions)
- Collection of models accessible via a unified API (e.g., GPT-3, MT-NLG, OPT, BLOOM)
- Collection of metrics beyond accuracy (efficiency, bias, toxicity, etc.)
- Collection of perturbations for evaluating robustness and fairness (e.g., typos, dialect)
- Modular framework for constructing prompts from datasets
- Proxy server for managing accounts and providing unified interface to access models
<!--intro-end-->

To get started, refer to [the documentation on Read the Docs](https://crfm-helm.readthedocs.io/) for how to install and run the package.

# 安装

- 从 dockerhub 上下载 docker: nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04\
- 在命令行执行下面的程序
```
conda create -n crfm-helm python=3.8 pip
conda activate crfm-helm
git clone git@github.com:LibertFan/helm.git
cd helm
pip install -r requirements.txt
./pre-commit.sh
```

# Tips

## 添加评测数据集
- 在 src/helm/benchmark/scenarios 文件夹下面创建对应的文件和scenario名称
- 在 src/helm/benchmark/scenarios/\_\_init\_\_.py 当中加入对应的路径
- 在 src/helm/benchmark/run_specs.py 当中加入对应的 run_spec_function
- 在 src/helm/benchmark/static/schema.yaml 当中加入 dataset card

## 评测模型
### huggingface远程模型
- 找到 huggingface model 的名字 zzz
- 运行命令运行 
```
CUDA_VISIBLE_DEVICES=0 helm-run \
    --conf-paths commands/run_xxx.conf \
    --suite yyy --max-eval-instances 10000 \
    --enable-huggingface-models zzz \
    -n 1 
```
### 本地模型
- 将模型 zzz 放在 examples/disc_llms 当中
- 运行命令 
```
CUDA_VISIBLE_DEVICES=0 helm-run \
    --conf-paths commands/run_xxx.conf \
    --suite yyy --max-eval-instances 10000 \
    --enable-huggingface-models disc_llms/zzz \
    -n 1 
```
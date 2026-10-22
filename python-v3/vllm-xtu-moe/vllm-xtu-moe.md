# vllm-xtu-moe

> 标签: Python

## 简介

XTU (X Transformers Unity) — a mainline-vLLM hybrid MoE plugin (CPU experts + GPU attention/long prefill). Bundles the xiaotu CPU MoE engine (AVX512-VNNI/BF16: MXFP4/FP8/INT4/BF16) so no-AMX x86 hosts (AMD EPYC) get usable CPU MoE backends through FusedMoEFactory.

## 官网

- 官网：https://pypi.org/project/vllm-xtu-moe/
- PyPI 项目页：https://pypi.org/project/vllm-xtu-moe/

## 历史版本号

- 当前版本：0.2.7

- 0.2.7

## 获取地址

- pip 安装：`pip install vllm-xtu-moe`
- 下载页面：https://pypi.org/project/vllm-xtu-moe/#files
- 运行要求：Python >=3.12

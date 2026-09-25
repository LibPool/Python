# Python 库索引

本目录收录来自 PyPI 的 Python 库索引，按大版本与发行包名路径组织：

- 版本目录：`python-v3`（当前唯一收录的大版本，覆盖 Python 3 生态）
- 包路径：`python-v3/<包名>/<包名>.md`
- 当前共收录 55019 个 PyPI 项目，来源为 PyPI simple index 全量枚举与人工种子。

## 数据源

- PyPI simple index：https://pypi.org/simple/（全量项目列表）
- PyPI JSON API：https://pypi.org/pypi/<package>/json
- PyPI 官网：https://pypi.org/

## 生成方式

```bash
python tools/build_seed_list.py
python tools/generate_index.py --crawl --crawl-limit 60000 --workers 32
```

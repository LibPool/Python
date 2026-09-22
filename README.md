# Python 库索引

本目录收录来自 PyPI 的 Python 库索引，按发行包名路径组织：

- 版本目录：`python-v3`（当前种子以 Python 3 生态为主）
- 包路径：`python-v3/<包名>/<包名>.md`
- 当前共收录 236 个 PyPI 项目，覆盖 Web、数据科学、AI、云原生、测试、安全等常见领域。

## 数据源

- PyPI JSON API：https://pypi.org/pypi/<package>/json
- PyPI 官网：https://pypi.org/

## 生成方式

```bash
python tools/build_seed_list.py
python tools/generate_index.py
```

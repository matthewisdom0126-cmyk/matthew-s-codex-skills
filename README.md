# Matthew 的 Codex 用户技能

记录最近自行安装的 **3 套技能，共 179 个独立技能**，供另一台电脑恢复。
不包含 Codex 自带的 `.system` 技能，也不包含应用管理的插件缓存。

| 最近安装的集合 | 独立技能数量 | 来源 |
| --- | ---: | --- |
| Academic Research Skills 的 Codex 版 | 1：`academic-research-suite` | [原仓库](https://github.com/Imbad0202/academic-research-skills-codex) |
| Scientific Agent Skills | 177 | [原仓库](https://github.com/K-Dense-AI/scientific-agent-skills) |
| RPlot | 1：`rplot` | [原仓库](https://github.com/XiaoLi1991-star/plot_skills) |

179 个中的 177 个来自 Scientific Agent Skills 的整套安装，并不是 Codex 自带技能。

## 最方便的恢复方式

在另一台电脑的 Codex 中发送：

> 请从 https://github.com/matthewisdom0126-cmyk/matthew-s-codex-skills 按 skills-lock.json 安装我自行安装的三套技能，使用清单中的固定提交和全部技能路径，不安装 Codex 自带技能。已有技能保留并报告版本差异。

## 自己运行恢复脚本

需要 Codex、Python 3.9 或更新版本、Git 和 GitHub 网络连接：

```powershell
git clone https://github.com/matthewisdom0126-cmyk/matthew-s-codex-skills.git
cd matthew-s-codex-skills
python restore.py --dry-run
python restore.py
```

macOS / Linux 可把 `python` 换成 `python3`。如果系统没有 Python 命令，可让 Codex 使用应用自带的 Python 执行。
恢复后开启新的 Codex 对话，例如使用 `$academic-research-suite` 或 `$rplot`。

默认使用 `$CODEX_HOME/skills`，未设置时使用 `~/.codex/skills`。
可用 `--dest "目标技能目录"` 修改位置，或用 `--installer "install-skill-from-github.py 的路径"` 指定 Codex 技能安装工具。
恢复脚本调用 Codex 自带安装工具；自带工具仅用于执行安装，不会被上传或复制。

## 版本与范围

- `skills-lock.json` 固定本次安装的 3 个上游提交及 179 个路径，不随上游更新而改变。
- 本仓库保存安装清单和恢复脚本，技能原文件在恢复时从原作者 GitHub 仓库下载，因此恢复需要网络。
- 已有同名技能会跳过，不覆盖；脚本会提示这些版本未经核对。清单中的固定版本适用于新安装的技能。
- 不同步登录凭据、API 密钥、聊天、论文或机器设置。
- R、科学计算扩展包、系统工具和外部服务密钥仍需按实际工作流配置。
- 不自动监控后续本机变更；新增或修改技能后需更新本仓库的清单。
- 技能版权与许可归原作者所有，以各源仓库及各技能的许可为准。ARS 有非商业许可条件。

清单日期：2026-11-07。

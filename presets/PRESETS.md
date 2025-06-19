# GPTContext Presets

This document describes each of the built-in configuration presets you can pass via `--config-file presets/<name>.yml`.

## Table of presets

| Preset | Short Description |
| ------ | ----------------- |
| [allcode](#allcode) | Maximum code coverage — capture ALL source-like files |
| [android](#android) | Android project (Java + Kotlin + Gradle) |
| [ansible](#ansible) | Ansible playbook / role repo |
| [audit](#audit) | Optimized for security audit — show configs, envs, keys, secrets |
| [backend_only](#backend_only) | Backend app only — API / server code |
| [bashops](#bashops) | Bash / Shell scripts / DevOps repo |
| [cdk_csharp](#cdk_csharp) | AWS CDK — C# (.NET) project |
| [cdk_java](#cdk_java) | AWS CDK — Java project |
| [cdk_py](#cdk_py) | AWS CDK — Python project |
| [cdk_ts](#cdk_ts) | AWS CDK — TypeScript project |
| [clojure](#clojure) | Clojure project (Leiningen / deps.edn / Babashka) |
| [cpp](#cpp) | C / C++ project |
| [datapipeline](#datapipeline) | Data pipeline / ETL project |
| [datascience](#datascience) | Python Data Science / ML / Notebook project |
| [default](#default) | Default preset for GPTContext |
| [design_docs](#design_docs) | Design docs only — textual / documentation content |
| [docs](#docs) | Docs / static site / knowledge base |
| [dotnet](#dotnet) | .NET Core project (C# + configs) |
| [flutter](#flutter) | Flutter / Dart project |
| [frontend_only](#frontend_only) | Frontend app only — React, Vue, JS/TS |
| [github_actions](#github_actions) | GitHub Actions / CI/CD repo |
| [golang](#golang) | Go project |
| [haskell](#haskell) | Haskell project (Stack or Cabal) |
| [hdl](#hdl) | FPGA / HDL (Verilog, VHDL, SystemVerilog) |
| [helm](#helm) | Helm chart repo (Kubernetes YAML + Helm templates) |
| [infra_only](#infra_only) | Infra only — IaC configs (Terraform, Ansible, Helm, K8s YAML) |
| [java](#java) | Java project (e.g. Maven or Gradle) |
| [kong](#kong) | API Gateway / Kong / NGINX config repo |
| [laravel](#laravel) | Laravel (PHP) project |
| [latex](#latex) | LaTeX / scientific writing project |
| [minimal](#minimal) | Minimal config — safest default, good as a base template |
| [monorepo](#monorepo) | Monorepo - multiple languages / tools |
| [phoenix](#phoenix) | Elixir / Phoenix project |
| [python](#python) | Pure Python project |
| [rails](#rails) | Ruby on Rails project |
| [react](#react) | React project (JS/TS + HTML + CSS) |
| [reactnative](#reactnative) | React Native / Ionic app |
| [review_only](#review_only) | Review only preset for code projects |
| [rust](#rust) | Rust project (Cargo) |
| [solidity](#solidity) | Blockchain / Solidity project (smart contracts) |
| [splunkapp](#splunkapp) | Python Splunk App (e.g. modular input or Add-on Builder app) |
| [terraform](#terraform) | Terraform / Infrastructure-as-Code (IaC) project |
| [tests_only](#tests_only) | Tests only — capture test files and configs |
| [typescript_node](#typescript_node) | Node.js / TypeScript app |
| [unity](#unity) | Unity game project (C# + Unity YAML + configs) |
| [unreal](#unreal) | Unreal Engine project |
| [vue](#vue) | Vue.js project |
| [webapp](#webapp) | Python webapp (FastAPI, Django, Flask, etc.) |

## allcode

[View YAML →](./allcode.yml)

This preset is designed to capture a wide range of source code files across various programming languages and formats.
It includes common extensions for languages like Python, JavaScript, TypeScript, Go, Java, Kotlin, Rust, C/C++, C#, Swift,
PHP, Ruby, Perl, Shell scripts, SQL, Terraform, YAML, JSON, XML, HTML, CSS, and more.
The preset also excludes common directories that typically contain build artifacts or dependencies.

**Include extensions:** `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.go`, `.java`, `.kt`, `.rs`, `.cpp`, `.c`, `.h`, `.hpp`, `.cs`, `.swift`, `.php`, `.rb`, `.pl`, `.sh`, `.bash`, `.zsh`, `.sql`, `.tf`, `.yaml`, `.yml`, `.json`, `.toml`, `.xml`, `.html`, `.css`, `.scss`, `.sass`, `.ini`, `.cfg`, `.md`, `.txt`

**Exclude patterns:** `.git/`, `node_modules/`, `vendor/`, `dist/`, `build/`, `bin/`, `obj/`, `target/`, `.venv/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 20000
MAX_FILE_TOKENS: 5000
description: "Maximum code coverage \u2014 capture ALL source-like files"
long_description: 'This preset is designed to capture a wide range of source code
  files across various programming languages and formats.

  It includes common extensions for languages like Python, JavaScript, TypeScript,
  Go, Java, Kotlin, Rust, C/C++, C#, Swift,

  PHP, Ruby, Perl, Shell scripts, SQL, Terraform, YAML, JSON, XML, HTML, CSS, and
  more.

  The preset also excludes common directories that typically contain build artifacts
  or dependencies.

  '
exclude:
- .git/
- node_modules/
- vendor/
- dist/
- build/
- bin/
- obj/
- target/
- .venv/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .py
- .js
- .jsx
- .ts
- .tsx
- .go
- .java
- .kt
- .rs
- .cpp
- .c
- .h
- .hpp
- .cs
- .swift
- .php
- .rb
- .pl
- .sh
- .bash
- .zsh
- .sql
- .tf
- .yaml
- .yml
- .json
- .toml
- .xml
- .html
- .css
- .scss
- .sass
- .ini
- .cfg
- .md
- .txt
use_default_excludes: true
```

## android

[View YAML →](./android.yml)

This preset is tailored for Android projects, focusing on Java and Kotlin source files, along with
Gradle build scripts. It includes common file extensions used in Android development and excludes directories
that typically contain build artifacts or IDE-specific configurations. The preset is designed to capture the essential
source files while avoiding unnecessary clutter from dependencies and build outputs.

**Include extensions:** `.java`, `.kt`, `.xml`, `.gradle`, `.md`, `.json`, `.yml`, `.yaml`, `.txt`

**Exclude patterns:** `.git/`, `.idea/`, `.vscode/`, `build/`, `.gradle/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: Android project (Java + Kotlin + Gradle)
long_description: 'This preset is tailored for Android projects, focusing on Java
  and Kotlin source files, along with

  Gradle build scripts. It includes common file extensions used in Android development
  and excludes directories

  that typically contain build artifacts or IDE-specific configurations. The preset
  is designed to capture the essential

  source files while avoiding unnecessary clutter from dependencies and build outputs.

  '
exclude:
- .git/
- .idea/
- .vscode/
- build/
- .gradle/
- .gptcontext-cache/
include_exts:
- .java
- .kt
- .xml
- .gradle
- .md
- .json
- .yml
- .yaml
- .txt
use_default_excludes: true
```

## ansible

[View YAML →](./ansible.yml)

This preset is designed for Ansible playbooks and roles, focusing on YAML files and Jinja2 templates.
It includes common file extensions used in Ansible development and excludes directories that typically
contain temporary files, artifacts, or IDE-specific configurations. The preset is tailored to capture the
essential source files while avoiding unnecessary clutter from dependencies and build outputs.

**Include extensions:** `.yaml`, `.yml`, `.j2`, `.json`, `.md`, `.txt`, `.sh`

**Exclude patterns:** `.git/`, `.gptcontext-cache/`, `.idea/`, `.vscode/`, `tmp/`, `artifacts/`, `.ansible/`

```yaml
MAX_TOTAL_TOKENS: 12000
MAX_FILE_TOKENS: 3000
description: Ansible playbook / role repo
long_description: 'This preset is designed for Ansible playbooks and roles, focusing
  on YAML files and Jinja2 templates.

  It includes common file extensions used in Ansible development and excludes directories
  that typically

  contain temporary files, artifacts, or IDE-specific configurations. The preset is
  tailored to capture the

  essential source files while avoiding unnecessary clutter from dependencies and
  build outputs.

  '
exclude:
- .git/
- .gptcontext-cache/
- .idea/
- .vscode/
- tmp/
- artifacts/
- .ansible/
include_exts:
- .yaml
- .yml
- .j2
- .json
- .md
- .txt
- .sh
use_default_excludes: true
```

## audit

[View YAML →](./audit.yml)

This preset is designed for security audits, focusing on configuration files, environment variables,
keys, and secrets. It includes common file extensions used for configuration and environment files,
while excluding directories that typically contain build artifacts, dependencies, or other non-essential files.

**Include extensions:** `.env`, `.yaml`, `.yml`, `.json`, `.toml`, `.ini`, `.cfg`, `.xml`, `.properties`, `.conf`, `.sh`, `.bash`, `.zsh`, `.md`, `.txt`, `.pem`, `.crt`, `.key`

**Exclude patterns:** `.git/`, `node_modules/`, `dist/`, `build/`, `vendor/`, `public/`, `static/`, `data/`, `tmp/`, `logs/`, `.venv/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: "Optimized for security audit \u2014 show configs, envs, keys, secrets"
long_description: 'This preset is designed for security audits, focusing on configuration
  files, environment variables,

  keys, and secrets. It includes common file extensions used for configuration and
  environment files,

  while excluding directories that typically contain build artifacts, dependencies,
  or other non-essential files.

  '
exclude:
- .git/
- node_modules/
- dist/
- build/
- vendor/
- public/
- static/
- data/
- tmp/
- logs/
- .venv/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .env
- .yaml
- .yml
- .json
- .toml
- .ini
- .cfg
- .xml
- .properties
- .conf
- .sh
- .bash
- .zsh
- .md
- .txt
- .pem
- .crt
- .key
use_default_excludes: true
```

## backend_only

[View YAML →](./backend_only.yml)

This preset is designed for backend applications, focusing on server-side code and API implementations.
It includes common file extensions used in backend development across various languages such as Python, Go,
Java, Kotlin, Rust, C/C++, C#, PHP, Ruby, and more.

**Include extensions:** `.py`, `.go`, `.java`, `.kt`, `.rs`, `.cpp`, `.c`, `.h`, `.cs`, `.php`, `.rb`, `.yaml`, `.yml`, `.json`, `.ini`, `.cfg`, `.md`, `.txt`

**Exclude patterns:** `.git/`, `node_modules/`, `dist/`, `build/`, `public/`, `static/`, `tmp/`, `data/`, `.venv/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: "Backend app only \u2014 API / server code"
long_description: 'This preset is designed for backend applications, focusing on server-side
  code and API implementations.

  It includes common file extensions used in backend development across various languages
  such as Python, Go,

  Java, Kotlin, Rust, C/C++, C#, PHP, Ruby, and more.

  '
exclude:
- .git/
- node_modules/
- dist/
- build/
- public/
- static/
- tmp/
- data/
- .venv/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .py
- .go
- .java
- .kt
- .rs
- .cpp
- .c
- .h
- .cs
- .php
- .rb
- .yaml
- .yml
- .json
- .ini
- .cfg
- .md
- .txt
use_default_excludes: true
```

## bashops

[View YAML →](./bashops.yml)

This preset is designed for Bash and Shell scripts, focusing on DevOps-related files. 
It includes common file extensions used in shell scripting and DevOps workflows, while 
excluding directories that typically contain build artifacts, dependencies, or other 
non-essential files. The preset is tailored to capture the essential scripts and 
configuration files while avoiding unnecessary clutter from temporary files and 
IDE-specific configurations.

**Include extensions:** `.sh`, `.bash`, `.zsh`, `.yaml`, `.yml`, `.md`, `.json`, `.txt`

**Exclude patterns:** `.git/`, `.gptcontext-cache/`, `tmp/`, `logs/`, `.idea/`, `.vscode/`

```yaml
MAX_TOTAL_TOKENS: 12000
MAX_FILE_TOKENS: 4000
description: Bash / Shell scripts / DevOps repo
long_description: "This preset is designed for Bash and Shell scripts, focusing on\
  \ DevOps-related files. \nIt includes common file extensions used in shell scripting\
  \ and DevOps workflows, while \nexcluding directories that typically contain build\
  \ artifacts, dependencies, or other \nnon-essential files. The preset is tailored\
  \ to capture the essential scripts and \nconfiguration files while avoiding unnecessary\
  \ clutter from temporary files and \nIDE-specific configurations.  \n"
exclude:
- .git/
- .gptcontext-cache/
- tmp/
- logs/
- .idea/
- .vscode/
include_exts:
- .sh
- .bash
- .zsh
- .yaml
- .yml
- .md
- .json
- .txt
use_default_excludes: true
```

## cdk_csharp

[View YAML →](./cdk_csharp.yml)

This preset is designed for AWS CDK projects using C# (.NET). It focuses on
capturing the essential source files, configuration files, and scripts while excluding
directories that typically contain build artifacts, dependencies, or IDE-specific configurations.

**Include extensions:** `.cs`, `.csproj`, `.json`, `.yaml`, `.yml`, `.md`, `.txt`, `.sh`

**Exclude patterns:** `.git/`, `bin/`, `obj/`, `cdk.out/`, `dist/`, `build/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: "AWS CDK \u2014 C# (.NET) project"
long_description: 'This preset is designed for AWS CDK projects using C# (.NET). It
  focuses on

  capturing the essential source files, configuration files, and scripts while excluding

  directories that typically contain build artifacts, dependencies, or IDE-specific
  configurations.

  '
exclude:
- .git/
- bin/
- obj/
- cdk.out/
- dist/
- build/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .cs
- .csproj
- .json
- .yaml
- .yml
- .md
- .txt
- .sh
use_default_excludes: true
```

## cdk_java

[View YAML →](./cdk_java.yml)

This preset is designed for AWS CDK projects using Java. It focuses on capturing the essential
source files, configuration files, and scripts while excluding directories that typically contain
build artifacts, dependencies, or IDE-specific configurations. The preset is tailored to ensure that
the core Java files, along with relevant configuration and script files, are included while avoiding
unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.java`, `.xml`, `.json`, `.yaml`, `.yml`, `.md`, `.txt`, `.sh`

**Exclude patterns:** `.git/`, `target/`, `cdk.out/`, `dist/`, `build/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: "AWS CDK \u2014 Java project"
long_description: 'This preset is designed for AWS CDK projects using Java. It focuses
  on capturing the essential

  source files, configuration files, and scripts while excluding directories that
  typically contain

  build artifacts, dependencies, or IDE-specific configurations. The preset is tailored
  to ensure that

  the core Java files, along with relevant configuration and script files, are included
  while avoiding

  unnecessary clutter from temporary files and build outputs.

  '
exclude:
- .git/
- target/
- cdk.out/
- dist/
- build/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .java
- .xml
- .json
- .yaml
- .yml
- .md
- .txt
- .sh
use_default_excludes: true
```

## cdk_py

[View YAML →](./cdk_py.yml)

This preset is designed for AWS CDK projects using Python. It focuses on capturing the essential
source files, configuration files, and scripts while excluding directories that typically contain
build artifacts, dependencies, or IDE-specific configurations. The preset is tailored to ensure that
the core Python files, along with relevant configuration and script files, are included while avoiding
unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.py`, `.json`, `.yaml`, `.yml`, `.md`, `.txt`, `.sh`

**Exclude patterns:** `.git/`, `.venv/`, `cdk.out/`, `dist/`, `build/`, `.idea/`, `.vscode/`, `__pycache__/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: "AWS CDK \u2014 Python project"
long_description: 'This preset is designed for AWS CDK projects using Python. It focuses
  on capturing the essential

  source files, configuration files, and scripts while excluding directories that
  typically contain

  build artifacts, dependencies, or IDE-specific configurations. The preset is tailored
  to ensure that

  the core Python files, along with relevant configuration and script files, are included
  while avoiding

  unnecessary clutter from temporary files and build outputs.

  '
exclude:
- .git/
- .venv/
- cdk.out/
- dist/
- build/
- .idea/
- .vscode/
- __pycache__/
- .gptcontext-cache/
include_exts:
- .py
- .json
- .yaml
- .yml
- .md
- .txt
- .sh
use_default_excludes: true
```

## cdk_ts

[View YAML →](./cdk_ts.yml)

This preset is designed for AWS CDK projects using TypeScript. It focuses on capturing the essential
source files, configuration files, and scripts while excluding directories that typically contain
build artifacts, dependencies, or IDE-specific configurations. The preset is tailored to ensure that
the core TypeScript files, along with relevant configuration and script files, are included while avoiding
unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.ts`, `.tsx`, `.json`, `.yaml`, `.yml`, `.md`, `.txt`, `.js`, `.sh`

**Exclude patterns:** `.git/`, `node_modules/`, `cdk.out/`, `dist/`, `build/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: "AWS CDK \u2014 TypeScript project"
long_description: 'This preset is designed for AWS CDK projects using TypeScript.
  It focuses on capturing the essential

  source files, configuration files, and scripts while excluding directories that
  typically contain

  build artifacts, dependencies, or IDE-specific configurations. The preset is tailored
  to ensure that

  the core TypeScript files, along with relevant configuration and script files, are
  included while avoiding

  unnecessary clutter from temporary files and build outputs.

  '
exclude:
- .git/
- node_modules/
- cdk.out/
- dist/
- build/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .ts
- .tsx
- .json
- .yaml
- .yml
- .md
- .txt
- .js
- .sh
use_default_excludes: true
```

## clojure

[View YAML →](./clojure.yml)

This preset is tailored for Clojure projects, focusing on source files and configuration files
used in common Clojure build tools like Leiningen and deps.edn. It includes common file extensions
used in Clojure development and excludes directories that typically contain build artifacts,
dependencies, or IDE-specific configurations. The preset is designed to capture the essential
source files while avoiding unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.clj`, `.cljs`, `.cljc`, `.edn`, `.md`, `.yaml`, `.yml`, `.json`, `.txt`

**Exclude patterns:** `.git/`, `target/`, `out/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 12000
MAX_FILE_TOKENS: 4000
description: Clojure project (Leiningen / deps.edn / Babashka)
long_description: 'This preset is tailored for Clojure projects, focusing on source
  files and configuration files

  used in common Clojure build tools like Leiningen and deps.edn. It includes common
  file extensions

  used in Clojure development and excludes directories that typically contain build
  artifacts,

  dependencies, or IDE-specific configurations. The preset is designed to capture
  the essential

  source files while avoiding unnecessary clutter from temporary files and build outputs.

  '
exclude:
- .git/
- target/
- out/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .clj
- .cljs
- .cljc
- .edn
- .md
- .yaml
- .yml
- .json
- .txt
use_default_excludes: true
```

## cpp

[View YAML →](./cpp.yml)

This preset is designed for C and C++ projects, focusing on source files, headers,
and configuration files. It includes common file extensions used in C/C++ development
and excludes directories that typically contain build artifacts, dependencies, or IDE-specific 
configurations.

**Include extensions:** `.c`, `.cpp`, `.cc`, `.h`, `.hpp`, `.md`, `.yaml`, `.yml`, `.json`, `.txt`, `.cmake`, `CMakeLists.txt`

**Exclude patterns:** `.git/`, `build/`, `bin/`, `obj/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 12000
MAX_FILE_TOKENS: 4000
description: C / C++ project
long_description: "This preset is designed for C and C++ projects, focusing on source\
  \ files, headers,\nand configuration files. It includes common file extensions used\
  \ in C/C++ development\nand excludes directories that typically contain build artifacts,\
  \ dependencies, or IDE-specific \nconfigurations.\n"
exclude:
- .git/
- build/
- bin/
- obj/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .c
- .cpp
- .cc
- .h
- .hpp
- .md
- .yaml
- .yml
- .json
- .txt
- .cmake
- CMakeLists.txt
use_default_excludes: true
```

## datapipeline

[View YAML →](./datapipeline.yml)

This preset is designed for data pipeline or ETL projects, focusing on Python scripts, SQL files,
configuration files, and data files. It includes common file extensions used in data processing
and excludes directories that typically contain data outputs, temporary files, or IDE-specific configurations.
The preset is tailored to capture the essential scripts and configuration files while avoiding unnecessary clutter
from dependencies and build outputs.

**Include extensions:** `.py`, `.sql`, `.json`, `.yaml`, `.yml`, `.csv`, `.parquet`, `.ipynb`, `.md`, `.txt`, `.sh`

**Exclude patterns:** `.git/`, `data/`, `tmp/`, `logs/`, `output/`, `.venv/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: Data pipeline / ETL project
long_description: 'This preset is designed for data pipeline or ETL projects, focusing
  on Python scripts, SQL files,

  configuration files, and data files. It includes common file extensions used in
  data processing

  and excludes directories that typically contain data outputs, temporary files, or
  IDE-specific configurations.

  The preset is tailored to capture the essential scripts and configuration files
  while avoiding unnecessary clutter

  from dependencies and build outputs.

  '
exclude:
- .git/
- data/
- tmp/
- logs/
- output/
- .venv/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .py
- .sql
- .json
- .yaml
- .yml
- .csv
- .parquet
- .ipynb
- .md
- .txt
- .sh
use_default_excludes: true
```

## datascience

[View YAML →](./datascience.yml)

This preset is designed for Python-based data science, machine learning, and notebook projects.
It focuses on capturing essential Python scripts, Jupyter notebooks, configuration files, and data files
while excluding directories that typically contain virtual environments, temporary files, or IDE-specific 
configurations.

**Include extensions:** `.py`, `.ipynb`, `.md`, `.toml`, `.yaml`, `.yml`, `.json`, `.csv`, `.txt`, `.ini`, `.cfg`, `.Rmd`, `.R`

**Exclude patterns:** `.git/`, `.venv/`, `dist/`, `build/`, `.mypy_cache/`, `.pytest_cache/`, `.vscode/`, `.idea/`, `.gptcontext-cache/`, `.ipynb_checkpoints/`, `output/`, `data/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: Python Data Science / ML / Notebook project
long_description: "This preset is designed for Python-based data science, machine\
  \ learning, and notebook projects.\nIt focuses on capturing essential Python scripts,\
  \ Jupyter notebooks, configuration files, and data files\nwhile excluding directories\
  \ that typically contain virtual environments, temporary files, or IDE-specific\
  \ \nconfigurations.\n"
exclude:
- .git/
- .venv/
- dist/
- build/
- .mypy_cache/
- .pytest_cache/
- .vscode/
- .idea/
- .gptcontext-cache/
- .ipynb_checkpoints/
- output/
- data/
include_exts:
- .py
- .ipynb
- .md
- .toml
- .yaml
- .yml
- .json
- .csv
- .txt
- .ini
- .cfg
- .Rmd
- .R
use_default_excludes: true
```

## default

[View YAML →](./default.yml)

This preset is designed to capture a wide range of file types and configurations
commonly found in software projects. It includes various programming languages, configuration files,
and documentation formats, while excluding directories that typically contain build artifacts,
dependencies, or IDE-specific configurations. The preset aims to provide a comprehensive context
for understanding the project without unnecessary clutter from temporary files or non-essential directories.

**Include extensions:** `.py`, `.md`, `.js`, `.ts`, `.jsx`, `.tsx`, `.json`, `.toml`, `.yaml`, `.yml`, `.html`, `.css`, `.scss`, `.sass`, `.less`, `.java`, `.go`, `.rs`, `.cpp`, `.c`, `.h`, `.hpp`, `.cs`, `.swift`, `.kt`, `.m`, `.sh`, `.bash`, `.zsh`, `.ps1`, `.pl`, `.rb`, `.php`, `.ini`, `.cfg`, `.env`, `.txt`, `.xml`

**Exclude patterns:** `.git/`, `.svn/`, `.hg/`, `node_modules/`, `__pycache__/`, `dist/`, `build/`, `.venv/`, `env/`, `.mypy_cache/`, `.pytest_cache/`, `.vscode/`, `.idea/`, `.gptcontext-cache/`, `.DS_Store/`, `__snapshots__/`, `.coverage/`, `.cache/`, `.gptcontext.txt`, `.gptcontext_message.txt`, `README.md`, `CHANGELOG.md`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`

```yaml
MAX_TOTAL_TOKENS: 12000
MAX_FILE_TOKENS: 5000
MAX_FILE_SIZE_MB: 1
BASE_DIR: .
CONTEXT_OUTPUT_FILENAME: .gptcontext.txt
MESSAGE_OUTPUT_FILENAME: .gptcontext_message.txt
GPTCONTEXT_CACHE_DIRNAME: .gptcontext-cache
OPENAI_MODEL: gpt-3.5-turbo
ENCODING_NAME: cl100k_base
description: Default preset for GPTContext
long_description: 'This preset is designed to capture a wide range of file types and
  configurations

  commonly found in software projects. It includes various programming languages,
  configuration files,

  and documentation formats, while excluding directories that typically contain build
  artifacts,

  dependencies, or IDE-specific configurations. The preset aims to provide a comprehensive
  context

  for understanding the project without unnecessary clutter from temporary files or
  non-essential directories.

  '
exclude:
- .git/
- .svn/
- .hg/
- node_modules/
- __pycache__/
- dist/
- build/
- .venv/
- env/
- .mypy_cache/
- .pytest_cache/
- .vscode/
- .idea/
- .gptcontext-cache/
- .DS_Store/
- __snapshots__/
- .coverage/
- .cache/
- .gptcontext.txt
- .gptcontext_message.txt
- README.md
- CHANGELOG.md
- LICENSE
- CONTRIBUTING.md
- CODE_OF_CONDUCT.md
- SECURITY.md
include_exts:
- .py
- .md
- .js
- .ts
- .jsx
- .tsx
- .json
- .toml
- .yaml
- .yml
- .html
- .css
- .scss
- .sass
- .less
- .java
- .go
- .rs
- .cpp
- .c
- .h
- .hpp
- .cs
- .swift
- .kt
- .m
- .sh
- .bash
- .zsh
- .ps1
- .pl
- .rb
- .php
- .ini
- .cfg
- .env
- .txt
- .xml
use_default_excludes: true
```

## design_docs

[View YAML →](./design_docs.yml)

This preset is tailored for design documents and textual content, focusing on formats commonly used for documentation
and design specifications. It includes common file extensions used in documentation while excluding directories
that typically contain code, build artifacts, or other non-documentation files. The preset is designed to capture the essential
textual content while avoiding unnecessary clutter from code repositories or temporary files.

**Include extensions:** `.md`, `.markdown`, `.txt`, `.rst`, `.adoc`, `.yaml`, `.yml`, `.json`

**Exclude patterns:** `.git/`, `node_modules/`, `dist/`, `build/`, `public/`, `static/`, `tmp/`, `data/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 20000
MAX_FILE_TOKENS: 5000
description: "Design docs only \u2014 textual / documentation content"
long_description: 'This preset is tailored for design documents and textual content,
  focusing on formats commonly used for documentation

  and design specifications. It includes common file extensions used in documentation
  while excluding directories

  that typically contain code, build artifacts, or other non-documentation files.
  The preset is designed to capture the essential

  textual content while avoiding unnecessary clutter from code repositories or temporary
  files.

  '
exclude:
- .git/
- node_modules/
- dist/
- build/
- public/
- static/
- tmp/
- data/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .md
- .markdown
- .txt
- .rst
- .adoc
- .yaml
- .yml
- .json
use_default_excludes: true
```

## docs

[View YAML →](./docs.yml)

This preset is designed for documentation, static sites, or knowledge bases. It focuses on
capturing essential documentation files, configuration files, and scripts while excluding directories
that typically contain build artifacts, dependencies, or IDE-specific configurations. The preset is tailored
to ensure that the core documentation files, along with relevant configuration and script files, are included
while avoiding unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.md`, `.markdown`, `.html`, `.yaml`, `.yml`, `.json`, `.txt`, `.rst`

**Exclude patterns:** `.git/`, `node_modules/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`, `dist/`, `build/`, `public/`, `static/`

```yaml
MAX_TOTAL_TOKENS: 20000
MAX_FILE_TOKENS: 4000
description: Docs / static site / knowledge base
long_description: 'This preset is designed for documentation, static sites, or knowledge
  bases. It focuses on

  capturing essential documentation files, configuration files, and scripts while
  excluding directories

  that typically contain build artifacts, dependencies, or IDE-specific configurations.
  The preset is tailored

  to ensure that the core documentation files, along with relevant configuration and
  script files, are included

  while avoiding unnecessary clutter from temporary files and build outputs.

  '
exclude:
- .git/
- node_modules/
- .idea/
- .vscode/
- .gptcontext-cache/
- dist/
- build/
- public/
- static/
include_exts:
- .md
- .markdown
- .html
- .yaml
- .yml
- .json
- .txt
- .rst
use_default_excludes: true
```

## dotnet

[View YAML →](./dotnet.yml)

This preset is designed for .NET Core projects, focusing on C# source files, 
configuration files, and project files. It includes common file extensions used 
in .NET development and excludes directories that typically contain build artifacts, 
dependencies, or IDE-specific configurations. The preset is designed to capture the
essential source files while avoiding unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.cs`, `.csproj`, `.sln`, `.json`, `.yaml`, `.yml`, `.md`, `.txt`, `.xml`, `.config`

**Exclude patterns:** `.git/`, `bin/`, `obj/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: .NET Core project (C# + configs)
long_description: "This preset is designed for .NET Core projects, focusing on C#\
  \ source files, \nconfiguration files, and project files. It includes common file\
  \ extensions used \nin .NET development and excludes directories that typically\
  \ contain build artifacts, \ndependencies, or IDE-specific configurations. The preset\
  \ is designed to capture the\nessential source files while avoiding unnecessary\
  \ clutter from temporary files and build outputs.\n"
exclude:
- .git/
- bin/
- obj/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .cs
- .csproj
- .sln
- .json
- .yaml
- .yml
- .md
- .txt
- .xml
- .config
use_default_excludes: true
```

## flutter

[View YAML →](./flutter.yml)

This preset is designed for Flutter projects, focusing on Dart source files, configuration files,
and other relevant files. It includes common file extensions used in Flutter development and excludes directories
that typically contain build artifacts, dependencies, or IDE-specific configurations. The preset is designed to capture the essential
source files while avoiding unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.dart`, `.yaml`, `.yml`, `.md`, `.json`, `.html`, `.css`, `.txt`

**Exclude patterns:** `.git/`, `build/`, `.dart_tool/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`, `.packages/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: Flutter / Dart project
long_description: 'This preset is designed for Flutter projects, focusing on Dart
  source files, configuration files,

  and other relevant files. It includes common file extensions used in Flutter development
  and excludes directories

  that typically contain build artifacts, dependencies, or IDE-specific configurations.
  The preset is designed to capture the essential

  source files while avoiding unnecessary clutter from temporary files and build outputs.

  '
exclude:
- .git/
- build/
- .dart_tool/
- .idea/
- .vscode/
- .gptcontext-cache/
- .packages/
include_exts:
- .dart
- .yaml
- .yml
- .md
- .json
- .html
- .css
- .txt
use_default_excludes: true
```

## frontend_only

[View YAML →](./frontend_only.yml)

This preset is designed for frontend applications, focusing on JavaScript and TypeScript codebases.
It includes common file extensions used in modern frontend development, such as React and Vue components,
and excludes directories that typically contain build artifacts, dependencies, or IDE-specific configurations.

**Include extensions:** `.js`, `.jsx`, `.ts`, `.tsx`, `.vue`, `.json`, `.yaml`, `.yml`, `.html`, `.css`, `.scss`, `.sass`, `.md`, `.txt`

**Exclude patterns:** `.git/`, `node_modules/`, `dist/`, `build/`, `public/`, `static/`, `coverage/`, `.cache/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: "Frontend app only \u2014 React, Vue, JS/TS"
long_description: 'This preset is designed for frontend applications, focusing on
  JavaScript and TypeScript codebases.

  It includes common file extensions used in modern frontend development, such as
  React and Vue components,

  and excludes directories that typically contain build artifacts, dependencies, or
  IDE-specific configurations.

  '
exclude:
- .git/
- node_modules/
- dist/
- build/
- public/
- static/
- coverage/
- .cache/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .js
- .jsx
- .ts
- .tsx
- .vue
- .json
- .yaml
- .yml
- .html
- .css
- .scss
- .sass
- .md
- .txt
use_default_excludes: true
```

## github_actions

[View YAML →](./github_actions.yml)

This preset is designed for GitHub Actions and CI/CD repositories, focusing on YAML files
and configuration files. It includes common file extensions used in CI/CD workflows and excludes
directories that typically contain build artifacts, dependencies, or IDE-specific configurations.

**Include extensions:** `.yaml`, `.yml`, `.json`, `.md`, `.txt`, `.sh`

**Exclude patterns:** `.git/`, `.gptcontext-cache/`, `node_modules/`, `dist/`, `build/`, `.idea/`, `.vscode/`

```yaml
MAX_TOTAL_TOKENS: 12000
MAX_FILE_TOKENS: 4000
description: GitHub Actions / CI/CD repo
long_description: 'This preset is designed for GitHub Actions and CI/CD repositories,
  focusing on YAML files

  and configuration files. It includes common file extensions used in CI/CD workflows
  and excludes

  directories that typically contain build artifacts, dependencies, or IDE-specific
  configurations.

  '
exclude:
- .git/
- .gptcontext-cache/
- node_modules/
- dist/
- build/
- .idea/
- .vscode/
include_exts:
- .yaml
- .yml
- .json
- .md
- .txt
- .sh
use_default_excludes: true
```

## golang

[View YAML →](./golang.yml)

This preset is designed for Go projects, focusing on Go source files, module files, and
configuration files. It includes common file extensions used in Go development and excludes directories
that typically contain build artifacts, dependencies, or IDE-specific configurations. The preset is designed to capture the essential
source files while avoiding unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.go`, `.mod`, `.sum`, `.md`, `.json`, `.yaml`, `.yml`, `.txt`

**Exclude patterns:** `.git/`, `vendor/`, `dist/`, `build/`, `.gptcontext-cache/`, `.vscode/`, `.idea/`

```yaml
MAX_TOTAL_TOKENS: 10000
MAX_FILE_TOKENS: 4000
description: Go project
long_description: 'This preset is designed for Go projects, focusing on Go source
  files, module files, and

  configuration files. It includes common file extensions used in Go development and
  excludes directories

  that typically contain build artifacts, dependencies, or IDE-specific configurations.
  The preset is designed to capture the essential

  source files while avoiding unnecessary clutter from temporary files and build outputs.

  '
exclude:
- .git/
- vendor/
- dist/
- build/
- .gptcontext-cache/
- .vscode/
- .idea/
include_exts:
- .go
- .mod
- .sum
- .md
- .json
- .yaml
- .yml
- .txt
use_default_excludes: true
```

## haskell

[View YAML →](./haskell.yml)

This preset is tailored for Haskell projects, focusing on source files and configuration files
used in common Haskell build tools like Stack and Cabal. It includes common file extensions
used in Haskell development and excludes directories that typically contain build artifacts,
dependencies, or IDE-specific configurations. The preset is designed to capture the essential
source files while avoiding unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.hs`, `.lhs`, `.cabal`, `.yaml`, `.yml`, `.md`, `.json`, `.txt`

**Exclude patterns:** `.git/`, `dist/`, `.stack-work/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 12000
MAX_FILE_TOKENS: 4000
description: Haskell project (Stack or Cabal)
long_description: 'This preset is tailored for Haskell projects, focusing on source
  files and configuration files

  used in common Haskell build tools like Stack and Cabal. It includes common file
  extensions

  used in Haskell development and excludes directories that typically contain build
  artifacts,

  dependencies, or IDE-specific configurations. The preset is designed to capture
  the essential

  source files while avoiding unnecessary clutter from temporary files and build outputs.

  '
exclude:
- .git/
- dist/
- .stack-work/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .hs
- .lhs
- .cabal
- .yaml
- .yml
- .md
- .json
- .txt
use_default_excludes: true
```

## hdl

[View YAML →](./hdl.yml)

This preset is tailored for FPGA and HDL projects, focusing on source files and configuration files
used in common HDL development. It includes common file extensions used in Verilog, VHDL, and SystemVerilog development
and excludes directories that typically contain build artifacts, simulation outputs, or IDE-specific configurations.
The preset is designed to capture the essential source files while avoiding unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.v`, `.vh`, `.sv`, `.svh`, `.vhd`, `.vhdl`, `.xdc`, `.md`, `.txt`, `.yaml`, `.yml`, `.json`

**Exclude patterns:** `.git/`, `build/`, `work/`, `sim/`, `xsim.dir/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 12000
MAX_FILE_TOKENS: 4000
description: FPGA / HDL (Verilog, VHDL, SystemVerilog)
long_description: 'This preset is tailored for FPGA and HDL projects, focusing on
  source files and configuration files

  used in common HDL development. It includes common file extensions used in Verilog,
  VHDL, and SystemVerilog development

  and excludes directories that typically contain build artifacts, simulation outputs,
  or IDE-specific configurations.

  The preset is designed to capture the essential source files while avoiding unnecessary
  clutter from temporary files and build outputs.

  '
exclude:
- .git/
- build/
- work/
- sim/
- xsim.dir/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .v
- .vh
- .sv
- .svh
- .vhd
- .vhdl
- .xdc
- .md
- .txt
- .yaml
- .yml
- .json
use_default_excludes: true
```

## helm

[View YAML →](./helm.yml)

This preset is designed for Helm chart repositories, focusing on Kubernetes YAML files and Helm templates.
It includes common file extensions used in Helm development and excludes directories that typically contain
build artifacts, temporary files, or IDE-specific configurations. The preset is tailored to capture the
essential Helm chart files while avoiding unnecessary clutter from dependencies and build outputs.

**Include extensions:** `.yaml`, `.yml`, `.tpl`, `.md`, `.txt`, `.sh`, `Chart.yaml`, `values.yaml`

**Exclude patterns:** `.git/`, `charts/`, `tmp/`, `.helmignore/`, `.gptcontext-cache/`, `.idea/`, `.vscode/`

```yaml
MAX_TOTAL_TOKENS: 12000
MAX_FILE_TOKENS: 3000
description: Helm chart repo (Kubernetes YAML + Helm templates)
long_description: 'This preset is designed for Helm chart repositories, focusing on
  Kubernetes YAML files and Helm templates.

  It includes common file extensions used in Helm development and excludes directories
  that typically contain

  build artifacts, temporary files, or IDE-specific configurations. The preset is
  tailored to capture the

  essential Helm chart files while avoiding unnecessary clutter from dependencies
  and build outputs.

  '
exclude:
- .git/
- charts/
- tmp/
- .helmignore/
- .gptcontext-cache/
- .idea/
- .vscode/
include_exts:
- .yaml
- .yml
- .tpl
- .md
- .txt
- .sh
- Chart.yaml
- values.yaml
use_default_excludes: true
```

## infra_only

[View YAML →](./infra_only.yml)

This preset is designed for infrastructure-only projects, focusing on Infrastructure as Code (IaC)
configurations such as Terraform, Ansible, Helm, and Kubernetes YAML files. It captures essential
configuration files while excluding directories that typically contain build artifacts, dependencies,
or IDE-specific configurations. The preset is designed to ensure that only relevant infrastructure files
are included, avoiding unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.tf`, `.tfvars`, `.yaml`, `.yml`, `.json`, `.tpl`, `.j2`, `.sh`, `.md`, `.txt`

**Exclude patterns:** `.git/`, `node_modules/`, `dist/`, `build/`, `bin/`, `tmp/`, `.terraform/`, `.venv/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: "Infra only \u2014 IaC configs (Terraform, Ansible, Helm, K8s YAML)"
long_description: 'This preset is designed for infrastructure-only projects, focusing
  on Infrastructure as Code (IaC)

  configurations such as Terraform, Ansible, Helm, and Kubernetes YAML files. It captures
  essential

  configuration files while excluding directories that typically contain build artifacts,
  dependencies,

  or IDE-specific configurations. The preset is designed to ensure that only relevant
  infrastructure files

  are included, avoiding unnecessary clutter from temporary files and build outputs.

  '
exclude:
- .git/
- node_modules/
- dist/
- build/
- bin/
- tmp/
- .terraform/
- .venv/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .tf
- .tfvars
- .yaml
- .yml
- .json
- .tpl
- .j2
- .sh
- .md
- .txt
use_default_excludes: true
```

## java

[View YAML →](./java.yml)

This preset is designed for Java projects, focusing on source files and configuration files
used in common Java build tools like Maven and Gradle. It includes common file extensions
used in Java development and excludes directories that typically contain build artifacts,
dependencies, or IDE-specific configurations. The preset is designed to capture the essential
source files while avoiding unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.java`, `.xml`, `.md`, `.properties`, `.yaml`, `.yml`, `.json`, `.gradle`, `.groovy`, `.txt`

**Exclude patterns:** `.git/`, `target/`, `build/`, `.idea/`, `.vscode/`, `.gradle/`, `.gptcontext-cache/`, `out/`

```yaml
MAX_TOTAL_TOKENS: 12000
MAX_FILE_TOKENS: 4000
description: Java project (e.g. Maven or Gradle)
long_description: 'This preset is designed for Java projects, focusing on source files
  and configuration files

  used in common Java build tools like Maven and Gradle. It includes common file extensions

  used in Java development and excludes directories that typically contain build artifacts,

  dependencies, or IDE-specific configurations. The preset is designed to capture
  the essential

  source files while avoiding unnecessary clutter from temporary files and build outputs.

  '
exclude:
- .git/
- target/
- build/
- .idea/
- .vscode/
- .gradle/
- .gptcontext-cache/
- out/
include_exts:
- .java
- .xml
- .md
- .properties
- .yaml
- .yml
- .json
- .gradle
- .groovy
- .txt
use_default_excludes: true
```

## kong

[View YAML →](./kong.yml)

This preset is designed for API Gateway configurations, specifically for Kong and NGINX.
It focuses on capturing essential configuration files, Lua scripts, and related documentation,
while excluding directories that typically contain logs, temporary files, or IDE-specific configurations.
The preset is tailored to ensure that the core configuration files and scripts are included while avoiding
unnecessary clutter from non-essential files.

**Include extensions:** `.yaml`, `.yml`, `.json`, `.conf`, `.lua`, `.md`, `.txt`, `.sh`

**Exclude patterns:** `.git/`, `logs/`, `tmp/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 12000
MAX_FILE_TOKENS: 4000
description: API Gateway / Kong / NGINX config repo
long_description: 'This preset is designed for API Gateway configurations, specifically
  for Kong and NGINX.

  It focuses on capturing essential configuration files, Lua scripts, and related
  documentation,

  while excluding directories that typically contain logs, temporary files, or IDE-specific
  configurations.

  The preset is tailored to ensure that the core configuration files and scripts are
  included while avoiding

  unnecessary clutter from non-essential files.

  '
exclude:
- .git/
- logs/
- tmp/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .yaml
- .yml
- .json
- .conf
- .lua
- .md
- .txt
- .sh
use_default_excludes: true
```

## laravel

[View YAML →](./laravel.yml)

This preset is designed for Laravel projects, focusing on PHP source files, Blade templates, and
configuration files. It includes common file extensions used in Laravel development and excludes directories
that typically contain build artifacts, dependencies, or IDE-specific configurations. The preset is designed to capture the essential
source files while avoiding unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.php`, `.blade.php`, `.js`, `.json`, `.md`, `.yaml`, `.yml`, `.env`, `.html`, `.scss`, `.css`, `.txt`

**Exclude patterns:** `.git/`, `vendor/`, `node_modules/`, `storage/`, `bootstrap/cache/`, `dist/`, `build/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: Laravel (PHP) project
long_description: 'This preset is designed for Laravel projects, focusing on PHP source
  files, Blade templates, and

  configuration files. It includes common file extensions used in Laravel development
  and excludes directories

  that typically contain build artifacts, dependencies, or IDE-specific configurations.
  The preset is designed to capture the essential

  source files while avoiding unnecessary clutter from temporary files and build outputs.

  '
exclude:
- .git/
- vendor/
- node_modules/
- storage/
- bootstrap/cache/
- dist/
- build/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .php
- .blade.php
- .js
- .json
- .md
- .yaml
- .yml
- .env
- .html
- .scss
- .css
- .txt
use_default_excludes: true
```

## latex

[View YAML →](./latex.yml)

This preset is designed for LaTeX projects, focusing on capturing the essential source files,
configuration files, and scripts while excluding directories that typically contain build artifacts,
dependencies, or IDE-specific configurations. The preset is tailored to ensure that the core LaTeX files,
along with relevant configuration and script files, are included while avoiding unnecessary clutter
from temporary files and build outputs. It includes common file extensions used in LaTeX projects
and excludes directories that are not relevant to the source code, such as build directories and IDE
configurations.

**Include extensions:** `.tex`, `.bib`, `.cls`, `.sty`, `.md`, `.yaml`, `.yml`, `.json`, `.txt`, `.pdf`

**Exclude patterns:** `.git/`, `build/`, `out/`, `_minted-*/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: LaTeX / scientific writing project
long_description: 'This preset is designed for LaTeX projects, focusing on capturing
  the essential source files,

  configuration files, and scripts while excluding directories that typically contain
  build artifacts,

  dependencies, or IDE-specific configurations. The preset is tailored to ensure that
  the core LaTeX files,

  along with relevant configuration and script files, are included while avoiding
  unnecessary clutter

  from temporary files and build outputs. It includes common file extensions used
  in LaTeX projects

  and excludes directories that are not relevant to the source code, such as build
  directories and IDE

  configurations.

  '
exclude:
- .git/
- build/
- out/
- _minted-*/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .tex
- .bib
- .cls
- .sty
- .md
- .yaml
- .yml
- .json
- .txt
- .pdf
use_default_excludes: true
```

## minimal

[View YAML →](./minimal.yml)

This preset is designed to provide a minimal configuration suitable for various projects.
It focuses on capturing essential source files and configuration files while excluding
directories that typically contain build artifacts, dependencies, or IDE-specific configurations.
The preset is tailored to ensure that core files are included while avoiding unnecessary clutter
from temporary files and build outputs. It includes common file extensions used in many projects
and excludes directories that are not relevant to the source code, such as build directories and IDE
configurations. This makes it a good starting point for various types of projects, including Python,
JavaScript, and general software development.

**Include extensions:** `.py`, `.md`, `.txt`, `.json`, `.yaml`, `.yml`

**Exclude patterns:** `.git/`, `node_modules/`, `build/`, `dist/`, `.venv/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 8000
MAX_FILE_TOKENS: 2000
description: "Minimal config \u2014 safest default, good as a base template"
long_description: 'This preset is designed to provide a minimal configuration suitable
  for various projects.

  It focuses on capturing essential source files and configuration files while excluding

  directories that typically contain build artifacts, dependencies, or IDE-specific
  configurations.

  The preset is tailored to ensure that core files are included while avoiding unnecessary
  clutter

  from temporary files and build outputs. It includes common file extensions used
  in many projects

  and excludes directories that are not relevant to the source code, such as build
  directories and IDE

  configurations. This makes it a good starting point for various types of projects,
  including Python,

  JavaScript, and general software development.

  '
exclude:
- .git/
- node_modules/
- build/
- dist/
- .venv/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .py
- .md
- .txt
- .json
- .yaml
- .yml
use_default_excludes: true
```

## monorepo

[View YAML →](./monorepo.yml)

This preset is designed for monorepos that contain multiple languages or tools. It captures
essential source files, configuration files, and scripts while excluding directories that
typically contain build artifacts, dependencies, or IDE-specific configurations. The preset
is flexible to accommodate various programming languages and tools commonly found in monorepos.

**Include extensions:** `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.go`, `.java`, `.kt`, `.rs`, `.cpp`, `.c`, `.h`, `.md`, `.json`, `.toml`, `.yaml`, `.yml`, `.sh`, `.html`, `.css`, `.tf`, `.tfvars`

**Exclude patterns:** `.git/`, `node_modules/`, `vendor/`, `dist/`, `build/`, `target/`, `bin/`, `obj/`, `.venv/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 20000
MAX_FILE_TOKENS: 5000
description: Monorepo - multiple languages / tools
long_description: 'This preset is designed for monorepos that contain multiple languages
  or tools. It captures

  essential source files, configuration files, and scripts while excluding directories
  that

  typically contain build artifacts, dependencies, or IDE-specific configurations.
  The preset

  is flexible to accommodate various programming languages and tools commonly found
  in monorepos.

  '
exclude:
- .git/
- node_modules/
- vendor/
- dist/
- build/
- target/
- bin/
- obj/
- .venv/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .py
- .js
- .ts
- .jsx
- .tsx
- .go
- .java
- .kt
- .rs
- .cpp
- .c
- .h
- .md
- .json
- .toml
- .yaml
- .yml
- .sh
- .html
- .css
- .tf
- .tfvars
use_default_excludes: true
```

## phoenix

[View YAML →](./phoenix.yml)

This preset is designed for Elixir projects, particularly those using the Phoenix framework. 
It focuses on capturing the essential source files, configuration files, and scripts while 
excluding directories that typically contain build artifacts, dependencies, or IDE-specific 
configurations. The preset is tailored to ensure that the core Elixir files,

**Include extensions:** `.ex`, `.exs`, `.eex`, `.leex`, `.heex`, `.js`, `.json`, `.yaml`, `.yml`, `.html`, `.scss`, `.css`, `.md`, `.txt`

**Exclude patterns:** `.git/`, `_build/`, `deps/`, `node_modules/`, `priv/static/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: Elixir / Phoenix project
long_description: "This preset is designed for Elixir projects, particularly those\
  \ using the Phoenix framework. \nIt focuses on capturing the essential source files,\
  \ configuration files, and scripts while \nexcluding directories that typically\
  \ contain build artifacts, dependencies, or IDE-specific \nconfigurations. The preset\
  \ is tailored to ensure that the core Elixir files,\n"
exclude:
- .git/
- _build/
- deps/
- node_modules/
- priv/static/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .ex
- .exs
- .eex
- .leex
- .heex
- .js
- .json
- .yaml
- .yml
- .html
- .scss
- .css
- .md
- .txt
use_default_excludes: true
```

## python

[View YAML →](./python.yml)

This preset is designed for pure Python projects, focusing on source files, configuration files,
and scripts. It includes common file extensions used in Python development and excludes directories
that typically contain build artifacts, dependencies, or IDE-specific configurations. The preset is designed to capture the essential
source files while avoiding unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.py`, `.toml`, `.yaml`, `.yml`, `.json`, `.md`, `.txt`, `.ini`, `.cfg`, `.sh`

**Exclude patterns:** `.git/`, `__pycache__/`, `.venv/`, `dist/`, `build/`, `.pytest_cache/`, `.mypy_cache/`, `.vscode/`, `.idea/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 12000
MAX_FILE_TOKENS: 5000
description: Pure Python project
long_description: 'This preset is designed for pure Python projects, focusing on source
  files, configuration files,

  and scripts. It includes common file extensions used in Python development and excludes
  directories

  that typically contain build artifacts, dependencies, or IDE-specific configurations.
  The preset is designed to capture the essential

  source files while avoiding unnecessary clutter from temporary files and build outputs.

  '
exclude:
- .git/
- __pycache__/
- .venv/
- dist/
- build/
- .pytest_cache/
- .mypy_cache/
- .vscode/
- .idea/
- .gptcontext-cache/
include_exts:
- .py
- .toml
- .yaml
- .yml
- .json
- .md
- .txt
- .ini
- .cfg
- .sh
use_default_excludes: true
```

## rails

[View YAML →](./rails.yml)

This preset is designed for Ruby on Rails projects. It focuses on capturing the essential
source files, configuration files, and scripts while excluding directories that typically contain
build artifacts, dependencies, or IDE-specific configurations. The preset is tailored to ensure that
the core Ruby files, along with relevant configuration and script files, are included while avoiding
unnecessary clutter from temporary files and build outputs. It includes common file extensions used in
Rails projects and excludes directories that are not relevant to the source code, such as log files
and temporary files.

**Include extensions:** `.rb`, `.erb`, `.haml`, `.slim`, `.js`, `.json`, `.yml`, `.yaml`, `.md`, `.html`, `.scss`, `.css`, `.txt`

**Exclude patterns:** `.git/`, `log/`, `tmp/`, `node_modules/`, `vendor/`, `public/assets/`, `storage/`, `.bundle/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: Ruby on Rails project
long_description: 'This preset is designed for Ruby on Rails projects. It focuses
  on capturing the essential

  source files, configuration files, and scripts while excluding directories that
  typically contain

  build artifacts, dependencies, or IDE-specific configurations. The preset is tailored
  to ensure that

  the core Ruby files, along with relevant configuration and script files, are included
  while avoiding

  unnecessary clutter from temporary files and build outputs. It includes common file
  extensions used in

  Rails projects and excludes directories that are not relevant to the source code,
  such as log files

  and temporary files.

  '
exclude:
- .git/
- log/
- tmp/
- node_modules/
- vendor/
- public/assets/
- storage/
- .bundle/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .rb
- .erb
- .haml
- .slim
- .js
- .json
- .yml
- .yaml
- .md
- .html
- .scss
- .css
- .txt
use_default_excludes: true
```

## react

[View YAML →](./react.yml)

This preset is designed for React projects, focusing on JavaScript and TypeScript source files,
along with HTML and CSS files. It includes common file extensions used in React development and excludes
directories that typically contain build artifacts, dependencies, or IDE-specific configurations. The preset is designed to capture the essential
source files while avoiding unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.js`, `.jsx`, `.ts`, `.tsx`, `.json`, `.md`, `.html`, `.css`, `.scss`, `.sass`, `.yml`, `.yaml`

**Exclude patterns:** `.git/`, `node_modules/`, `dist/`, `build/`, `coverage/`, `.cache/`, `.gptcontext-cache/`, `.idea/`, `.vscode/`, `public/static/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: React project (JS/TS + HTML + CSS)
long_description: 'This preset is designed for React projects, focusing on JavaScript
  and TypeScript source files,

  along with HTML and CSS files. It includes common file extensions used in React
  development and excludes

  directories that typically contain build artifacts, dependencies, or IDE-specific
  configurations. The preset is designed to capture the essential

  source files while avoiding unnecessary clutter from temporary files and build outputs.

  '
exclude:
- .git/
- node_modules/
- dist/
- build/
- coverage/
- .cache/
- .gptcontext-cache/
- .idea/
- .vscode/
- public/static/
include_exts:
- .js
- .jsx
- .ts
- .tsx
- .json
- .md
- .html
- .css
- .scss
- .sass
- .yml
- .yaml
use_default_excludes: true
```

## reactnative

[View YAML →](./reactnative.yml)

This preset is designed for React Native or Ionic applications, focusing on JavaScript and TypeScript
source files, along with HTML and CSS files. It includes common file extensions used in React Native and Ionic development
and excludes directories that typically contain build artifacts, dependencies, or IDE-specific configurations.
The preset is designed to capture the essential source files while avoiding unnecessary clutter from temporary files
and build outputs.

**Include extensions:** `.js`, `.jsx`, `.ts`, `.tsx`, `.json`, `.yaml`, `.yml`, `.html`, `.css`, `.scss`, `.md`, `.txt`

**Exclude patterns:** `.git/`, `node_modules/`, `android/build/`, `ios/build/`, `ios/Pods/`, `dist/`, `build/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: React Native / Ionic app
long_description: 'This preset is designed for React Native or Ionic applications,
  focusing on JavaScript and TypeScript

  source files, along with HTML and CSS files. It includes common file extensions
  used in React Native and Ionic development

  and excludes directories that typically contain build artifacts, dependencies, or
  IDE-specific configurations.

  The preset is designed to capture the essential source files while avoiding unnecessary
  clutter from temporary files

  and build outputs.

  '
exclude:
- .git/
- node_modules/
- android/build/
- ios/build/
- ios/Pods/
- dist/
- build/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .js
- .jsx
- .ts
- .tsx
- .json
- .yaml
- .yml
- .html
- .css
- .scss
- .md
- .txt
use_default_excludes: true
```

## review_only

[View YAML →](./review_only.yml)

This preset is designed for code review purposes, focusing on source files and configuration files
while excluding directories that typically contain build artifacts, dependencies, or large data files.
It is tailored to ensure that only the essential files needed for code review are included, avoiding
unnecessary clutter from temporary files, build outputs, and large assets. This preset is ideal for
reviewing code changes, configurations, and scripts without the overhead of large data files or
non-essential directories.

**Include extensions:** `.py`, `.js`, `.ts`, `.java`, `.go`, `.cpp`, `.c`, `.h`, `.kt`, `.cs`, `.php`, `.rb`, `.sh`, `.yaml`, `.yml`, `.json`, `.toml`, `.xml`, `.cfg`, `.ini`, `.md`, `.txt`

**Exclude patterns:** `.git/`, `node_modules/`, `vendor/`, `dist/`, `build/`, `bin/`, `obj/`, `target/`, `data/`, `datasets/`, `images/`, `public/`, `static/`, `tmp/`, `logs/`, `.venv/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 12000
MAX_FILE_TOKENS: 4000
description: Review only preset for code projects
long_description: 'This preset is designed for code review purposes, focusing on source
  files and configuration files

  while excluding directories that typically contain build artifacts, dependencies,
  or large data files.

  It is tailored to ensure that only the essential files needed for code review are
  included, avoiding

  unnecessary clutter from temporary files, build outputs, and large assets. This
  preset is ideal for

  reviewing code changes, configurations, and scripts without the overhead of large
  data files or

  non-essential directories.

  '
exclude:
- .git/
- node_modules/
- vendor/
- dist/
- build/
- bin/
- obj/
- target/
- data/
- datasets/
- images/
- public/
- static/
- tmp/
- logs/
- .venv/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .py
- .js
- .ts
- .java
- .go
- .cpp
- .c
- .h
- .kt
- .cs
- .php
- .rb
- .sh
- .yaml
- .yml
- .json
- .toml
- .xml
- .cfg
- .ini
- .md
- .txt
use_default_excludes: true
```

## rust

[View YAML →](./rust.yml)

This preset is tailored for Rust projects using Cargo as the build system. It focuses on capturing
the essential source files, configuration files, and scripts while excluding directories that typically
contain build artifacts, dependencies, or IDE-specific configurations. The preset is designed to ensure
that the core Rust files, along with relevant configuration and script files, are included while avoiding
unnecessary clutter from temporary files and build outputs. It includes common file extensions used in Rust
projects and excludes directories that are not relevant to the source code, such as build directories
and IDE configurations.

**Include extensions:** `.rs`, `.toml`, `.md`, `.yaml`, `.yml`, `.json`, `.txt`

**Exclude patterns:** `.git/`, `target/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 10000
MAX_FILE_TOKENS: 4000
description: Rust project (Cargo)
long_description: 'This preset is tailored for Rust projects using Cargo as the build
  system. It focuses on capturing

  the essential source files, configuration files, and scripts while excluding directories
  that typically

  contain build artifacts, dependencies, or IDE-specific configurations. The preset
  is designed to ensure

  that the core Rust files, along with relevant configuration and script files, are
  included while avoiding

  unnecessary clutter from temporary files and build outputs. It includes common file
  extensions used in Rust

  projects and excludes directories that are not relevant to the source code, such
  as build directories

  and IDE configurations.

  '
exclude:
- .git/
- target/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .rs
- .toml
- .md
- .yaml
- .yml
- .json
- .txt
use_default_excludes: true
```

## solidity

[View YAML →](./solidity.yml)

This preset is designed for Solidity projects, particularly those involving smart contracts on blockchain platforms.
It focuses on capturing the essential source files, configuration files, and scripts while excluding directories
that typically contain build artifacts, dependencies, or IDE-specific configurations. The preset is tailored to
ensure that the core Solidity files, along with relevant configuration and script files, are included while
avoiding unnecessary clutter from temporary files and build outputs. It includes common file extensions used in
Solidity projects and excludes directories that are not relevant to the source code, such as build directories
and IDE configurations.

**Include extensions:** `.sol`, `.js`, `.ts`, `.json`, `.yaml`, `.yml`, `.md`, `.txt`, `.env`

**Exclude patterns:** `.git/`, `node_modules/`, `build/`, `artifacts/`, `cache/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: Blockchain / Solidity project (smart contracts)
long_description: 'This preset is designed for Solidity projects, particularly those
  involving smart contracts on blockchain platforms.

  It focuses on capturing the essential source files, configuration files, and scripts
  while excluding directories

  that typically contain build artifacts, dependencies, or IDE-specific configurations.
  The preset is tailored to

  ensure that the core Solidity files, along with relevant configuration and script
  files, are included while

  avoiding unnecessary clutter from temporary files and build outputs. It includes
  common file extensions used in

  Solidity projects and excludes directories that are not relevant to the source code,
  such as build directories

  and IDE configurations.

  '
exclude:
- .git/
- node_modules/
- build/
- artifacts/
- cache/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .sol
- .js
- .ts
- .json
- .yaml
- .yml
- .md
- .txt
- .env
use_default_excludes: true
```

## splunkapp

[View YAML →](./splunkapp.yml)

This preset is tailored for Python-based Splunk apps, such as modular inputs or apps created
using the Add-on Builder. It focuses on capturing essential Python source files, configuration files,
and scripts while excluding directories that typically contain build artifacts, dependencies, or IDE-specific
configurations. The preset is designed to ensure that the core Python files, along with relevant configuration
and script files, are included while avoiding unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.py`, `.conf`, `.json`, `.spec`, `.manifest`, `.md`, `.yml`, `.yaml`, `.txt`

**Exclude patterns:** `.git/`, `.venv/`, `build/`, `dist/`, `.gptcontext-cache/`, `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.vscode/`, `.idea/`, `bin/lib/`, `bin/generated/`, `bin/ta_*/aob_py3/`, `appserver/`

```yaml
MAX_TOTAL_TOKENS: 12000
description: Python Splunk App (e.g. modular input or Add-on Builder app)
long_description: 'This preset is tailored for Python-based Splunk apps, such as modular
  inputs or apps created

  using the Add-on Builder. It focuses on capturing essential Python source files,
  configuration files,

  and scripts while excluding directories that typically contain build artifacts,
  dependencies, or IDE-specific

  configurations. The preset is designed to ensure that the core Python files, along
  with relevant configuration

  and script files, are included while avoiding unnecessary clutter from temporary
  files and build outputs.

  '
exclude:
- .git/
- .venv/
- build/
- dist/
- .gptcontext-cache/
- __pycache__/
- .pytest_cache/
- .mypy_cache/
- .vscode/
- .idea/
- bin/lib/
- bin/generated/
- bin/ta_*/aob_py3/
- appserver/
include_exts:
- .py
- .conf
- .json
- .spec
- .manifest
- .md
- .yml
- .yaml
- .txt
use_default_excludes: true
```

## terraform

[View YAML →](./terraform.yml)

This preset is designed for Terraform projects, focusing on capturing the essential
source files, configuration files, and scripts while excluding directories that typically contain
build artifacts, dependencies, or IDE-specific configurations. The preset is tailored to ensure that
the core Terraform files, along with relevant configuration and script files, are included while avoiding
unnecessary clutter from temporary files and build outputs. It includes common file extensions used in Terraform
projects and excludes directories that are not relevant to the source code, such as build directories
and IDE configurations.

**Include extensions:** `.tf`, `.tfvars`, `.tfstate`, `.json`, `.yaml`, `.yml`, `.md`, `.sh`, `.txt`

**Exclude patterns:** `.git/`, `.terraform/`, `.gptcontext-cache/`, `.idea/`, `.vscode/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: Terraform / Infrastructure-as-Code (IaC) project
long_description: 'This preset is designed for Terraform projects, focusing on capturing
  the essential

  source files, configuration files, and scripts while excluding directories that
  typically contain

  build artifacts, dependencies, or IDE-specific configurations. The preset is tailored
  to ensure that

  the core Terraform files, along with relevant configuration and script files, are
  included while avoiding

  unnecessary clutter from temporary files and build outputs. It includes common file
  extensions used in Terraform

  projects and excludes directories that are not relevant to the source code, such
  as build directories

  and IDE configurations.

  '
exclude:
- .git/
- .terraform/
- .gptcontext-cache/
- .idea/
- .vscode/
include_exts:
- .tf
- .tfvars
- .tfstate
- .json
- .yaml
- .yml
- .md
- .sh
- .txt
use_default_excludes: true
```

## tests_only

[View YAML →](./tests_only.yml)

This preset is designed for capturing test files and configurations across various programming languages.
It includes common file extensions used in testing and configuration files, while excluding directories
that typically contain source code, build artifacts, or other non-essential files. The preset is tailored
to ensure that the core test files, along with relevant configuration files, are included while avoiding
unnecessary clutter from source code and build outputs. It includes common file extensions used in testing
and excludes directories that are not relevant to the test files, such as source directories and build
directories.

**Include extensions:** `.py`, `.js`, `.ts`, `.java`, `.rb`, `.yaml`, `.yml`, `.json`, `.md`, `.txt`

**Exclude patterns:** `.git/`, `node_modules/`, `dist/`, `build/`, `public/`, `static/`, `src/`, `app/`, `bin/`, `.venv/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 12000
MAX_FILE_TOKENS: 4000
description: "Tests only \u2014 capture test files and configs"
long_description: 'This preset is designed for capturing test files and configurations
  across various programming languages.

  It includes common file extensions used in testing and configuration files, while
  excluding directories

  that typically contain source code, build artifacts, or other non-essential files.
  The preset is tailored

  to ensure that the core test files, along with relevant configuration files, are
  included while avoiding

  unnecessary clutter from source code and build outputs. It includes common file
  extensions used in testing

  and excludes directories that are not relevant to the test files, such as source
  directories and build

  directories.

  '
exclude:
- .git/
- node_modules/
- dist/
- build/
- public/
- static/
- src/
- app/
- bin/
- .venv/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .py
- .js
- .ts
- .java
- .rb
- .yaml
- .yml
- .json
- .md
- .txt
use_default_excludes: true
```

## typescript_node

[View YAML →](./typescript_node.yml)

This preset is designed for Node.js applications using TypeScript. It focuses on capturing the essential
source files, configuration files, and scripts while excluding directories that typically contain
build artifacts, dependencies, or IDE-specific configurations. The preset is tailored to ensure that
the core TypeScript files, along with relevant configuration and script files, are included while avoiding
unnecessary clutter from temporary files and build outputs. It includes common file extensions used in Node.js
projects and excludes directories that are not relevant to the source code, such as build directories
and IDE configurations. This preset is ideal for applications that utilize TypeScript for development, ensuring
that the essential files are captured for analysis or deployment while maintaining a clean project structure.

**Include extensions:** `.ts`, `.tsx`, `.js`, `.jsx`, `.json`, `.yaml`, `.yml`, `.md`, `.html`, `.scss`, `.css`

**Exclude patterns:** `.git/`, `node_modules/`, `dist/`, `build/`, `coverage/`, `.gptcontext-cache/`, `.vscode/`, `.idea/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: Node.js / TypeScript app
long_description: 'This preset is designed for Node.js applications using TypeScript.
  It focuses on capturing the essential

  source files, configuration files, and scripts while excluding directories that
  typically contain

  build artifacts, dependencies, or IDE-specific configurations. The preset is tailored
  to ensure that

  the core TypeScript files, along with relevant configuration and script files, are
  included while avoiding

  unnecessary clutter from temporary files and build outputs. It includes common file
  extensions used in Node.js

  projects and excludes directories that are not relevant to the source code, such
  as build directories

  and IDE configurations. This preset is ideal for applications that utilize TypeScript
  for development, ensuring

  that the essential files are captured for analysis or deployment while maintaining
  a clean project structure.

  '
exclude:
- .git/
- node_modules/
- dist/
- build/
- coverage/
- .gptcontext-cache/
- .vscode/
- .idea/
include_exts:
- .ts
- .tsx
- .js
- .jsx
- .json
- .yaml
- .yml
- .md
- .html
- .scss
- .css
use_default_excludes: true
```

## unity

[View YAML →](./unity.yml)

This preset is tailored for Unity game projects, focusing on C# scripts, Unity YAML files,
and configuration files. It includes common file extensions used in Unity development and excludes directories
that typically contain build artifacts, temporary files, or IDE-specific configurations. The preset is designed to capture the essential
source files while avoiding unnecessary clutter from temporary files and build outputs.

**Include extensions:** `.cs`, `.shader`, `.cginc`, `.yaml`, `.yml`, `.meta`, `.md`, `.txt`

**Exclude patterns:** `.git/`, `Library/`, `Temp/`, `Obj/`, `Build/`, `Builds/`, `Logs/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: Unity game project (C# + Unity YAML + configs)
long_description: 'This preset is tailored for Unity game projects, focusing on C#
  scripts, Unity YAML files,

  and configuration files. It includes common file extensions used in Unity development
  and excludes directories

  that typically contain build artifacts, temporary files, or IDE-specific configurations.
  The preset is designed to capture the essential

  source files while avoiding unnecessary clutter from temporary files and build outputs.

  '
exclude:
- .git/
- Library/
- Temp/
- Obj/
- Build/
- Builds/
- Logs/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .cs
- .shader
- .cginc
- .yaml
- .yml
- .meta
- .md
- .txt
use_default_excludes: true
```

## unreal

[View YAML →](./unreal.yml)

This preset is designed for Unreal Engine projects, focusing on C++ source files, configuration files,
and Unreal-specific files. It includes common file extensions used in Unreal Engine development and excludes directories
that typically contain build artifacts, intermediate files, or IDE-specific configurations. The preset is tailored to ensure that
the core Unreal Engine files, along with relevant configuration and script files, are included while avoiding
unnecessary clutter from temporary files and build outputs. It captures the essential source files
while excluding directories that are not relevant to the source code, such as build directories and IDE configurations.

**Include extensions:** `.cpp`, `.h`, `.hpp`, `.uproject`, `.uplugin`, `.ini`, `.json`, `.yaml`, `.yml`, `.md`, `.txt`

**Exclude patterns:** `.git/`, `Binaries/`, `Intermediate/`, `Saved/`, `DerivedDataCache/`, `.idea/`, `.vscode/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: Unreal Engine project
long_description: 'This preset is designed for Unreal Engine projects, focusing on
  C++ source files, configuration files,

  and Unreal-specific files. It includes common file extensions used in Unreal Engine
  development and excludes directories

  that typically contain build artifacts, intermediate files, or IDE-specific configurations.
  The preset is tailored to ensure that

  the core Unreal Engine files, along with relevant configuration and script files,
  are included while avoiding

  unnecessary clutter from temporary files and build outputs. It captures the essential
  source files

  while excluding directories that are not relevant to the source code, such as build
  directories and IDE configurations.

  '
exclude:
- .git/
- Binaries/
- Intermediate/
- Saved/
- DerivedDataCache/
- .idea/
- .vscode/
- .gptcontext-cache/
include_exts:
- .cpp
- .h
- .hpp
- .uproject
- .uplugin
- .ini
- .json
- .yaml
- .yml
- .md
- .txt
use_default_excludes: true
```

## vue

[View YAML →](./vue.yml)

This preset is designed for Vue.js projects, focusing on capturing the essential source files,
configuration files, and scripts while excluding directories that typically contain build artifacts,
dependencies, or IDE-specific configurations. The preset is tailored to ensure that the core Vue.js files,
along with relevant configuration and script files, are included while avoiding unnecessary clutter
from temporary files and build outputs. It includes common file extensions used in Vue.js projects and
excludes directories that are not relevant to the source code, such as build directories and IDE configurations.

**Include extensions:** `.vue`, `.js`, `.ts`, `.jsx`, `.tsx`, `.json`, `.md`, `.html`, `.css`, `.scss`, `.sass`, `.yml`, `.yaml`

**Exclude patterns:** `.git/`, `node_modules/`, `dist/`, `build/`, `coverage/`, `.cache/`, `.gptcontext-cache/`, `.idea/`, `.vscode/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: Vue.js project
long_description: 'This preset is designed for Vue.js projects, focusing on capturing
  the essential source files,

  configuration files, and scripts while excluding directories that typically contain
  build artifacts,

  dependencies, or IDE-specific configurations. The preset is tailored to ensure that
  the core Vue.js files,

  along with relevant configuration and script files, are included while avoiding
  unnecessary clutter

  from temporary files and build outputs. It includes common file extensions used
  in Vue.js projects and

  excludes directories that are not relevant to the source code, such as build directories
  and IDE configurations.

  '
exclude:
- .git/
- node_modules/
- dist/
- build/
- coverage/
- .cache/
- .gptcontext-cache/
- .idea/
- .vscode/
include_exts:
- .vue
- .js
- .ts
- .jsx
- .tsx
- .json
- .md
- .html
- .css
- .scss
- .sass
- .yml
- .yaml
use_default_excludes: true
```

## webapp

[View YAML →](./webapp.yml)

This preset is tailored for Python web applications, including frameworks like FastAPI, Django, and Flask.
It focuses on capturing the essential source files, templates, static files, and configuration files
while excluding directories that typically contain build artifacts, dependencies, or IDE-specific configurations.
The preset is designed to ensure that the core Python files, along with relevant HTML templates,
JavaScript, CSS, and configuration files, are included while avoiding unnecessary clutter from temporary files
and build outputs. It includes common file extensions used in Python web applications and excludes directories
that are not relevant to the source code, such as virtual environments, build directories, and IDE configurations.

**Include extensions:** `.py`, `.html`, `.jinja`, `.jinja2`, `.md`, `.js`, `.ts`, `.json`, `.toml`, `.yaml`, `.yml`, `.css`, `.scss`, `.env`, `.txt`, `.ini`, `.cfg`

**Exclude patterns:** `.git/`, `.venv/`, `node_modules/`, `dist/`, `build/`, `static/`, `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.vscode/`, `.idea/`, `.gptcontext-cache/`

```yaml
MAX_TOTAL_TOKENS: 15000
MAX_FILE_TOKENS: 4000
description: Python webapp (FastAPI, Django, Flask, etc.)
long_description: 'This preset is tailored for Python web applications, including
  frameworks like FastAPI, Django, and Flask.

  It focuses on capturing the essential source files, templates, static files, and
  configuration files

  while excluding directories that typically contain build artifacts, dependencies,
  or IDE-specific configurations.

  The preset is designed to ensure that the core Python files, along with relevant
  HTML templates,

  JavaScript, CSS, and configuration files, are included while avoiding unnecessary
  clutter from temporary files

  and build outputs. It includes common file extensions used in Python web applications
  and excludes directories

  that are not relevant to the source code, such as virtual environments, build directories,
  and IDE configurations.

  '
exclude:
- .git/
- .venv/
- node_modules/
- dist/
- build/
- static/
- __pycache__/
- .pytest_cache/
- .mypy_cache/
- .vscode/
- .idea/
- .gptcontext-cache/
include_exts:
- .py
- .html
- .jinja
- .jinja2
- .md
- .js
- .ts
- .json
- .toml
- .yaml
- .yml
- .css
- .scss
- .env
- .txt
- .ini
- .cfg
use_default_excludes: true
```

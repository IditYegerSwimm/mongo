---
title: Internal API
---
## Introduction

In this doc we will describe the API for {{API Name (e.g., sending Analytic Events)}} and how to use it correctly.

We use this API when {{use cases}}.

## API definition

## Simple usage

<SwmSnippet path="/evergreen/bazel_compile.sh" line="12">

---

&nbsp;

```shell
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null 2>&1 && pwd)"
. "$DIR/prelude.sh"

cd src

set -o errexit
set -o verbose

# Use `eval` to force evaluation of the environment variables in the echo statement:
eval echo "Execution environment: Compiler: ${compiler} Targets: ${targets}"

source ./evergreen/bazel_RBE_supported.sh

if bazel_rbe_supported; then
  LOCAL_ARG=""
else
  LOCAL_ARG="--config=local"
fi

```

---

</SwmSnippet>

## Advanced usage: {{explain a scenario where this is needed}}

<SwmSnippetPlaceholder>

Show an advanced example of using this API

</SwmSnippetPlaceholder>

## Best practices and additional notes

When using this API, it is important to follow a few best practices and avoid some common mistakes.

<SwmSnippet path="/evergreen/bazel_scons_diff.sh" line="26">

---

&nbsp;

```shell
extra_args="$extra_args ${compile_flags}"
extra_args="$extra_args --evergreen-tmp-dir=${TMPDIR}"
extra_args="$extra_args\""

```

---

</SwmSnippet>

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBbW9uZ28lM0ElM0FJZGl0WWVnZXJTd2ltbQ==" repo-name="mongo"><sup>Powered by [Swimm](https://staging.swimm.cloud/)</sup></SwmMeta>

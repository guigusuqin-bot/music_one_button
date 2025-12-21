name: Build Android APK (Kivy)

on:
  push:
    branches: ["main"]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install system deps
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            zip unzip \
            build-essential \
            git \
            openjdk-17-jdk \
            libffi-dev libssl-dev \
            libsqlite3-dev zlib1g-dev

      - name: Install Buildozer
        run: |
          python -m pip install --upgrade pip wheel setuptools
          pip install --no-cache-dir buildozer==1.5.0 Cython==0.29.36

      - name: Build APK (debug)
        run: |
          buildozer -v android debug

      - name: Collect APK
        run: |
          set -e
          mkdir -p output
          echo "=== bin/ ==="
          ls -la bin || true
          echo "=== find apk ==="
          find . -maxdepth 6 -type f -name "*.apk" -print
          cp -v bin/*.apk output/ || true
          # 兜底：如果 apk 不在 bin/，就从 find 结果里拷贝
          if [ ! "$(ls -A output 2>/dev/null)" ]; then
            find . -maxdepth 6 -type f -name "*.apk" -exec cp -v {} output/ \;
          fi
          echo "=== output/ ==="
          ls -la output

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: apk
          path: output/*.apk
          if-no-files-found: error

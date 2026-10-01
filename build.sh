#!/usr/bin/env sh
# Builds the whole site into site/: the landing page at the root, the docs under /docs/.
# Cloudflare Pages runs this (build command: sh build.sh, output directory: site).
set -e
mkdocs build --strict
cp -R landing/. site/

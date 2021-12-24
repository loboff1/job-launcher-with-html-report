#!/usr/bin/env bash
set -e

echo -e "\n---Update pip---"
pip install -U pip
echo -e "\n---Update setuptools, wheel packages---"
pip install -U setuptools wheel
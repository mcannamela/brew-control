#!/bin/bash

echo "Put this in your profile:"
echo "export ATLAS=None"
echo "export BLAS=/usr/local/opt/openblas/lib/libopenblas.dylib"
echo "export LAPACK=/usr/local/opt/openblas/lib/libopenblas.dylib"

brew tap 'homebrew/bundle'
brew bundle
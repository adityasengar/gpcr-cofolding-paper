#!/bin/bash
# Papers on disk with no extraction. Empty-dir safe.
cd "$(dirname "$0")"
comm -23 <(find pdfs -name '*.pdf' -exec basename {} .pdf \; | sort) \
         <(find notes -name '*.md' -exec basename {} .md \; 2>/dev/null | sort)

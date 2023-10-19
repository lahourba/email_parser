# Email Parser and Keyword Extractor

A Python script to parse and extract context from .msg email files.

## Overview

This script processes .msg email files to:

- Extract details such as sender, date sent, recipient, subject, and content.
- Determine top keywords from the content to provide context about the email's theme or subject.
- Put this info in a pandas dataframe.
- Extracts a .csv from the dataframe.

## Dependencies 

- os
- pandas
- extract_msg
- re
- spacy
- collections

Make sure to install the required Python packages using pip


## Usage

1. Update the `directory_path` variable in the script to point to your directory containing `.msg` files:

```python
directory_path = 'path_to_directory_with_msg_files'
```

2. Run the script

```python
python your_script_name.py

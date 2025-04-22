# EASE 2025 Data Paper Project

This repository contains code for your EASE 2025 paper and data for analyzing bug reports and developer reputation in open-source projects. Below is a detailed description of each file and its purpose:

## Data Files

### `bugs-2025-02-23.csv`
- **Purpose**: Main dataset containing raw bug reports
- **Data Content**: Contains bug report information including bug IDs, descriptions, status, and other metadata
- **Format**: CSV file with multiple columns of bug report attributes

## Core Analysis Scripts

### `CTQRS_Scoring_Code.py`
- **Purpose**: Implements the CTQRS (Completeness, Traceability, Quality, Reproducibility, and Specificity) scoring system for bug reports
- **Key Features**:
  - Analyzes bug report text quality using NLP techniques
  - Implements various scoring rules (RM1-RM4, RR1-RR5, RA1-RA4)
  - Uses Stanza for text processing
  - Evaluates readability, punctuation, sentence structure, and content quality
  - Processes Excel files to generate bug report scores
- **Source**:  author={Zhang, Huan and Zhao, Yuan and Yu, Shengcheng and Chen, Zhenyu},
  booktitle={2022 9th International Conference on Dependable Systems and Their Applications (DSA)}, 
  title={Automated Quality Assessment for Crowdsourced Test Reports Based on Dependency Parsing}, 
  year={2022},
  volume={},
  number={},
  pages={34-41},
  keywords={Industries;Computer bugs;Inspection;Predictive models;Quality assessment;Mobile applications;Testing;Crowdsourced testing;Desirable properties;Quality indicators;dependency parsing;Test report quality},
  doi={10.1109/DSA56465.2022.00014}

### `reputation.py` and `local_reputation_.py`
- **Purpose**: Analyzes developer reputation and contribution history
- **Key Features**:
  - Fetches user details from bug tracking systems
  - Implements rate limiting for API calls
  - Connects to MongoDB for data storage
  - Analyzes developer activity and contribution patterns

### `Get_meta_data.py` and `2_get_meta.py`
- **Purpose**: Retrieves metadata about bug reports from bugzilla
- **Key Features**:
  - Fetches bug details from Bugzilla
  - Implements rate-limited API calls
  - Extracts bug comments and author information
  - Stores data in MongoDB

### `Only_meta_data.py`
- **Purpose**: Focused version of metadata extraction
- **Key Features**:
  - Extracts specific metadata fields from bug reports
  - Optimized for targeted data collection

## Supporting Scripts

### `Authors.py`
- **Purpose**: Analyzes author information and contribution patterns
- **Key Features**:
  - Processes author-related data
  - Analyzes developer participation in bug reports

### `Bug_comment.py`
- **Purpose**:  Fetches and Analyzes bug report comments
- **Key Features**:
  - Processes and analyzes comment content
  - Extracts meaningful information from discussion threads

### `proxies.py` and `proxy.py`
- **Purpose**: Manages proxy connections for web scraping
- **Key Features**:
  - Implements proxy rotation
  - Handles proxy authentication and management
  - Used for rate-limited API calls

### `proxies_list.txt`
- **Purpose**: Contains list of proxy servers
- **Format**: Text file with proxy server addresses and credentials

### `vis.py`
- **Purpose**: Data visualization scripts
- **Key Features**:
  - Creates visualizations of analysis results
  - Generates plots and charts for data presentation

## Dependencies
- Python 3.x
- Required Python packages:
  - pandas
  - requests
  - BeautifulSoup
  - pymongo
  - stanza
  - textstat
  - numpy

## Usage
1. Ensure all dependencies are installed
2. Configure MongoDB connection settings if needed
3. Run the desired analysis scripts based on your needs
4. Check the output files for results

## Data Flow
1. Raw bug reports are collected from `bugs-2025-02-23.csv`
2. Metadata is extracted using `Get_meta_data.py`
3. Bug reports are scored using `CTQRS_Scoring_Code.py`
4. Developer reputation is analyzed using `reputation.py`
5. Results are stored in MongoDB and can be visualized using `vis.py`

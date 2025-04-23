# EASE 2025 Data Paper Project

This repository contains code for your EASE 2025 paper and data for analyzing bug reports and developer reputation in open-source projects. Below is a detailed description of each file and its purpose:

## Key Mozilla Projects Summary

Here is a summary of some core and prominent Mozilla projects:

| Project           | What it does                                                     |
| :---------------- | :--------------------------------------------------------------- |
| Core              | Show websites and run JavaScript in Firefox using the Gecko engine and SpiderMonkey |
| Firefox           | A web browser focused on speed, privacy, and user control        |
| Thunderbird       | Free email app with calendar and contact tools                   |
| Mozilla Testing   | Runs checks on Mozilla software to find bugs early               |
| Mozilla Toolkit   | Tools for building apps that run on any system                   |
| Fenix (Firefox Android) | New Firefox for Android using GeckoView engine             |
| DevTools          | Tools inside Firefox for editing and debugging websites          |
| Firefox Build System | System to turn Firefox source code into apps                   |
| Web Extensions    | One system to build browser add-ons for multiple browsers        |

## Active Mozilla Projects

This section lists various active projects and areas within Mozilla.

### Main Applications & User-Facing Products

* **Firefox:** Mozilla's flagship web browser.
* **Thunderbird:** Email, calendar, and contact management application.
* **Focus:** Privacy-centric mobile browser.
* **Firefox for iOS:** Firefox browser tailored for iOS devices.
* **SeaMonkey:** Integrated internet suite with browser, email, and more.
* **Pocket:** Service for saving content to read later.
* **Mozilla VPN:** Virtual private network service.
* **Firefox Private Network:** Experimental secure Browse service.
* **Other Applications:** Miscellaneous software projects.

### Core & Platform Technologies

* **Core:** Foundational principles and community driving Mozilla's mission. (Also refers to the Gecko rendering engine and SpiderMonkey JavaScript engine).
* **Toolkit:** Shared code and tools for Mozilla applications.
* **NSPR:** Low-level platform abstraction library.
* **GeckoView:** Embeddable browser engine for Android apps.
* **MailNews Core:** Core components for email and news functionalities.
* **Chat Core:** Core components for chat functionalities.
* **Remote Protocol:** APIs for remote browser control and automation.
* **Conduit:** Project details not specified.
* **Eliot:** Project details not specified.
* **Tecken:** Project details not specified.
* **Snippets:** Project details not specified.

### Development & Infrastructure

* **WebExtensions:** Framework for building browser add-ons.
* **DevTools:** Built-in tools for web development in Firefox.
* **Firefox Build System:** Infrastructure for compiling Firefox.
* **Taskcluster:** Automation framework for building and testing code.
* **Developer Infrastructure:** Tools and systems supporting developer workflows.
* **Infrastructure & Operations:** Manages Mozilla's IT infrastructure.
* **Webtools:** Web-based tools for development and support.
* **Localization Infrastructure and Tools:** Tools for software translation.
* **Participation Infrastructure:** Systems enabling community contributions.

### Data, Quality, & Security

* **bugzilla.mozilla.org:** Platform for tracking and resolving software bugs.
* **Data Platform and Tools:** Systems for data collection and analysis.
* **Data & BI Services Team:** Provides data analytics and business intelligence.
* **Mozilla Metrics:** Data collection and analysis for product insights.
* **quality.mozilla.org:** Platform related to software quality assurance.
* **Security Assurance:** Ensures product security and integrity.
* **Mozilla QA:** Quality assurance processes and testing.
* **Data Compliance:** Ensures adherence to data privacy regulations.
* **Firefox Profiler:** Performance analysis tool for Firefox.
* **Testing:** Processes ensuring software quality and reliability.
* **Testopia:** Test case management system.
* **Socorro:** Crash reporting and analysis system.
* **NSS:** Security libraries for cryptographic operations.
* **Tracking:** Efforts to protect users from online tracking.
* **Shield:** Platform for running product experiments and studies.
* **Web Compatibility:** Ensures websites function correctly in Firefox.

### Foundation, Outreach, & Services

* **CA Program:** Manages digital certificates for secure web connections.
* **www.mozilla.org:** Mozilla's official website.
* **support.mozilla.org:** User support and help resources.
* **developer.mozilla.org:** Resource hub for web developers.
* **Mozilla Foundation Communications:** Public communications from the Mozilla Foundation.
* **Mozilla Foundation:** Non-profit organization behind Mozilla's initiatives.
* **Marketing:** Promotion of Mozilla's products and mission.
* **User Research:** Studies on user interactions with Mozilla products.
* **Developer Engagement:** Initiatives to support and connect with developers.
* **Websites:** Management of Mozilla's web properties.
* **Mozilla Localizations:** Translation of Mozilla products into various languages.
* **Internet Public Policy:** Advocacy on internet policy issues.
* **Application Services:** Backend services supporting applications.
* **Developer Ecosystem:** Support for the broader developer community.
* **Location:** Services related to geolocation functionalities.
* **Growth:** Initiatives to expand Mozilla's user base.
* **Air Mozilla:** Platform for internal communications and events.
* **Release Engineering:** Processes for software release management.

## Archived Mozilla Projects (Graveyard)

These projects represent older or retired components and initiatives.

* **Toolkit Graveyard:** Archive of older parts of the Mozilla Toolkit.
* **Webtools Graveyard:** Archive of older web-based tools from Mozilla.
* **Cloud Services Graveyard:** Archive of older cloud services from Mozilla.
* **GeckoView Graveyard:** Archive of older versions or related projects of GeckoView.
* **Core Graveyard:** Archive of older parts of the Mozilla Core project.
* **Lockwise Graveyard:** Archive of Mozilla's password manager.
* **Release Engineering Graveyard:** Archive of older release processes.
* **Testing Graveyard:** Archive of older testing methods or projects.
* **Firefox for FireTV Graveyard:** Archive of the Firefox version for Amazon Fire TV.
* **User Experience Design Graveyard:** Archive of older user experience design projects.
* **Data Platform and Tools Graveyard:** Archive of older data platform and tool projects.
* 
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

# AutoDoc Generator

An automated documentation generator that captures screenshots of web applications and creates comprehensive user guides using AI-powered analysis.

## Overview

AutoDoc Generator is a Python-based tool that automates the process of creating user documentation for web applications. It captures screenshots of specified web pages, analyzes them using OpenAI's Vision API, and generates both individual markdown chapters and a complete PDF user guide.

## Features

- **Automated Screenshot Capture**: Uses `shot-scraper` to capture screenshots of web application pages
- **AI-Powered Analysis**: Leverages OpenAI's GPT-4 Vision API to analyze screenshots and generate descriptions
- **Multi-Format Output**: Generates individual markdown files and combines them into a single PDF guide
- **Authentication Support**: Handles login-protected applications with authentication files
- **Configurable Workflow**: YAML-based configuration for easy customization

## Prerequisites

- Python 3.7+
- OpenAI API key
- Web application running and accessible
- Browser (automatically installed by shot-scraper)

## Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install browser for screenshot capture:
   ```bash
   shot-scraper install
   ```

5. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   Or create a `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Configuration

### 1. Login Configuration (`login.yml`)

Configure the login URL for your web application:

```yaml
- output: screenshots/login.png
  url: http://localhost:3000/login
```

### 2. Screenshots Configuration (`shots.yml`)

Define which pages to capture and document:

```yaml
- output: screenshots/dashboard.png
  url: http://localhost:3000/admin/dashboard
- output: screenshots/users.png
  url: http://localhost:3000/admin/users
- output: screenshots/settings.png
  url: http://localhost:3000/settings
```

## Usage

### Quick Start

Run the complete workflow:

```bash
./autodoc.sh
```

This script will:
1. Set up the virtual environment
2. Install dependencies if needed
3. Run the complete documentation generation process

Or activate your environment and run this directly

```bash
python3 autodoc.py
```

### Manual Execution

1. **Capture Screenshots**:
   ```bash
   python3 capture_screenshots.py
   ```

2. **Analyze and Generate Documentation**:
   ```bash
   python3 analyze_and_document.py
   ```

### Individual Components

#### Screenshot Capture (`capture_screenshots.py`)

- Reads configuration from `login.yml` and `shots.yml`
- Handles authentication for protected pages
- Captures screenshots and saves them to the `screenshots/` directory

#### Analysis and Documentation (`analyze_and_document.py`)

- Analyzes each screenshot using OpenAI's Vision API
- Generates descriptive content for each page
- Creates individual markdown files in the `chapters/` directory
- Combines all chapters into a single PDF user guide

#### Markdown to HTML/PDF Converter (`markdown_to_html.py`)

- Converts markdown files to HTML
- Generates PDF output using WeasyPrint
- Supports both individual file conversion and combined document generation

## Output Structure

After running the tool, you'll find:

```
├── screenshots/          # Captured screenshots
│   ├── dashboard.png
│   ├── users.png
│   └── ...
├── chapters/            # Individual markdown chapters
│   ├── Dashboard.md
│   ├── Users.md
│   └── ...
├── user_guide.html      # Combined HTML documentation
└── user_guide.pdf       # Final PDF user guide
```

## Configuration Options

### Authentication

For applications requiring login:

1. The tool will prompt for authentication when first accessing protected pages
2. Authentication is saved in `auth.json` for subsequent runs
3. Update `login.yml` with your application's login URL

### Customization

- **Screenshot Quality**: Modify wait times in `capture_screenshots.py` for better page loading
- **AI Analysis**: Customize the analysis prompt in `analyze_and_document.py`
- **Output Format**: Adjust styling and layout in `markdown_to_html.py`

## Troubleshooting

### Common Issues

1. **Authentication Failures**:
   - Ensure your web application is running
   - Check that the login URL in `login.yml` is correct
   - Delete `auth.json` and re-authenticate if needed

2. **Screenshot Capture Issues**:
   - Verify URLs in `shots.yml` are accessible
   - Check that the browser is properly installed: `shot-scraper install`
   - Increase wait times for slow-loading pages

3. **AI Analysis Errors**:
   - Verify your OpenAI API key is set correctly
   - Check your OpenAI account has sufficient credits
   - Ensure screenshots are valid image files

4. **PDF Generation Issues**:
   - Install WeasyPrint dependencies: `pip install weasyprint`
   - On Linux, you may need additional system packages:
     ```bash
     sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
     ```

## Dependencies

- `openai`: OpenAI API client for AI analysis
- `shot-scraper`: Web screenshot capture tool
- `python-dotenv`: Environment variable management
- `markdown`: Markdown processing
- `weasyprint`: PDF generation
- `pyyaml`: YAML configuration parsing

## License

This project is open source. Please check the license file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the configuration files
3. Ensure all dependencies are properly installed
4. Verify your OpenAI API key and credits
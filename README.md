# AI Organization Management System

A sophisticated organization management system powered by AI agents. This system provides a framework for managing departments, agents, and quality assurance processes with a focus on scalability and efficiency.

## System Components

1. **Base Classes** (in `organization/utils/`)
   - `BaseAgent`: Abstract base class for all agents
   - `BaseManager`: Abstract base class for all managers
   - `BaseQAAgent`: Abstract base class for all QA agents

2. **Departments**
   - **Marketing Department**
     - `MarketingAgent`: Handles content creation, campaigns, market research, and social media tasks
     - `MarketingManager`: Manages marketing strategy, budget allocation, and team coordination
     - `MarketingQAAgent`: Reviews marketing content and campaigns with specific checklists
   - **Production Department** (structure ready for implementation)
   - **Content Department** (structure ready for implementation)

## Features

- **Agent Management**
  - Task assignment and tracking
  - Performance metrics and reporting
  - Skill development and knowledge base
  - Asynchronous task processing

- **Manager Capabilities**
  - Department strategy development
  - Budget allocation
  - Team coordination
  - Performance monitoring

- **Quality Assurance**
  - Task review and validation
  - Quality scoring
  - Issue tracking and suggestions
  - Department-specific checklists

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the test suite to verify the system:
```bash
python test_organization.py
```

## Project Structure

```
├── organization/
│   ├── utils/
│   │   ├── base_agent.py
│   │   ├── base_manager.py
│   │   └── base_qa_agent.py
│   ├── departments/
│   │   ├── marketing/
│   │   │   ├── agents/
│   │   │   │   └── marketing_agent.py
│   │   │   ├── managers/
│   │   │   │   └── marketing_manager.py
│   │   │   └── qa/
│   │   │       └── marketing_qa_agent.py
│   │   ├── production/
│   │   └── content/
│   └── vp/
├── test_organization.py
├── requirements.txt
└── README.md
```

## Testing

The system includes a comprehensive test suite (`test_organization.py`) that verifies:
- Base class functionality
- Marketing department components
- Agent task processing
- Manager operations
- QA review processes

Run the tests with:
```bash
python test_organization.py
```

## Dependencies

- python-dotenv==1.0.0
- pydantic==2.5.2
- fastapi==0.104.1
- uvicorn==0.24.0
- python-multipart==0.0.6
- requests==2.31.0

## Contributing

To add new departments or components:
1. Create new agent/manager/QA classes inheriting from base classes
2. Implement required abstract methods
3. Add department-specific functionality
4. Update tests to cover new components

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
# Claude Instructions for TouchDesigner Project

## Pre-Response Requirements

**CRITICAL: Before answering ANY TouchDesigner-related question, you MUST:**

1. **Read this entire CLAUDE.md file** to understand the project context and requirements
2. **Reference the TouchDesigner documentation** for accurate parameter names and API usage:
   - Main UserGuide: https://derivative.ca/UserGuide
   - Python API Documentation: https://derivative.ca/UserGuide/Category%3APython
3. **Reference the AxiDraw documentation** when questions involve pen plotting:
   - AxiDraw Python API: https://axidraw.com/doc/py_api/#
   - Hardware: AxiDraw V3 with brushless servo configuration
4. **Consult the following project-specific files** for context about the HydraToTD system:
   - `Architechure.md` - System architecture and module specifications
   - `Hydra-TouchDesigner Implementation Blueprint.md` - Step-by-step build instructions and implementation details
   - `Hydra-TouchDesigner Technical Stack.md` - Technical specifications, dependencies, and performance requirements
   - `ProjectDescription.md` - Core features, workflow, and build priorities

## Documentation Reference Guidelines

### Always Verify Parameter Names
- **DO NOT guess** TouchDesigner parameter names or methods
- **ALWAYS check** the official documentation for exact parameter syntax
- **Common TouchDesigner objects** to reference:
  - `op()` - Operator references
  - `me` - Current operator context
  - `parent()` - Parent component access
  - `args[]` - Callback arguments
  - Parameter syntax: `op.par.parametername`

### Key TouchDesigner Python Classes to Reference:
- `OP` class - Base operator class
- `COMP` class - Component operators
- `TOP` class - Texture operators  
- `CHOP` class - Channel operators
- `SOP` class - Surface operators
- `DAT` class - Data operators
- `MAT` class - Material operators

### Parameter Access Patterns:
```python
# Correct parameter access patterns to verify in docs:
op.par.parameter_name.val          # Get parameter value
op.par.parameter_name = value       # Set parameter value
op.par.parameter_name.expr = "expr" # Set expression
```

## Project Context

This is a **HydraToTD** project that bridges Hydra visual synthesis with TouchDesigner. Key components:

### Project Structure:
- Main TD file: `hydraToTD.41.toe`
- Python scripts in `/scripts/`
- HTML/JS integration in `/html/`
- Preset system in `/presets/`
- Component library in `/components/`

### Key Systems (Reference Architecture.md for details):
1. **Hydra-to-TouchDesigner translation**
2. **Preset management system**
3. **Multi-output rendering**
4. **Real-time parameter mapping**

### Project Documentation Files:
- **Architecture.md:** System modules, phase buildout, technical implementation notes
- **Implementation Blueprint.md:** Step-by-step build guide, code examples, testing procedures
- **Technical Stack.md:** Performance specs, dependencies, optimization strategies, file structure
- **ProjectDescription.md:** Core features overview, workflow, build priorities

## Response Protocol

### Before Every Response:
1. ✅ Read this CLAUDE.md file completely
2. ✅ Check TouchDesigner docs for parameter accuracy
3. ✅ Verify syntax against official API documentation
4. ✅ Check AxiDraw Python API docs if pen plotting is involved
5. ✅ Review relevant project documentation files:
   - Architecture.md for system design context
   - Implementation Blueprint.md for build procedures
   - Technical Stack.md for performance/dependency info
   - ProjectDescription.md for feature requirements

### When Writing TouchDesigner Code:
- Use exact parameter names from documentation
- Include proper error handling
- Follow TouchDesigner Python conventions
- Reference appropriate operator classes
- Validate callback signatures against docs

## Collaborative Workflow

### Code Execution Process:
1. **Claude writes** TouchDesigner Python code
2. **User executes** the code within TouchDesigner environment
3. **User provides feedback** with any errors or issues encountered
4. **Claude iterates** based on actual TouchDesigner error messages

### Error Feedback Handling:
When user reports errors from TouchDesigner execution:

#### Expected Error Types:
- **Parameter name errors**: `AttributeError: 'Par' object has no attribute 'paramname'`
- **Operator reference errors**: `AttributeError: op 'operatorname' not found`
- **Syntax errors**: Python syntax issues in TouchDesigner context
- **Runtime errors**: Execution errors during callback or script execution
- **Type errors**: Incorrect parameter types or value ranges

#### Response to Error Feedback:
1. **Analyze the exact error message** provided by user
2. **Re-check TouchDesigner documentation** for correct parameter names
3. **Identify the root cause** (parameter name, operator reference, syntax, etc.)
4. **Provide corrected code** with explanation of the fix
5. **Include debugging suggestions** if applicable

### Best Practices for Code Delivery:
- Provide **complete, runnable code blocks**
- Include **comments explaining TouchDesigner-specific syntax**
- Add **error checking** where appropriate
- Suggest **testing steps** for the user to validate
- Be prepared for **multiple iterations** based on execution feedback

### Documentation Lookup Process:
1. Identify the TouchDesigner operator type (TOP, CHOP, SOP, etc.)
2. Look up the specific operator in the UserGuide
3. Verify parameter names and types
4. Check Python API documentation for method signatures
5. Confirm callback patterns and arguments

## Common TouchDesigner Pitfalls to Avoid:
- Guessing parameter names instead of looking them up
- Using incorrect callback signatures
- Mixing up operator reference syntax
- Assuming parameter types without verification
- Not handling TouchDesigner's frame-based execution model

## Project-Specific Notes:
- This project uses extensive Python callbacks
- Real-time parameter updates are critical
- Multiple output systems require careful operator management
- Preset system needs robust parameter serialization
- **AxiDraw Integration:** Using AxiDraw V3 with brushless servo for SVG plotting
  - Reference pyaxidraw API for pen control parameters
  - Consider brushless servo timing and acceleration settings
  - SVG optimization required for plotting performance

---

**Remember: Accuracy over speed. Always verify TouchDesigner syntax and parameter names in the official documentation before providing code examples or solutions.**
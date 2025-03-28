"""
Command parser for the CLI
Parses user input into commands and arguments
"""
import re
import logging
import shlex

logger = logging.getLogger(__name__)

def parse_command(command_string):
    """
    Parse a command string into entity, action, and arguments
    
    Example command formats:
    - patient add "John" "Doe" "01/15/1985" "john@example.com" "555-123-4567"
    - patient search "Doe"
    - appointment list --doctor="Smith" --date="2023-12-01"
    """
    try:
        # Use shlex to handle quoted arguments properly
        parts = shlex.split(command_string)
        
        if not parts:
            return None, None, []
        
        # Extract entity and action
        entity = parts[0].lower()
        action = parts[1].lower() if len(parts) > 1 else "list"
        
        # Extract arguments and options
        args = []
        options = {}
        
        for part in parts[2:]:
            # Check if it's an option (starts with --)
            if part.startswith("--"):
                # Extract option name and value
                option_match = re.match(r'--([^=]+)=?(.*)', part)
                if option_match:
                    option_name = option_match.group(1)
                    option_value = option_match.group(2) or True  # If no value, set to True
                    options[option_name] = option_value
            else:
                args.append(part)
        
        # Combine args and options
        args_with_options = {"args": args, "options": options}
        
        logger.debug(f"Parsed command: entity={entity}, action={action}, args={args_with_options}")
        
        return entity, action, args_with_options
    
    except Exception as e:
        logger.error(f"Error parsing command: {e}")
        return None, None, []


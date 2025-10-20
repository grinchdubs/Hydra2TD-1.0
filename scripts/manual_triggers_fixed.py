# Enhanced Manual Triggers - FIXED VERSION (FAST)
# Based on the working lightweight script with TD-compliant naming
# No external dependencies - simple and fast

import re

# ===== SOURCE TRACING HELPER FUNCTIONS =====

def trace_to_source_dat(dat_op):
    """
    Trace from a DAT back to the original source textDAT by following inputs and dat parameters.
    Follows the chain: scene_code textDAT -> selectDAT -> SceneCodeSender -> original SceneCode

    Args:
        dat_op: The DAT operator to trace from

    Returns:
        The original source textDAT with 'SceneCode' tag, or the input dat_op if no source found
    """

    # Check if this DAT itself has the SceneCode tag (we found the source!)
    if 'SceneCode' in dat_op.tags:
        return dat_op

    # If this DAT has inputs, follow them
    if dat_op.inputs and len(dat_op.inputs) > 0:
        # For selectDAT, get the currently selected input
        if dat_op.OPType == 'selectDAT':
            # Try to get the select index
            select_index = 0
            if hasattr(dat_op.par, 'select'):
                select_index = int(dat_op.par.select.eval())
            elif hasattr(dat_op.par, 'index'):
                select_index = int(dat_op.par.index.eval())

            if len(dat_op.inputs) > select_index:
                input_dat = dat_op.inputs[select_index]
                if input_dat:
                    # Recursively trace from the selected input
                    return trace_to_source_dat(input_dat)
        else:
            # For other DATs, just follow the first input
            input_dat = dat_op.inputs[0]
            if input_dat:
                # Recursively trace from the input
                return trace_to_source_dat(input_dat)

    # For selectDAT, also check the 'dat' parameter (parameter-based reference)
    if dat_op.OPType == 'selectDAT':
        try:
            # SelectDAT has a 'dat' parameter that references the source DAT
            if hasattr(dat_op.par, 'dat'):
                dat_path = dat_op.par.dat.eval()
                if dat_path:
                    referenced_dat = op(dat_path)
                    if referenced_dat:
                        # Recursively trace from the referenced DAT
                        return trace_to_source_dat(referenced_dat)
        except Exception as e:
            pass

    # No inputs or couldn't find source - return current DAT as fallback
    return dat_op

def get_current_scene_code():
    """Get the currently running scene code DAT"""
    # Check the scene_registry tableDAT for the active scene
    scene_registry = op('/project1/hydra_system/code/CodeManager/scene_registry')
    if scene_registry:
        try:
            # Look through the table to find the active scene
            for row in range(scene_registry.numRows):
                if row == 0:  # Skip header row
                    continue

                # Find the column indices for 'active' and 'dat_name'
                active_col = None
                dat_name_col = None

                for col in range(scene_registry.numCols):
                    header = str(scene_registry[0, col].val).lower()
                    if header in ['active', 'is_active', 'current']:
                        active_col = col
                    elif header in ['dat_name', 'datname', 'dat', 'code_dat']:
                        dat_name_col = col

                # If we found the active column, check if this scene is active
                if active_col is not None:
                    active_val = scene_registry[row, active_col].val
                    # Check for various ways "active" might be represented
                    is_active = (active_val == 1 or
                               active_val == True or
                               str(active_val).lower() in ['true', '1', 'yes', 'active'])

                    if is_active:
                        # Get the DAT name directly from dat_name column
                        if dat_name_col is not None:
                            dat_name = str(scene_registry[row, dat_name_col].val)
                        else:
                            # Fallback: try to find scene name and construct
                            scene_name_val = scene_registry[row, 0].val if active_col != 0 else scene_registry[row, 1].val
                            if isinstance(scene_name_val, (int, float)):
                                dat_name = f"scene{int(scene_name_val)}_code"
                            else:
                                # Extract number from scene name like "Scene 2"
                                scene_str = str(scene_name_val)
                                numbers = re.findall(r'\d+', scene_str)
                                if numbers:
                                    dat_name = f"scene{numbers[0]}_code"
                                else:
                                    dat_name = "scene1_code"  # fallback

                        # Try to get the actual scene code DAT
                        scene_code = op(f'/project1/hydra_system/code/CodeManager/{dat_name}')
                        if scene_code:
                            print(f"Found active scene from registry: {dat_name}")
                            return scene_code
                        else:
                            print(f"Scene registry indicates {dat_name} is active, but DAT not found")

            print("No active scene found in scene_registry")
        except Exception as e:
            print(f"Error reading scene_registry: {e}")
    else:
        print("scene_registry not found")

    # Fallback: Find the first non-empty scene
    code_manager = op('/project1/hydra_system/code/CodeManager')
    if code_manager:
        scene_codes = []
        for child in code_manager.children:
            if child.name.endswith('_code') and child.name.startswith('scene'):
                scene_codes.append(child)

        if scene_codes:
            # Use the first scene with content as fallback
            active_scenes = [sc for sc in scene_codes if sc.text.strip()]
            if active_scenes:
                current_scene = active_scenes[0]
                print(f"Fallback to first non-empty scene: {current_scene.name}")
                return current_scene

    # Final fallback to scene1_code
    fallback_scene = op('/project1/hydra_system/code/CodeManager/scene1_code')
    if fallback_scene:
        print("Final fallback to scene1_code")
        return fallback_scene

    print("ERROR: No scene code found")
    return None


def preprocess_code_structure(code_text):
    """Pre-calculate function positions and chain positions for fast lookup"""
    # Find all function calls in the code
    func_pattern = r'(\w+)\s*\('
    all_functions = list(re.finditer(func_pattern, code_text))

    # Build a map of position -> (function_name, chain_position)
    func_info_map = {}

    # Split code into lines once
    lines = code_text.split('\n')
    line_starts = [0]
    for line in lines[:-1]:
        line_starts.append(line_starts[-1] + len(line) + 1)  # +1 for newline

    # For each function, calculate its chain position
    for func_match in all_functions:
        func_name = func_match.group(1).lower()
        func_pos = func_match.start()

        # Find which line this function is on
        func_line_idx = 0
        for i, start in enumerate(line_starts):
            if func_pos >= start:
                func_line_idx = i
            else:
                break

        # Walk backwards from this line to find chain start
        chain_position = 0
        for idx in range(func_line_idx, -1, -1):
            stripped = lines[idx].strip()
            if not stripped:
                continue
            if stripped.startswith('.'):
                # This is a chained function
                if idx < func_line_idx:
                    chain_position += 1
            else:
                # Found the start of the chain
                break

        # If current line starts with '.', it's part of a chain
        if lines[func_line_idx].strip().startswith('.'):
            # Count how many dots we've seen up to this point
            for idx in range(func_line_idx, -1, -1):
                stripped = lines[idx].strip()
                if not stripped:
                    continue
                if stripped.startswith('.'):
                    if idx == func_line_idx:
                        # Include this one
                        chain_position += 1
                        break
                    else:
                        chain_position += 1
                else:
                    break

        func_info_map[func_pos] = {
            'name': func_name,
            'chain_position': chain_position,
            'match': func_match
        }

    return func_info_map


def analyze_parameter_context(code_text, valid_matches):
    """Analyze Hydra code context to generate TD-compliant parameter names"""
    param_info = []

    # Common Hydra functions and their parameter patterns
    hydra_functions = {
        'osc': ['frequency', 'sync', 'offset'],
        'noise': ['scale', 'offset'],
        'voronoi': ['scale', 'speed', 'blending'],
        'shape': ['sides', 'radius', 'smoothing'],
        'gradient': ['speed'],
        'src': ['src'],
        'rotate': ['angle', 'speed'],
        'scale': ['amount', 'xmult', 'ymult'],
        'pixelate': ['pixelx', 'pixely'],
        'repeat': ['repeatx', 'repeaty', 'offsetx', 'offsety'],
        'modulaterepeat': ['repeatx', 'repeaty', 'offsetx', 'offsety'],
        'kaleid': ['nsides'],
        'hue': ['hue'],
        'saturate': ['amount'],
        'contrast': ['amount'],
        'brightness': ['amount'],
        'invert': ['amount'],
        'thresh': ['threshold', 'tolerance'],
        'color': ['r', 'g', 'b', 'a'],
        'solid': ['r', 'g', 'b', 'a'],
        'colorama': ['amount'],
        'blend': ['amount'],
        'add': ['amount'],
        'sub': ['amount'],
        'mult': ['amount'],
        'diff': ['amount'],
        'modulate': ['amount'],
        'modulatescale': ['multiple', 'offset'],
        'modulaterotate': ['multiple', 'offset'],
        'modulatehue': ['amount'],
        'modulatekaleid': ['nsides'],
        'modulatescrollx': ['scrollx', 'speed'],
        'modulatescrolly': ['scrolly', 'speed']
    }

    # Functions that use RGB color parameters
    color_functions = {'color', 'solid'}

    chain_names = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

    # Preprocess code structure once for all parameters
    func_info_map = preprocess_code_structure(code_text)

    # Sort function positions once for binary search
    func_positions = sorted(func_info_map.keys())

    # Track parameter name usage to avoid duplicates
    param_name_counts = {}

    for i, (num_str, match_start, match_end) in enumerate(valid_matches):
        # Extract larger context around the number
        context_start = max(0, match_start - 100)
        context_end = min(len(code_text), match_end + 50)
        context = code_text[context_start:context_end]

        # Look for function name before this parameter
        func_name = None
        param_index = 0
        chain_position = 0

        # Find the nearest function call before this number using preprocessed map
        nearest_func_pos = None
        nearest_func_info = None

        # Binary search for nearest function (much faster than linear search)
        left, right = 0, len(func_positions) - 1
        best_pos = None

        while left <= right:
            mid = (left + right) // 2
            if func_positions[mid] < match_start:
                best_pos = func_positions[mid]
                left = mid + 1
            else:
                right = mid - 1

        if best_pos is not None:
            nearest_func_pos = best_pos
            nearest_func_info = func_info_map[best_pos]

        if nearest_func_info:
            func_name = nearest_func_info['name']
            chain_position = nearest_func_info['chain_position']
            func_match = nearest_func_info['match']

            # Count commas between function start and our number to get parameter index
            func_start = func_match.end()
            between_text = code_text[func_start:match_start]
            param_index = between_text.count(',')

        # Generate TD-compliant parameter name
        if func_name and func_name in hydra_functions:
            param_names = hydra_functions[func_name]
            if param_index < len(param_names):
                base_name = param_names[param_index]

                # TD-compliant naming: Uppercase first letter, lowercase after
                if chain_position == 0:
                    # Source function - no prefix
                    param_name = f"{func_name.capitalize()}{base_name}"
                    label = f"{func_name.title()} {base_name.title()}"
                else:
                    # Chained function - add suffix
                    chain_suffix = chain_names[chain_position] if chain_position < len(chain_names) else f"n{chain_position}"
                    param_name = f"{func_name.capitalize()}{base_name}{chain_suffix}"
                    label = f"{func_name.title()} {base_name.title()} {chain_position}"
            else:
                if chain_position == 0:
                    param_name = f"{func_name.capitalize()}param{param_index + 1}"
                    label = f"{func_name.title()} Param {param_index + 1}"
                else:
                    chain_suffix = chain_names[chain_position] if chain_position < len(chain_names) else f"n{chain_position}"
                    param_name = f"{func_name.capitalize()}param{param_index + 1}{chain_suffix}"
                    label = f"{func_name.title()} Param {param_index + 1} {chain_position}"
        elif func_name:
            # Unknown function but we found one
            if chain_position == 0:
                param_name = f"{func_name.capitalize()}param{param_index + 1}"
                label = f"{func_name.title()} Param {param_index + 1}"
            else:
                chain_suffix = chain_names[chain_position] if chain_position < len(chain_names) else f"n{chain_position}"
                param_name = f"{func_name.capitalize()}param{param_index + 1}{chain_suffix}"
                label = f"{func_name.title()} Param {param_index + 1} {chain_position}"
        else:
            # Fallback to position-based names
            param_name = f"Value{i + 1}"
            label = f"Value {i + 1}"

        # Ensure parameter name is TD-compliant (no underscores, no trailing digits for non-sequence params)
        param_name = re.sub(r'[^a-zA-Z0-9]', '', param_name)

        # Track parameter name usage and add suffix if duplicate
        original_param_name = param_name
        if param_name in param_name_counts:
            param_name_counts[param_name] += 1
            # Add lowercase letter suffix for duplicates (a, b, c, etc.)
            suffix = chr(ord('a') + param_name_counts[param_name] - 1)
            param_name = f"{param_name}{suffix}"
        else:
            param_name_counts[param_name] = 1

        # Mark if this is a color parameter (r, g, b from color/solid functions)
        is_color_param = False
        color_channel = None
        if func_name in color_functions and param_index < 3:
            is_color_param = True
            color_channel = ['r', 'g', 'b'][param_index]

        param_info.append({
            'name': param_name,
            'label': label,
            'context': context,
            'function': func_name or 'unknown',
            'param_index': param_index,
            'is_color_param': is_color_param,
            'color_channel': color_channel,
            'chain_position': chain_position
        })

    return param_info


def group_color_parameters(param_info):
    """Group consecutive r, g, b color parameters into RGB groups"""
    grouped_info = []
    i = 0

    while i < len(param_info):
        info = param_info[i]

        # Check if this starts a color group
        if info.get('is_color_param') and info.get('color_channel') == 'r':
            # Look ahead to see if we have g and b following
            func_name = info['function']
            chain_pos = info.get('chain_position', 0)

            # Collect all consecutive color params from same function call
            color_group = [info]  # Start with r
            j = i + 1

            # Check for g
            if j < len(param_info):
                next_info = param_info[j]
                if (next_info.get('is_color_param') and
                    next_info.get('color_channel') == 'g' and
                    next_info['function'] == func_name and
                    next_info.get('chain_position') == chain_pos):
                    color_group.append(next_info)
                    j += 1

            # Check for b
            if j < len(param_info):
                next_info = param_info[j]
                if (next_info.get('is_color_param') and
                    next_info.get('color_channel') == 'b' and
                    next_info['function'] == func_name and
                    next_info.get('chain_position') == chain_pos):
                    color_group.append(next_info)
                    j += 1

            # Create RGB group parameter info
            chain_suffix = ''
            if chain_pos > 0:
                chain_names = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
                chain_suffix = chain_names[chain_pos] if chain_pos < len(chain_names) else f"n{chain_pos}"

            rgb_name = f"{func_name.capitalize()}rgb{chain_suffix}" if chain_suffix else f"{func_name.capitalize()}rgb"
            rgb_label = f"{func_name.title()} RGB {chain_pos}" if chain_pos > 0 else f"{func_name.title()} RGB"

            # Add RGB group
            grouped_info.append({
                'name': rgb_name,
                'label': rgb_label,
                'context': info['context'],
                'function': func_name,
                'param_index': info['param_index'],
                'is_rgb_group': True,
                'color_params': color_group,  # Store the original r, g, b info
                'num_channels': len(color_group)
            })

            i = j  # Skip past the color params we grouped
        else:
            # Not a color param or not the start of a group, keep as-is
            grouped_info.append(info)
            i += 1

    return grouped_info


def ensure_parameters_with_context(param_info):
    """Ensure we have parameters with intelligent names - ONLY CREATE NEW ONES"""
    controller = op('/project1/hydra_system/direct_param_controller')
    param_page = None
    for page in controller.customPages:
        if page.name == "HydraParams":
            param_page = page
            break

    if not param_page:
        print("Creating HydraParams page...")
        param_page = controller.appendCustomPage("HydraParams")

    # Get existing parameters (including RGB groups)
    existing_params = {}
    for par in param_page.pars:
        if not par.name.startswith('_'):
            # Handle RGB parameters (they come in tuples of r, g, b)
            if hasattr(par, 'vecSize'):
                # This is an RGB/vector parameter
                existing_params[par.name] = par
            else:
                existing_params[par.name] = par

    # Create new parameters ONLY if they don't exist
    created_params = {}
    created_count = 0
    skipped_count = 0

    for i, info in enumerate(param_info):
        param_name = info['name']
        label = info['label']
        original_name = param_name

        # Check if this is an RGB group
        is_rgb_group = info.get('is_rgb_group', False)

        # Check if this exact parameter already exists FIRST
        if param_name in existing_params:
            # Use the existing parameter - don't create new one
            created_params[param_name] = existing_params[param_name]
            skipped_count += 1
            continue

        # Handle name conflicts by adding letters ONLY for new parameters
        counter = 0
        while param_name in existing_params or param_name in created_params:
            suffix_letter = chr(ord('a') + counter)
            param_name = f"{original_name}{suffix_letter}"
            counter += 1

        try:
            if is_rgb_group:
                # Create RGB parameter
                new_param = param_page.appendRGB(param_name, label=label)
                # RGB parameters have r, g, b sub-parameters
                for sub_par in [new_param[0], new_param[1], new_param[2]]:
                    sub_par.normMin = -1000
                    sub_par.normMax = 1000
                    sub_par.clampMin = False
                    sub_par.clampMax = False
                created_params[param_name] = new_param
                print(f"  Created RGB parameter: {param_name} ({label})")
                created_count += 1
            else:
                # Create regular float parameter
                new_param = param_page.appendFloat(param_name, label=label)
                new_param.normMin = -1000
                new_param.normMax = 1000
                new_param.clampMin = False
                new_param.clampMax = False
                created_params[param_name] = new_param
                print(f"  Created parameter: {param_name} ({label})")
                created_count += 1
        except Exception as e:
            print(f"  Warning: Could not create parameter {param_name}: {e}")
            # Fallback to generic name
            fallback_name = f"Param{i + 1}"
            try:
                new_param = param_page.appendFloat(fallback_name, label=f"Param {i + 1}")
                new_param.normMin = -1000
                new_param.normMax = 1000
                new_param.clampMin = False
                new_param.clampMax = False
                created_params[fallback_name] = new_param
                print(f"  Created fallback parameter: {fallback_name}")
                created_count += 1
            except Exception as e2:
                print(f"  ERROR: Could not create fallback parameter: {e2}")

    if created_count > 0:
        print(f"  Created {created_count} new parameters")
    if skipped_count > 0:
        print(f"  Skipped {skipped_count} existing parameters")

    return param_page, created_params


def sync_now():
    """SYNC: Read values from current scene and update parameter sliders - FAST VERSION"""
    print("\n=== SYNCING FROM CURRENT SCENE (FAST) ===")

    # Get current scene code dynamically
    scene_code = get_current_scene_code()
    if not scene_code:
        print("ERROR: No current scene code found")
        return

    print(f"Using scene: {scene_code.path}")

    # Extract numbers with simple regex (including negatives)
    code_text = scene_code.text
    print(f"Scene code: {repr(code_text[:100] + '...' if len(code_text) > 100 else code_text)}")

    # Find all numbers, including negatives
    pattern = r'-?\d+\.?\d*|-?\.\d+'
    all_matches = list(re.finditer(pattern, code_text))

    # Find all {{...}} blocks to skip numbers inside them
    brace_blocks = list(re.finditer(r'\{\{[^}]*\}\}', code_text))
    brace_ranges = [(b.start(), b.end()) for b in brace_blocks]

    # Find all arrow function blocks to skip numbers inside them
    # Match: () => ...) or (x) => ...) including nested parentheses
    arrow_pattern = r'\([^)]*\)\s*=>\s*[^,)]*'
    arrow_blocks = list(re.finditer(arrow_pattern, code_text))
    arrow_ranges = [(a.start(), a.end()) for a in arrow_blocks]

    # Filter out {{null references, time, Math.*, arrow functions, etc
    valid_matches = []
    for match in all_matches:
        start_pos = match.start()
        end_pos = match.end()

        # Check if this number is inside any {{...}} block
        inside_braces = any(block_start <= start_pos < block_end
                          for block_start, block_end in brace_ranges)

        # Check if this number is inside any arrow function
        inside_arrow = any(arrow_start <= start_pos < arrow_end
                         for arrow_start, arrow_end in arrow_ranges)

        # Check for special patterns in preceding text
        preceding_text = code_text[max(0, start_pos-30):start_pos]
        has_skip_pattern = any(skip_pattern in preceding_text for skip_pattern in [
            'time', 'Math.', 'PI', 'frame', 'width', 'height', '=>'
        ])

        # Skip if inside braces, arrow function, or has special pattern
        if inside_braces or inside_arrow or has_skip_pattern:
            continue

        valid_matches.append((match.group(), match.start(), match.end()))

    print(f"Found {len(valid_matches)} valid numbers: {[m[0] for m in valid_matches[:10]]}{'...' if len(valid_matches) > 10 else ''}")

    # Analyze context to generate intelligent parameter names (LIGHTWEIGHT)
    param_info = analyze_parameter_context(code_text, valid_matches)

    # Group color parameters into RGB groups
    grouped_param_info = group_color_parameters(param_info)

    # Ensure we have parameters with intelligent names (ONLY CREATE NEW ONES)
    param_page, created_params = ensure_parameters_with_context(grouped_param_info)
    if not param_page:
        return

    # Update parameter values (FAST - just set values)
    # Need to map valid_matches to grouped_param_info
    synced_count = 0
    value_index = 0  # Track position in valid_matches

    for info in grouped_param_info:
        param_name = info['name']

        # Find the actual parameter (might have had letter appended for uniqueness)
        actual_param = None
        actual_param_name = None
        for created_name, param in created_params.items():
            if created_name == param_name or created_name.startswith(param_name):
                actual_param = param
                actual_param_name = created_name
                break

        if actual_param is not None:
            try:
                if info.get('is_rgb_group'):
                    # Handle RGB group - gather 1-3 color values
                    num_channels = info['num_channels']
                    r_val = 0.0
                    g_val = 0.0
                    b_val = 0.0

                    # Get r value
                    if value_index < len(valid_matches):
                        r_val = float(valid_matches[value_index][0])
                        value_index += 1

                    # Get g value if present
                    if num_channels >= 2 and value_index < len(valid_matches):
                        g_val = float(valid_matches[value_index][0])
                        value_index += 1

                    # Get b value if present
                    if num_channels >= 3 and value_index < len(valid_matches):
                        b_val = float(valid_matches[value_index][0])
                        value_index += 1

                    # Set RGB values
                    old_r = actual_param[0].val
                    old_g = actual_param[1].val
                    old_b = actual_param[2].val

                    actual_param[0].val = r_val
                    actual_param[1].val = g_val
                    actual_param[2].val = b_val

                    print(f"  {actual_param_name}: ({old_r}, {old_g}, {old_b}) -> ({r_val}, {g_val}, {b_val}) [{info['label']}]")
                    synced_count += 1
                else:
                    # Regular float parameter
                    if value_index < len(valid_matches):
                        num_str = valid_matches[value_index][0]
                        old_val = actual_param.val
                        new_val = float(num_str)

                        # Always set wide range and disable clamping for ALL parameters
                        if hasattr(actual_param, 'normMin') and hasattr(actual_param, 'normMax'):
                            actual_param.normMin = -1000
                            actual_param.normMax = 1000
                            actual_param.clampMin = False
                            actual_param.clampMax = False

                        actual_param.val = new_val
                        print(f"  {actual_param_name}: {old_val} -> {new_val} [{info['label']}]")
                        synced_count += 1
                        value_index += 1
            except Exception as e:
                print(f"  ERROR updating {param_name}: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"  WARNING: Could not find parameter for {param_name}")
            # Still need to advance value_index
            if info.get('is_rgb_group'):
                value_index += info['num_channels']
            else:
                value_index += 1

    print(f"SUCCESS: Synced {synced_count} parameters from current scene")


def apply_now():
    """APPLY: Write parameter slider values to current scene"""
    print("\n=== APPLYING TO CURRENT SCENE ===")

    # Get current scene code dynamically
    scene_code = get_current_scene_code()
    if not scene_code:
        print("ERROR: No current scene code found")
        return

    # Trace to find the original source DAT
    source_dat = trace_to_source_dat(scene_code)

    print(f"Reading code from: {scene_code.path}")
    if source_dat != scene_code:
        print(f"Will write changes to: {source_dat.path} (original source)")
    else:
        print(f"Will write changes to: {scene_code.path} (same as read location)")

    # Get parameter page
    controller = op('/project1/hydra_system/direct_param_controller')
    param_page = None
    for page in controller.customPages:
        if page.name == "HydraParams":
            param_page = page
            break

    if not param_page:
        print("ERROR: HydraParams page not found")
        return

    # Get parameter values by NAME (not index) for proper matching
    param_values_by_name = {}
    for par in param_page.pars:
        if not par.name.startswith('_'):
            # Check if this is an RGB parameter
            if hasattr(par, 'vecSize') and par.vecSize == 3:
                # Store RGB values separately for expansion
                param_values_by_name[par.name] = {
                    'type': 'rgb',
                    'r': par[0].val,
                    'g': par[1].val,
                    'b': par[2].val
                }
            else:
                param_values_by_name[par.name] = {
                    'type': 'single',
                    'value': par.val
                }

    print(f"Loaded {len(param_values_by_name)} parameters by name")

    # Get original code and find replacement positions
    original_code = scene_code.text
    print(f"Original code: {repr(original_code[:100] + '...' if len(original_code) > 100 else original_code)}")

    # Find all numbers including negatives
    pattern = r'-?\d+\.?\d*|-?\.\d+'
    all_matches = list(re.finditer(pattern, original_code))

    # Find all {{...}} blocks to skip numbers inside them
    brace_blocks = list(re.finditer(r'\{\{[^}]*\}\}', original_code))
    brace_ranges = [(b.start(), b.end()) for b in brace_blocks]

    # Find all arrow function blocks to skip numbers inside them
    arrow_pattern = r'\([^)]*\)\s*=>\s*[^,)]*'
    arrow_blocks = list(re.finditer(arrow_pattern, original_code))
    arrow_ranges = [(a.start(), a.end()) for a in arrow_blocks]

    # Filter out {{null references and special patterns
    valid_matches = []
    for match in all_matches:
        start_pos = match.start()
        end_pos = match.end()

        # Check if this number is inside any {{...}} block
        inside_braces = any(block_start <= start_pos < block_end
                          for block_start, block_end in brace_ranges)

        # Check if this number is inside any arrow function
        inside_arrow = any(arrow_start <= start_pos < arrow_end
                         for arrow_start, arrow_end in arrow_ranges)

        # Check for special patterns in preceding text
        preceding_text = original_code[max(0, start_pos-30):start_pos]
        has_skip_pattern = any(skip_pattern in preceding_text for skip_pattern in [
            'time', 'Math.', 'PI', 'frame', 'width', 'height', '=>'
        ])

        # Skip if inside braces, arrow function, or has special pattern
        if inside_braces or inside_arrow or has_skip_pattern:
            continue

        valid_matches.append(match)

    print(f"Found {len(valid_matches)} valid replacement positions")

    # Convert match objects to tuples for analyze_parameter_context
    valid_match_tuples = []
    for match in valid_matches:
        num_str = match.group()
        match_start = match.start()
        match_end = match.end()
        valid_match_tuples.append((num_str, match_start, match_end))

    # Analyze context to get parameter info for each position
    # This uses the same logic as sync_now to match parameters by name
    param_info = analyze_parameter_context(original_code, valid_match_tuples)

    # Group color parameters into RGB groups (same as sync_now)
    grouped_param_info = group_color_parameters(param_info)

    # Map each position to its parameter value
    # Need to expand RGB groups back to individual r, g, b values
    print("\nMapping positions to parameters:")
    position_to_value = {}
    value_index = 0

    for info in grouped_param_info:
        if info.get('is_rgb_group'):
            # RGB group - expand to r, g, b values
            param_name = info['name']

            if param_name in param_values_by_name:
                param_data = param_values_by_name[param_name]
                num_channels = info['num_channels']

                # Map r, g, b values to consecutive positions
                if num_channels >= 1:
                    position_to_value[value_index] = param_data['r']
                    print(f"  Position {value_index}: {param_name}.r = {param_data['r']}")
                    value_index += 1
                if num_channels >= 2:
                    position_to_value[value_index] = param_data['g']
                    print(f"  Position {value_index}: {param_name}.g = {param_data['g']}")
                    value_index += 1
                if num_channels >= 3:
                    position_to_value[value_index] = param_data['b']
                    print(f"  Position {value_index}: {param_name}.b = {param_data['b']}")
                    value_index += 1
            else:
                print(f"  RGB group {param_name} NOT FOUND in parameters")
                value_index += info['num_channels']
        else:
            # Regular parameter
            param_name = info['name']  # Use 'name' not 'param_name'

            if param_name in param_values_by_name:
                param_data = param_values_by_name[param_name]
                position_to_value[value_index] = param_data['value']
                print(f"  Position {value_index}: {param_name} = {param_data['value']}")
            else:
                print(f"  Position {value_index}: {param_name} NOT FOUND in parameters")

            value_index += 1

    # Replace from end to start to preserve positions
    print("\nApplying changes:")
    new_code = original_code
    applied_count = 0
    for i in reversed(range(len(valid_matches))):
        if i in position_to_value:
            match = valid_matches[i]
            new_value = position_to_value[i]

            # Format number nicely
            if abs(new_value - round(new_value)) < 0.001:
                new_value_str = str(int(round(new_value)))
            else:
                new_value_str = "{:.3f}".format(new_value).rstrip('0').rstrip('.')

            old_value = match.group()
            new_code = new_code[:match.start()] + new_value_str + new_code[match.end():]
            print(f"  Position {i}: '{old_value}' -> '{new_value_str}'")
            applied_count += 1

    # Update scene - try to write to the best DAT in the chain
    # Priority: SceneCodeSender > SceneCode > traced source > scene_code
    write_success = False
    dats_to_try = []

    # Walk backwards from source_dat to find all DATs in chain
    current = scene_code
    chain_dats = []
    visited = set()

    def collect_chain(dat):
        """Collect all DATs in the input chain"""
        if not dat or dat.path in visited:
            return
        visited.add(dat.path)
        chain_dats.append(dat)

        # For selectDAT, always check the dat parameter first
        if dat.OPType == 'selectDAT' and hasattr(dat.par, 'dat'):
            dat_path = dat.par.dat.eval()
            if dat_path:
                next_dat = op(dat_path)
                if next_dat:
                    collect_chain(next_dat)
                    return

        # Follow inputs for other DAT types
        if dat.inputs and len(dat.inputs) > 0:
            input_dat = dat.inputs[0]
            if input_dat:
                collect_chain(input_dat)

    collect_chain(scene_code)

    print(f"\nCollected {len(chain_dats)} DATs in chain:")
    for dat in chain_dats:
        tags_str = f" (tags: {', '.join(dat.tags)})" if dat.tags else ""
        print(f"  - {dat.path} [{dat.OPType}]{tags_str}")

    # Prioritize SceneCode tagged DATs (no inputs = original source)
    for dat in chain_dats:
        if 'SceneCode' in dat.tags:
            dats_to_try.append(dat)

    # Then try SceneCodeSender tagged DATs
    for dat in chain_dats:
        if 'SceneCodeSender' in dat.tags and dat not in dats_to_try:
            dats_to_try.append(dat)

    # Then try any other DATs in chain
    for dat in chain_dats:
        if dat not in dats_to_try and dat.OPType == 'textDAT':
            dats_to_try.append(dat)

    print(f"\nTrying to write in priority order:")

    # Try writing to each DAT in priority order
    for dat_to_write in dats_to_try:
        print(f"  Attempting: {dat_to_write.path}")
        try:
            # Check if DAT is locked and try to unlock
            if hasattr(dat_to_write.par, 'locked') and dat_to_write.par.locked.eval():
                print(f"    Unlocking...")
                dat_to_write.par.locked = False

            # Check if DAT has file sync enabled and disable it
            if hasattr(dat_to_write.par, 'syncfile') and dat_to_write.par.syncfile.eval():
                print(f"    Disabling file sync...")
                dat_to_write.par.syncfile = False

            # Try to write
            dat_to_write.text = new_code
            print(f"  ✓ SUCCESS: Applied {applied_count} changes to: {dat_to_write.path}")
            write_success = True
            break
        except Exception as e:
            print(f"    ✗ Failed: {e}")
            continue

    if not write_success:
        print(f"ERROR: Could not write to any DAT in the chain")


def test_both():
    """Test both sync and apply functions"""
    print("\n" + "=" * 30)
    print("TESTING BOTH FUNCTIONS")
    print("=" * 30)
    sync_now()
    apply_now()


def remove_unused_parameters():
    """Remove parameters that are not needed for the current scene"""
    print("\n=== REMOVING UNUSED PARAMETERS ===")

    # Get current scene code dynamically
    scene_code = get_current_scene_code()
    if not scene_code:
        print("ERROR: No current scene code found")
        return

    print(f"Analyzing scene: {scene_code.path}")

    # Extract numbers and generate parameter info (same as sync_now)
    code_text = scene_code.text
    pattern = r'-?\d+\.?\d*|-?\.\d+'
    all_matches = list(re.finditer(pattern, code_text))

    # Find all {{...}} blocks to skip numbers inside them
    brace_blocks = list(re.finditer(r'\{\{[^}]*\}\}', code_text))
    brace_ranges = [(b.start(), b.end()) for b in brace_blocks]

    # Find all arrow function blocks to skip numbers inside them
    arrow_pattern = r'\([^)]*\)\s*=>\s*[^,)]*'
    arrow_blocks = list(re.finditer(arrow_pattern, code_text))
    arrow_ranges = [(a.start(), a.end()) for a in arrow_blocks]

    # Filter out {{null references
    valid_matches = []
    for match in all_matches:
        start_pos = match.start()

        # Check if this number is inside any {{...}} block
        inside_braces = any(block_start <= start_pos < block_end
                          for block_start, block_end in brace_ranges)

        # Check if this number is inside any arrow function
        inside_arrow = any(arrow_start <= start_pos < arrow_end
                         for arrow_start, arrow_end in arrow_ranges)

        # Check for special patterns in preceding text
        preceding_text = code_text[max(0, start_pos-30):start_pos]
        has_skip_pattern = any(skip_pattern in preceding_text for skip_pattern in [
            'time', 'Math.', 'PI', 'frame', 'width', 'height', '=>'
        ])

        # Skip if inside braces, arrow function, or has special pattern
        if not inside_braces and not inside_arrow and not has_skip_pattern:
            valid_matches.append((match.group(), match.start(), match.end()))

    # Analyze context to get the parameter names we need
    param_info = analyze_parameter_context(code_text, valid_matches)
    grouped_param_info = group_color_parameters(param_info)
    needed_param_names = set(info['name'] for info in grouped_param_info)

    print(f"Current scene needs {len(needed_param_names)} parameters: {sorted(needed_param_names)}")

    # Get parameter page
    controller = op('/project1/hydra_system/direct_param_controller')
    param_page = None
    for page in controller.customPages:
        if page.name == "HydraParams":
            param_page = page
            break

    if not param_page:
        print("ERROR: HydraParams page not found")
        return

    # Collect all user parameters and determine which to remove
    all_user_params = []
    params_to_remove = []

    for par in param_page.pars:
        if not par.name.startswith('_'):  # Skip system parameters
            all_user_params.append(par)
            # Remove parameters whose names are NOT in the needed set
            if par.name not in needed_param_names:
                params_to_remove.append(par)

    user_param_count = len(all_user_params)
    print(f"Found {user_param_count} user parameters, {len(params_to_remove)} are unused")

    # Remove unused parameters
    removed_count = 0
    for param in params_to_remove:
        try:
            param_name = param.name
            param.destroy()
            print(f"  Removed: {param_name}")
            removed_count += 1
        except Exception as e:
            print(f"  Warning: Could not remove parameter: {e}")

    if removed_count > 0:
        print(f"SUCCESS: Removed {removed_count} unused parameters")
    else:
        print("No unused parameters to remove")


def cleanup_and_sync():
    """Remove unused parameters and then sync with current scene"""
    print("\n=== CLEANUP AND SYNC ===")
    remove_unused_parameters()
    sync_now()


def set_current_scene(scene_number):
    """Helper function to manually set which scene should be considered 'current'"""
    scene_name = f"scene{scene_number}_code"
    scene_code = op(f'/project1/hydra_system/code/CodeManager/{scene_name}')
    if scene_code:
        print(f"Scene {scene_number} is available: {scene_name}")
        return True
    else:
        print(f"Scene {scene_number} not found: {scene_name}")
        return False

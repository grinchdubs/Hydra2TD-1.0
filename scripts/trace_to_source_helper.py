"""
Helper functions to trace from selectDAT back to original source textDAT
For use with Hydra Parameter Creation system
"""

def trace_to_source_dat(dat_op):
    """
    Trace from a DAT (possibly a selectDAT) back to the original source textDAT.

    Follows the chain:
    selectDAT in CodeManager -> SceneCodeSender textDAT -> original SceneCode textDAT

    Args:
        dat_op: The DAT operator to trace from

    Returns:
        The original source textDAT, or the input dat_op if no source found
    """

    print(f"\n=== TRACING SOURCE FOR: {dat_op.path} ===")
    print(f"  DAT type: {dat_op.OPType}")

    # Step 1: Check if this is a selectDAT
    if dat_op.OPType == 'selectDAT':
        print("  This is a selectDAT, checking selected input...")

        # Get the selectDAT's input
        if dat_op.inputs:
            # Get the selected index
            select_index = int(dat_op.par.index.eval())
            print(f"  Select index: {select_index}")

            # Get the input at that index
            if len(dat_op.inputs) > select_index:
                input_dat = dat_op.inputs[select_index]
                if input_dat:
                    print(f"  Selected input: {input_dat.path}")
                    # Recursively trace from the selected input
                    return trace_to_source_dat(input_dat)
                else:
                    print("  WARNING: Selected input is None")
            else:
                print(f"  WARNING: Select index {select_index} out of range")
        else:
            print("  WARNING: selectDAT has no inputs")

    # Step 2: Check if this DAT has inputs (could be connected from another DAT)
    elif dat_op.inputs and len(dat_op.inputs) > 0:
        input_dat = dat_op.inputs[0]
        if input_dat:
            print(f"  DAT has input: {input_dat.path}")

            # Check if the input has the SceneCode tag
            if 'SceneCode' in input_dat.tags:
                print(f"  ✓ Found source with SceneCode tag: {input_dat.path}")
                return input_dat

            # Otherwise continue tracing
            return trace_to_source_dat(input_dat)

    # Step 3: Check if this DAT itself has the SceneCode tag (it's the source)
    if 'SceneCode' in dat_op.tags:
        print(f"  ✓ This DAT has SceneCode tag, it's the source: {dat_op.path}")
        return dat_op

    # Step 4: Fallback - return the current DAT
    print(f"  ✓ Using current DAT as source (end of chain): {dat_op.path}")
    return dat_op


def get_source_for_current_scene():
    """
    Get the source textDAT for the currently active scene.
    This combines the existing get_current_scene_code() logic with source tracing.

    Returns:
        Tuple of (scene_code_dat_in_codemanager, source_textdat_to_write_to)
    """

    # Import the existing function
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from manual_triggers_fixed import get_current_scene_code

    # Get the current scene code (the selectDAT in CodeManager)
    scene_code = get_current_scene_code()

    if not scene_code:
        print("ERROR: Could not find current scene code")
        return None, None

    print(f"\nCurrent scene in CodeManager: {scene_code.path}")

    # Trace back to find the source
    source_dat = trace_to_source_dat(scene_code)

    if source_dat and source_dat != scene_code:
        print(f"\n✓ Found original source: {source_dat.path}")
        print(f"  Will READ from: {scene_code.path}")
        print(f"  Will WRITE to: {source_dat.path}")
    else:
        print(f"\n  Using same DAT for read/write: {scene_code.path}")

    return scene_code, source_dat


def test_trace():
    """Test the tracing function on current scene"""
    scene_code, source_dat = get_source_for_current_scene()

    if scene_code and source_dat:
        print("\n=== TEST SUCCESSFUL ===")
        print(f"Read from (CodeManager): {scene_code.path}")
        print(f"Write to (Source): {source_dat.path}")
        print(f"Source has SceneCode tag: {'SceneCode' in source_dat.tags}")
        return True
    else:
        print("\n=== TEST FAILED ===")
        return False

"""
Install Fixed Manual Triggers
Run this to update your manual_triggers DAT with the consolidated, fixed version
"""

import sys

def install_fixed_triggers():
    print("=" * 70)
    print("INSTALLING FIXED MANUAL TRIGGERS")
    print("=" * 70)

    # Read the fixed script
    script_path = r'C:/Users/cuban/HydraToTD/manual_triggers_fixed.py'
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            fixed_code = f.read()
    except Exception as e:
        print(f"ERROR reading fixed script: {e}")
        return False

    # Find or create the manual_triggers DAT
    controller = op('/project1/hydra_system/direct_param_controller')
    if not controller:
        print("ERROR: direct_param_controller not found")
        return False

    manual_triggers = controller.op('manual_triggers')
    if not manual_triggers:
        print("Creating manual_triggers DAT...")
        manual_triggers = controller.create(textDAT, 'manual_triggers')

    # Update the code
    manual_triggers.text = fixed_code
    print(f"✓ Updated: {manual_triggers.path}")

    print("\n" + "=" * 70)
    print("INSTALLATION COMPLETE!")
    print("=" * 70)
    print("\nFIXES APPLIED:")
    print("  ✓ TouchDesigner-compliant parameter naming (Oscfrequency, Fxtwocolor, etc.)")
    print("  ✓ RGB color parameters grouped together")
    print("  ✓ No tool_dat1 dependency - all detection logic consolidated")
    print("  ✓ Fixed regex to properly detect numbers (including negatives)")
    print("  ✓ Parameters no longer end with digits (TD compliant)")
    print("\nUSAGE:")
    print("  Sync:  op('/project1/hydra_system/direct_param_controller/manual_triggers').module.sync_now()")
    print("  Apply: op('/project1/hydra_system/direct_param_controller/manual_triggers').module.apply_now()")
    print("  Test:  op('/project1/hydra_system/direct_param_controller/manual_triggers').module.test_both()")
    print("\n" + "=" * 70)

    return True


if __name__ == '__main__':
    success = install_fixed_triggers()
    if success:
        print("\n✓ Ready to use! Try running sync_now() to test the fixed detection.")
    else:
        print("\n✗ Installation failed. Check the errors above.")

import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure ops is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from ops.patterns.claw_loop import LoopConfig, ClawActionLoop

def test_loop_config_defaults():
    config = LoopConfig(target_window_title="Test Window")
    assert config.max_steps == 15
    assert config.step_delay_sec == 2.0
    assert config.target_window_title == "Test Window"

@patch('ops.patterns.claw_loop.claw_control.check_panic_button', return_value=True)
@patch('ops.patterns.claw_loop.claw_control.get_cursor_position', return_value=(0,0))
@patch('ops.patterns.claw_loop.claw_control.set_expected_position')
def test_start_loop_panic_button(mock_set_pos, mock_get_pos, mock_panic):
    # Let it Fail rule applied: if panic button is triggered, loop stops immediately
    config = LoopConfig(target_window_title="Test")
    loop = ClawActionLoop(config)
    loop.start_loop()
    mock_panic.assert_called()

def test_process_preemption_stop():
    config = LoopConfig(target_window_title="Test")
    loop = ClawActionLoop(config)
    result = loop._execute_preempt_action("stop", {}, 1, "Test Window", None)
    assert result is False

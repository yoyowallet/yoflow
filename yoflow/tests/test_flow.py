import unittest

from yoflow.flow import Flow


class TestFlow(unittest.TestCase):

    def test_init(self):
        class BasicFlow(Flow):
            states = {}
        flow = BasicFlow()
        assert flow.reversed_states == {}
        assert flow.field == 'state'
        assert flow.lookup_field == 'pk'

    def test_init_overrides(self):
        class BasicFlow(Flow):
            states = {}
            field = 'test'
            lookup_field = 'id'
        flow = BasicFlow()
        assert flow.reversed_states == {}
        assert flow.field == 'test'
        assert flow.lookup_field == 'id'

    def test_urls(self):
        pass

    def test_validate_state_change(self):
        pass

    def test_invalid_state_change_raises_exception(self):
        pass

    def test_process_state_to_state(self):
        pass

    def test_process_on_state(self):
        pass

    def test_process_on_all(self):
        pass

    def test_process(self):
        pass

    def test_check_user_permissions(self):
        pass

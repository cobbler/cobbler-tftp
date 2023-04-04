"""
Tests for the CobblerTftpSchemaVersion class
"""

from cobbler_tftp.settings.migrations import CobblerTftpSchemaVersion


class TestCobblertTftpSchemaVersion:
    def setup_method(self):
        self.v1_0 = CobblerTftpSchemaVersion(1, 0)
        self.v2_0 = CobblerTftpSchemaVersion(2, 0)
        self.v2_1 = CobblerTftpSchemaVersion(2, 1)

    def test_init(self):
        assert isinstance(self.v1_0, CobblerTftpSchemaVersion)
        assert isinstance(self.v2_0, CobblerTftpSchemaVersion)
        assert isinstance(self.v2_1, CobblerTftpSchemaVersion)
        assert self.v1_0.major == 1
        assert self.v1_0.minor == 0

    def test_eq(self):
        assert self.v1_0 == self.v1_0
        assert not self.v1_0 == self.v2_0

    def test_ne(self):
        assert self.v1_0 != self.v2_0
        assert not self.v1_0 != self.v1_0

    def test_lt(self):
        assert self.v1_0 < self.v2_0
        assert self.v2_0 < self.v2_1
        assert not self.v2_1 < self.v1_0

    def test_le(self):
        assert self.v1_0 <= self.v1_0
        assert self.v1_0 <= self.v2_0
        assert self.v2_0 <= self.v2_1
        assert not self.v2_0 <= self.v1_0

    def test_gt(self):
        assert self.v2_0 > self.v1_0
        assert self.v2_1 > self.v2_0
        assert not self.v1_0 > self.v1_0
        assert not self.v1_0 > self.v2_1

    def test_ge(self):
        assert self.v2_0 >= self.v1_0
        assert self.v2_1 >= self.v2_0
        assert self.v2_1 >= self.v2_1

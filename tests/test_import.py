"""Basic import tests."""

def test_import():
    """Test that package can be imported."""
    from jetson_orin_st7789 import ST7789, ST7789Error, ST7789InitError
    assert ST7789 is not None

def test_version():
    """Test version is accessible."""
    from jetson_orin_st7789 import __version__
    assert __version__ == "1.0.0"

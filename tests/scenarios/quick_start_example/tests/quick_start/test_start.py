def test_passthrough(tf_outputs, tf_vars):
    assert tf_outputs["pass_through"] == tf_vars["pass_through"]

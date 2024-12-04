def test_passthrough(tf_output, tf_variables):
    assert tf_output["pass_through"] == tf_variables["pass_through"]

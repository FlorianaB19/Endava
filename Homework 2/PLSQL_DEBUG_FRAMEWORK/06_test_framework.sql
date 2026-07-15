BEGIN

    debug_utils.enable_debug;

    debug_utils.log_msg(
        'TEST_FRAMEWORK',
        10,
        'Framework started successfully.'
    );

    debug_utils.log_variable(
        'TEST_FRAMEWORK',
        20,
        'TEST_VARIABLE',
        '12345'
    );

    debug_utils.log_error(
        'TEST_FRAMEWORK',
        30,
        'This is only a test error.'
    );

END;
/

COMMIT;
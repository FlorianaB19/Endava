CREATE OR REPLACE PACKAGE BODY debug_utils AS

    ------------------------------------------------------------------
    -- Enable debugging
    ------------------------------------------------------------------
    PROCEDURE enable_debug IS
    BEGIN
        g_debug_mode := TRUE;
    END enable_debug;

    ------------------------------------------------------------------
    -- Disable debugging
    ------------------------------------------------------------------
    PROCEDURE disable_debug IS
    BEGIN
        g_debug_mode := FALSE;
    END disable_debug;

    ------------------------------------------------------------------
    -- Generic logging procedure
    ------------------------------------------------------------------
    PROCEDURE log(
        p_module_name IN VARCHAR2,
        p_line_no     IN NUMBER,
        p_log_level   IN VARCHAR2,
        p_message      IN VARCHAR2
    ) IS
    BEGIN

        IF NOT g_debug_mode THEN
            RETURN;
        END IF;

        INSERT INTO debug_log
        (
            module_name,
            line_no,
            log_level,
            log_message
        )
        VALUES
        (
            p_module_name,
            p_line_no,
            UPPER(p_log_level),
            p_message
        );

    END log;

    ------------------------------------------------------------------
    -- Log informational message
    ------------------------------------------------------------------
    PROCEDURE log_msg(
        p_module_name IN VARCHAR2,
        p_line_no     IN NUMBER,
        p_message      IN VARCHAR2
    ) IS
    BEGIN

        log(
            p_module_name,
            p_line_no,
            'INFO',
            p_message
        );

    END log_msg;

    ------------------------------------------------------------------
    -- Log variable
    ------------------------------------------------------------------
    PROCEDURE log_variable(
        p_module_name IN VARCHAR2,
        p_line_no     IN NUMBER,
        p_variable    IN VARCHAR2,
        p_value       IN VARCHAR2
    ) IS
    BEGIN

        log(
            p_module_name,
            p_line_no,
            'DEBUG',
            p_variable || ' = ' || p_value
        );

    END log_variable;

    ------------------------------------------------------------------
    -- Log error
    ------------------------------------------------------------------
    PROCEDURE log_error(
        p_module_name IN VARCHAR2,
        p_line_no     IN NUMBER,
        p_error       IN VARCHAR2
    ) IS
    BEGIN

        log(
            p_module_name,
            p_line_no,
            'ERROR',
            p_error
        );

    END log_error;

END debug_utils;
/
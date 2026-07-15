CREATE OR REPLACE PACKAGE debug_utils AS

    ------------------------------------------------------------------
    -- Global debug flag
    ------------------------------------------------------------------
    g_debug_mode BOOLEAN := FALSE;

    ------------------------------------------------------------------
    -- Enable debugging
    ------------------------------------------------------------------
    PROCEDURE enable_debug;

    ------------------------------------------------------------------
    -- Disable debugging
    ------------------------------------------------------------------
    PROCEDURE disable_debug;

    ------------------------------------------------------------------
    -- Generic logging procedure
    ------------------------------------------------------------------
    PROCEDURE log(
        p_module_name IN VARCHAR2,
        p_line_no     IN NUMBER,
        p_log_level   IN VARCHAR2,
        p_message     IN VARCHAR2
    );

    ------------------------------------------------------------------
    -- Information message
    ------------------------------------------------------------------
    PROCEDURE log_msg(
        p_module_name IN VARCHAR2,
        p_line_no     IN NUMBER,
        p_message     IN VARCHAR2
    );

    ------------------------------------------------------------------
    -- Variable logger
    ------------------------------------------------------------------
    PROCEDURE log_variable(
        p_module_name IN VARCHAR2,
        p_line_no     IN NUMBER,
        p_variable    IN VARCHAR2,
        p_value       IN VARCHAR2
    );

    ------------------------------------------------------------------
    -- Error logger
    ------------------------------------------------------------------
    PROCEDURE log_error(
        p_module_name IN VARCHAR2,
        p_line_no     IN NUMBER,
        p_error       IN VARCHAR2
    );

END debug_utils;
/
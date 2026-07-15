CREATE OR REPLACE PROCEDURE adjust_salaries_by_commission
IS

    ------------------------------------------------------------------
    -- Cursor that retrieves all employees
    ------------------------------------------------------------------
    CURSOR c_employees IS
        SELECT employee_id,
               salary,
               commission_pct
        FROM employees
        ORDER BY employee_id;

    ------------------------------------------------------------------
    -- Local variables
    ------------------------------------------------------------------
    v_old_salary    NUMBER;
    v_new_salary    NUMBER;
    v_updated_count NUMBER := 0;

BEGIN

    ------------------------------------------------------------------
    -- Enable debugging
    ------------------------------------------------------------------
    debug_utils.enable_debug;

    debug_utils.log_msg(
        'ADJUST_SALARIES',
        1,
        'Procedure started.'
    );

    ------------------------------------------------------------------
    -- Process every employee
    ------------------------------------------------------------------
    FOR rec IN c_employees LOOP

        debug_utils.log_msg(
            'ADJUST_SALARIES',
            20,
            'Processing employee ' || rec.employee_id
        );

        --------------------------------------------------------------
        -- Save old salary
        --------------------------------------------------------------
        v_old_salary := rec.salary;

        --------------------------------------------------------------
        -- Calculate new salary
        --------------------------------------------------------------
        IF rec.commission_pct IS NULL THEN

            v_new_salary := rec.salary * 1.02;

        ELSE

            v_new_salary := rec.salary * (1 + rec.commission_pct);

        END IF;

        --------------------------------------------------------------
        -- Log old salary
        --------------------------------------------------------------
        debug_utils.log_variable(
            'ADJUST_SALARIES',
            30,
            'OLD_SALARY',
            TO_CHAR(v_old_salary)
        );

        --------------------------------------------------------------
        -- Log new salary
        --------------------------------------------------------------
        debug_utils.log_variable(
            'ADJUST_SALARIES',
            40,
            'NEW_SALARY',
            TO_CHAR(v_new_salary)
        );

        --------------------------------------------------------------
        -- Update employee salary
        --------------------------------------------------------------
        UPDATE employees
        SET salary = v_new_salary
        WHERE employee_id = rec.employee_id;

        v_updated_count := v_updated_count + 1;

        --------------------------------------------------------------
        -- Log successful update
        --------------------------------------------------------------
        debug_utils.log_msg(
            'ADJUST_SALARIES',
            50,
            'Employee updated successfully.'
        );

    END LOOP;

    ------------------------------------------------------------------
    -- Save all changes
    ------------------------------------------------------------------
    COMMIT;

    ------------------------------------------------------------------
    -- Final message
    ------------------------------------------------------------------
    debug_utils.log_msg(
        'ADJUST_SALARIES',
        999,
        'Procedure finished successfully. Employees updated: '
        || v_updated_count
    );

    ------------------------------------------------------------------
    -- Disable debugging
    ------------------------------------------------------------------
    debug_utils.disable_debug;

EXCEPTION

    WHEN OTHERS THEN

        --------------------------------------------------------------
        -- Log unexpected error
        --------------------------------------------------------------
        debug_utils.log_error(
            'ADJUST_SALARIES',
            1000,
            SQLERRM
        );

        ROLLBACK;

        RAISE;

END adjust_salaries_by_commission;
/
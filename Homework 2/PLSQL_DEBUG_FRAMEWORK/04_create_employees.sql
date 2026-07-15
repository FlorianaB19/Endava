CREATE TABLE employees (
    employee_id NUMBER GENERATED ALWAYS AS IDENTITY,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    salary NUMBER(10,2) NOT NULL,
    commission_pct NUMBER(4,2),
    department_id NUMBER,
    hire_date DATE DEFAULT SYSDATE,
    CONSTRAINT pk_employees PRIMARY KEY (employee_id)
);
/